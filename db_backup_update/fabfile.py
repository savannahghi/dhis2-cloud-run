import os

from fabric import Connection, task


@task
def createproddbdump(ctx):
    with Connection(
        os.environ["PROD_HOST"],
        user=os.environ["PROD_SYS_USER"],
        connect_kwargs={
            "key_filename": [
                os.environ["DEPLOY_KEY"],
            ]
        },
    ) as c:
        with c.cd("/home/" + os.environ["PROD_SYS_USER"] + "/"):
            c.run(
                "PGPASSWORD="
                + os.environ["PROD_PG_PASSWORD"]
                + " pg_dump -U "
                + os.environ["PROD_DB_USER"]
                + " --host="
                + os.environ["PROD_PG_HOST"]
                + " "
                + os.environ["PROD_DB_NAME"]
                + " --port="
                + os.environ["PROD_PG_PORT"]
                + " >"
                + "PROD_DB_FILE.sql"
            )
            c.run("echo success creating dump on prod server")
            c.run(
                "scp -i ~/.ssh/google_compute_engine "
                + " PROD_DB_FILE.sql "
                + os.environ["TEST_SYS_USER"]
                + "@"
                + os.environ["TEST_DOMAIN"]
                + ":/home/"
                + os.environ["TEST_SYS_USER"]
                + "/"
            )
            c.run("echo success copying prod dump to test server")


@task
def backupandupdatetestdb(ctx):
    """
    - ssh to test server
    - generate test db dump file
    - create copies of the dump file to cloud backet
    - update the test db with the prod dump file
    - restart postgres
    """
    with Connection(
        os.environ["TEST_HOST"],
        user=os.environ["TEST_SYS_USER"],
        connect_kwargs={
            "key_filename": [
                os.environ["DEPLOY_KEY"],
            ]
        },
    ) as c:

        with c.cd("/home/" + os.environ["TEST_SYS_USER"] + "/"):
            c.run(
                "PGPASSWORD="
                + os.environ["TEST_PG_PASSWORD"]
                + " pg_dump -U "
                + os.environ["TEST_DB_USER"]
                + " --host="
                + os.environ["TEST_PG_HOST"]
                + " "
                + os.environ["TEST_DB_NAME"]
                + " --port="
                + os.environ["TEST_PG_PORT"]
                + " >"
                + "TEST_DB_FILE.sql"
            )
            c.run("echo success creating test dump")
            c.run("gsutil cp TEST_DB_FILE.sql gs://fahari-ya-jamii-test/test_db_backup/")
            c.run("echo success creating test db backup on cloud bucket")
            c.run("echo starting test db update")
            c.run("sudo service postgresql stop")
            c.run("sudo service postgresql start")
            c.run("sudo -u postgres psql")
            c.run("echo success accessing pg shell")
            c.run("drop database " + os.environ["TEST_DB_NAME"] + ";")
            c.run("echo success test db drop")
            c.run(
                "create database "
                + os.environ["TEST_DB_NAME"]
                + " with owner "
                + os.environ["TEST_DB_USER"]
                + ";"
            )
            c.run("\q")  # noqa
            c.run("sudo -u postgres psql " +
                  os.environ["TEST_DB_NAME"] + " < PROD_DB_FILE.sql")
            c.run("echo success updating test db")


@task
def runscript(ctx):
    createproddbdump(ctx)
    backupandupdatetestdb(ctx)

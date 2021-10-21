### How to run the script

1. Install fabric on your system(https://docs.fabfile.org/en/2.6/getting-started.html)
pip install fabric==2.6
2. Edit and activate the environment variables.
    DHIS2_DEPLOY/db_backup_and_update$ source env_vars.sh
3. Run the script as;
    DHIS2_DEPLOY/db_backup_and_update$ fab runscript

### Ensure:

- Ensure Cloud API access scopes is allowed in the vm for gsutil cp to work
- Fabfile function names do not contain underscores
- Only name the main file as fabfile or fabfile.py


### Resources
- https://docs.fabfile.org/en/2.6/concepts/configuration.html
- https://cloud.google.com/compute/docs/instances/transfer-files
- https://cloud.google.com/storage/docs/folders#gsutil

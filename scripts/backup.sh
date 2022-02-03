#!/bin/bash

# Set some variables.
DB_NAME=your_db_name
DB_USER=your_user_name
DB_PWD=your_db_pwd

# Other vars
USER="$USER"
now="$(date +'%d_%m_%Y_%H_%M_%S')"
dump_data="dhis2_db_backup_$now".sql
dump_folder="/home/$USER/db_backups/"

# create directory if it does not already exist
mkdir -p $dump_folder

# Keep only 5 latest files
cd $dump_folder && rm -rf `ls -t | awk 'NR>4'`

dump_file="$dump_folder/$dump_data"
# Create a dump file in the local backup directory
PGPASSWORD=$DB_PWD pg_dump -U $DB_USER --host="127.0.0.1" $DB_NAME --port=5432 > $dump_file


# Ensure only 5 latest dumps exist. I.e delete one, oldest one
no_of_files=$(gsutil ls gs://fahariyajamii-dhis2-backups/prod_db_dumps | wc -l)


if [[ $no_of_files -gt 5 ]]
then
    # Delete the last file
    gsutil ls gs://fahariyajamii-dhis2-backups/prod_db_dumps | awk '{print}' | tail -1 | xargs gsutil rm
    # Copy dump file to cloud bucket
    gsutil cp $dump_file "gs://fahariyajamii-dhis2-backups/prod_db_dumps"
else
    # Copy dump file to cloud bucket. Retain only 5 latest copies of dump file
    gsutil cp $dump_file "gs://fahariyajamii-dhis2-backups/prod_db_dumps"
fi

exit 0
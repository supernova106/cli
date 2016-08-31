!#/bin/bash
# Command Line to run from terminal
# Logs result to file s3_backup.log
# Command will run in the background
/usr/local/bin/s3cmd sync -v /home/ubuntu/data/ s3://<S3_BUCKET> /home/ubuntu/s3_backup.log


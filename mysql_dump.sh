DBNAME=$1
DATE=`date +"%Y%m%d"`
SQLFILE=$DBNAME-${DATE}.sql
mysqldump \
    --opt \
    --user=root \
    --password \
    --databases $DBNAME \
    --master-data=2  \
    --single-transaction \
    --order-by-primary \
    -r $SQLFILE \

gzip $SQLFILE
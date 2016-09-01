# disk usage warning check

if [ 90 -lt ` df -h  |grep xvda1|  awk '{print $5}'|cut -d '%' -f 1` ]
        then echo 'Disk usage too high on the instance. ' | mail -s'Disk Usage Warning' -b admin@domain.com
fi


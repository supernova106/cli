#!/bin/bash

SUBJECT="WARNING CPU USAGE HIGH"

TO=yourteam@companiesemailcom

MESSAGE=/tmp/messages

echo "#######################" > $MESSAGE


echo "CPU statistics as follows.." >> $MESSAGE


mpstat >> $MESSAGE

echo "#######################" >> $MESSAGE

CPU_USAGE=$(top -b -n1 | awk '/^Cpu/ {print $2}' | cut -d. -f1)

[ $CPU_USAGE -gt 75 ] && mail -s "$SUBJECT" "$TO" < $MESSAGE


#!/bin/sh

N_ACCOUNTS=10
i=1

while [ $i -lte $N_ACCOUNTS ]
do
  echo "Creating Account #$i"
  ((i++))
  
  ./ig-adb-bot/aws/blank/create.sh
done
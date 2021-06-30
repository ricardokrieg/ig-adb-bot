#!/bin/sh

N_ACCOUNTS=10
i=0

while [ $i -lt $N_ACCOUNTS ]
do
  echo "Creating Account #$((i + 1))"
  ((i++))
  
  ./ig-adb-bot/aws/travel/create.sh
done
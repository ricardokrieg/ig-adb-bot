#!/bin/sh

N_ACCOUNTS=2
i=0

while [ $i -lt $N_ACCOUNTS ]
do
  echo "Creating Account #$((i + 1))"
  ((i++))
  
  ./ig-adb-bot/aws/cat/create.sh
done
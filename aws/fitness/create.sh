#!/bin/sh

OUTPUT=$(aws ec2 run-instances \
    --image-id ami-0ccf2d40012a1d067 \
    --count 1 \
    --instance-type t3.small \
    --key-name ricardo_aws \
    --security-group-ids sg-06c24e62aa6a8e8b2 \
    --output text \
    --query 'Instances[0].[InstanceId,PrivateIpAddress]')

INSTANCE_ID=$(echo "${OUTPUT}" | cut -f1)
PRIVATE_IP_ADDRESS=$(echo "${OUTPUT}"| cut -f2)

echo "InstanceId = ${INSTANCE_ID}"
echo "PrivateIpAddress = ${PRIVATE_IP_ADDRESS}"

echo Installing on ${INSTANCE_ID}...
sh ./ig-adb-bot/aws/fitness/install.sh ${INSTANCE_ID} ${PRIVATE_IP_ADDRESS}
echo Done!

echo Sign up on ${INSTANCE_ID}
python3 ./ig-adb-bot/signup_fitness.py ${PRIVATE_IP_ADDRESS}:5555
echo Done!

echo Shutting down ${INSTANCE_ID}
aws ec2 terminate-instances --instance-ids ${INSTANCE_ID}
#!/bin/bash

exec &> >( logger -t gjallarhorn )

source /home/ubuntu/.aws.env
##################################################
# /home/ubuntu/.aws.env must contain the following lines:
#export AWS_ACCESS_KEY_ID=xxxxxx
#export AWS_SECRET_ACCESS_KEY=xxxxxxxxx
#export KORGHALLA_ID=i-0c7d6f6653d1fd188
##################################################


#check if powered off/on
STOPPED=$(aws ec2 describe-instances \
	--instance-ids $KORGHALLA_ID \
	--filters Name=instance-state-code,Values=80 \
	--output text \
	| grep -o stopped)


#if powered off, power it on
if [ ! -z $STOPPED ]; then
	echo "It appears Korghalla has fallen, rebuilding."
	aws ec2 start-instances --instance-ids $KORGHALLA_ID
else
	echo "Korghalla is alive and well warrior."
fi

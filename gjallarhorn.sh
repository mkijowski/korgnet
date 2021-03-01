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
check_status() 
{
	STATUS=$(aws ec2 describe-instances \
		--instance-ids $KORGHALLA_ID \
		--query "Reservations[*].Instances[*].[State.Name]" \
		--o text)
	echo $STATUS
}

boot()
{

	STATUS=$(check_status)
	#if powered off, power it on
	if [ $STATUS == "stopped" ]; then
		echo "It appears Korghalla has fallen, rebuilding."
		aws ec2 start-instances --instance-ids $KORGHALLA_ID
	else
		echo "Korghalla is alive and well warrior."
	fi
}

boot


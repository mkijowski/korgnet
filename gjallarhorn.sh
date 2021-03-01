#!/bin/bash

#exec &> >( logger -t gjallarhorn )

source /home/ubuntu/.aws.env
##################################################
# /home/ubuntu/.aws.env must contain the following lines:
#export AWS_ACCESS_KEY_ID=xxxxxx
#export AWS_SECRET_ACCESS_KEY=xxxxxxxxx
#export KORGHALLA_ID=i-0c7d6f6653d1fd188
##################################################


#check if powered off/on
get_state() 
{
	STATUS=$(aws ec2 describe-instances \
		--instance-ids $KORGHALLA_ID \
		--query "Reservations[*].Instances[*].[State.Name]" \
		--o text)
	echo $STATUS
}


boot()
{
	STATE=$(get_state)
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo "It appears Korghalla has fallen, rebuilding."
		aws ec2 start-instances --instance-ids $KORGHALLA_ID
	else
		echo "Korghalla is alive and well warrior."
	fi
}

check_status()
{
	STATE=$(get_state)
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo 'The ring of Gramr falls dead in the air, it appears Korghalla has fallen. Sound the mighty `!gjallarhorn` to rebuild.'
	elif [ $STATE == "running" ]; then
		STATUS=$(ssh 10.0.0.25 -f  'sudo systemctl status valheimserver.service |grep -o running')
		if [ $STATUS == "running" ]; then
			echo "A cheer echoes in the air, warriors of Korghalla beckon you to join them!"
		else
			echo "Something terrible is wrong.  Get Ikorg some mead stat!"
		fi
	else
		echo "Loki must be playing tricks on us, Korghalla is hidden in the mysts!"
	fi

}

$@


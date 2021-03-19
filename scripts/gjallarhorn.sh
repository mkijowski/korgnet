#!/bin/bash

exec &> >( logger -t gjallarhorn )

source /home/ubuntu/.aws.env
##################################################
# /home/ubuntu/.aws.env must contain the following lines:
#export AWS_ACCESS_KEY_ID=xxxxxx
#export AWS_SECRET_ACCESS_KEY=xxxxxxxxx
export KORGHALLA_ID=i-0c7d6f6653d1fd188
export PWNIE_ID=i-0d33da4eb27c121f0
##################################################

testme()
{
	STATE=$(get_state $KORGHALLA_ID)
	echo $STATE
}
export -f testme

#check if powered off/on
get_state() 
{
	STATUS=$(/usr/local/bin/aws ec2 describe-instances \
		--instance-ids $1 \
		--query "Reservations[*].Instances[*].[State.Name]" \
		--o text)
	echo $STATUS
}
export -f get_state

boot()
{
	STATE=$(get_state $KORGHALLA_ID)
	echo $STATE
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo "It appears Korghalla has fallen, rebuilding."
		/usr/local/bin/aws ec2 start-instances --instance-ids $KORGHALLA_ID
	else
		echo "Korghalla is alive and well warrior."
	fi
}
export -f boot

mlpboot()
{
	STATE=$(get_state $PWNIE_ID)
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo "Waking up the Pwnies."
		/usr/local/bin/aws ec2 start-instances --instance-ids $PWNIE_ID
	else
		echo "The pwnies are happy."
	fi
}
export -f mlpboot

check_status()
{
	STATE=$(get_state $KORGHALLA_ID)
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo 'The ring of Gramr falls dead in the air, it appears Korghalla has fallen. Sound the mighty `!gjallarhorn` to rebuild.'
	elif [ $STATE == "running" ]; then
		STATUS=$(ssh 10.0.0.25 -f  'sudo systemctl status valheimserver.service' | grep -o running)
		if [ $STATUS == "running" ]; then
			echo "A cheer echoes in the air, warriors of Korghalla beckon you to join them!"
		else
			echo "Something terrible is wrong.  Get Ikorg some mead stat!"
		fi
	else
		echo "Loki must be playing tricks on us, Korghalla is hidden in the mysts!"
	fi
}
export -f check_status

check_mlp_status()
{
	STATE=$(get_state $PWNIE_ID)
	#if powered off, power it on
	if [ $STATE == "stopped" ]; then
		echo 'Quiet. `!redpill` to free your mind'
	elif [ $STATE == "running" ]; then
		echo "Hopefully we are up and running!"
		#STATUS=$(ssh 10.0.0.25 -f  'sudo systemctl status valheimserver.service |grep -o running')
		#if [ $STATUS == "running" ]; then
		#	echo "A cheer echoes in the air, warriors of Korghalla beckon you to join them!"
		#else
		#	echo "Something terrible is wrong.  Get Ikorg some mead stat!"
		#fi
	else
		echo "Get to an exit, something is wrong!"
	fi
}
export -f mlp_status

$@

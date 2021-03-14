#!/bin/bash

##enable logging
exec &> >( logger -t korgnarok )

echo "Starting Korgnarok!"

FILES_TO_BACKUP=("/home/steam/.config/unity3d/IronGate/Valheim/worlds/Korghalla.db" \
        "/home/steam/.config/unity3d/IronGate/Valheim/worlds/Korghalla.fwl")

BACKUP_LOCATION=("/home/korghalla")
TIMESTAMP=$(date +%F_%R)

update ()
{
	echo "updating"
	git -C /home/ubuntu/git/korgnet
}

backup ()
{
echo "Backup and restart triggered $TIMESTAMP, stopping valheim."
sudo systemctl stop valheimserver.service
sleep 1m

echo "Backing up world files"
for FILE in ${FILES_TO_BACKUP[@]}; do
        FILENAME=$(echo $FILE | gawk -F / '{print $NF}')
        cp $FILE "$BACKUP_LOCATION/$FILENAME.$TIMESTAMP"
done
}

resume ()
{
sleep 30s
echo " Starting valheim service"
sudo systemctl start valheimserver.service
}

packet_monitor ()
{
        threshold=1000
        rx=$(cat /sys/class/net/eth0/statistics/rx_packets)
        sleep 5m
        rxnew=$(cat /sys/class/net/eth0/statistics/rx_packets)

        received="$(($rxnew-$rx))"

        if [ $received -lt $threshold ] && [ $1 -lt $threshold ]; then
                echo "No sounds in the halls of Korghalla, Korgnarok take us!"
                update && backup && sudo shutdown now || echo "Backup unsuccessful, Korghalla is in danger!"
        else
                echo "Korghalla rings with the sounds of battle!"
                packet_monitor $received
        fi
}

cleanup ()
{


}

# start packet monitor and pass it an arbitrary amount of packets
packet_monitor 1001

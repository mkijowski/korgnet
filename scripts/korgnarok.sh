#!/bin/bash

##enable logging
exec &> >( logger -t valheim )

FILES_TO_BACKUP=("/home/steam/.config/unity3d/IronGate/Valheim/worlds/Korghalla.db" \
	"/home/steam/.config/unity3d/IronGate/Valheim/worlds/Korghalla.fwl")

BACKUP_LOCATION=("/home/korghalla")
TIMESTAMP=$(date +%F_%R)

echo "Backup and restart triggered $TIMESTAMP, stopping valheim."

sudo systemctl stop valheimserver.service

sleep 1m

echo "Backing up world files"
for FILE in ${FILES_TO_BACKUP[@]}; do
	FILENAME=$(echo $FILE | gawk -F / '{print $NF}')
	cp $FILE "$BACKUP_LOCATION/$FILENAME.$TIMESTAMP"
done

sleep 1m

echo " Starting valheim service"
sudo systemctl start valheimserver.service


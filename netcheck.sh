#!/bin/bash

HOST=10.0.0.25
PORT=22

nc -4 -d -z -w 1 $HOST $PORT &> /dev/null
if [[ $? == 0 ]]
then
    # Port is reached
    echo "Korghalla is online!"
    ssh 10.0.0.25 -f  'sudo systemctl status valheimserver.service'
    exit 0
else
    # Port is unreachable
    echo "Korghalla is offline!"
    exit 1
fi

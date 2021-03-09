#!/bin/bash

#enable logging
exec &> >( logger -t discord )

echo "Launching Korgbot."

/opt/anaconda3/bin/python /home/ubuntu/git/korgnet/korgbot.py


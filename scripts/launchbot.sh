#!/bin/bash

#enable logging
exec &> >( logger -t discord )

echo "Launching Korgbot."

python /home/ubuntu/git/korgnet/korgbot.py

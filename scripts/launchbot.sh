#!/bin/bash

#enable logging
exec &> >( logger -t discord )

echo "Launching Korgbot."

cd /home/ubuntu/git/korgnet && /home/ubuntu/git/korgnet/korgbot.py

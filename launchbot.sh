#!/bin/bash

#enable logging
exec &> >( logger -t discord )

/home/ubuntu/git/korgnet/korgbot.py

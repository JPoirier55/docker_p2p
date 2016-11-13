#!/bin/bash

#ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'

echo $INSTANCE


#python /docker_p2p/scripts/server.py --serverip

#!/bin/bash

type=$1
version=$2
if [ "$type" = "ams" ]
then
	for i in A88 A88GD S88 T88 D88 G88 D89;do time python3 /opt/scripts/ios_automatic_sign/entrypoint.py -P $i -M $type -V 3.1.$version;done
elif [ "$type" = "game" ]
then
	for i in A88 A89 A88GD S88 T88 D88 G88 D89;do time python3 /opt/scripts/ios_automatic_sign/entrypoint.py -P $i -M $type -V 3.0.$version;done
fi
		

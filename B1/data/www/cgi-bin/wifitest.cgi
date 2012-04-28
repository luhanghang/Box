#!/bin/sh
echo ""
host=`grep host /etc/mg.conf|cut -d= -f2`
result=`ping -W 1 -w 1 $host|grep ttl -c`
if [ $result == 0 ]; then
	echo "Failure"
else
	echo "Success"
fi

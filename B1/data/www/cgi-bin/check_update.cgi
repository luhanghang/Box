#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
#server='124.206.31.62'
v_conf=`cat /etc/version`
c_version=`echo $v_conf|awk '{print $1}'`
c_ver=`echo $c_version|cut -d. -f1,2`
echo "$c_version $server" > /etc/version
new_version=`curl -m 1 -s http://$server/$c_ver.txt`
new_ver=`echo $new_version|cut -d. -f1,2`
echo
if [ "$new_ver" == "$c_ver" ]; then
	echo $new_version
else
	echo -1
fi

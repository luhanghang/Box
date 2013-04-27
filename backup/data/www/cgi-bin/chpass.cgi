#!/bin/sh
cpass=`cat /etc/httpd.conf|cut -d: -f3`
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

case $lan in
	1)
		. ../lan/set_strings_1
	;;
	3)
		. ../lan/set_strings_3
	;;
	*)
		. ../lan/set_strings_2
esac

echo ""
if [ -z ${curpass} ] || [ ${cpass} != ${curpass} ]; then
	echo $s30
else
	pass=`echo $newpass|grep '^[A-Za-z0-9]*$'`
	if [ -z ${pass} ]; then
		echo $s31
	else
		tmp=`httpd -d $newpass`
		echo "admin:$newpass" > /etc/.httpdpasswd
		echo $s32
	fi
fi
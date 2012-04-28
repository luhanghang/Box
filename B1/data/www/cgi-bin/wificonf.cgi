#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
case $index in
	1)
		echo ""
		echo `iwlist ra0 scanning|grep ESSID|awk -F: '{print $2}'|tr -d \"`	
		exit 
	;;
esac

if [ -f "/etc/wificonf/recent" ]; then
	exists=`grep -c $ESSID /etc/wificonf/recent`
	if [ $exists == 0 ]; then
		echo $ESSID > /etc/wificonf/recent
	fi  
else
	echo $ESSID > /etc/wificonf/recent
fi

echo $ESSID > /etc/wificonf/current
echo "AuthMode=$AuthMode" > /etc/wificonf/$ESSID
echo "EncrypType=$EncrypType" >> /etc/wificonf/$ESSID
echo "passwd=$passwd" >> /etc/wificonf/$ESSID
echo "ip=$ip" >> /etc/wificonf/$ESSID
echo "mask=$mask" >> /etc/wificonf/$ESSID
echo "gateway=$gateway" >> /etc/wificonf/$ESSID
echo "dhcp=$dhcp" >> /etc/wificonf/$ESSID

iwpriv ra0 set NetworkType=Infra
iwpriv ra0 set AuthMode=$AuthMode
iwpriv ra0 set EncrypType=$EncrypType
iwpriv ra0 set SSID="$ESSID"
if [ $EncrypType == 'WEP' ]; then
	iwpriv ra0 set DefaultKeyID=1
	iwpriv ra0 set Key1="$passwd"
fi

if [ $EncrypType == 'WPAPSK' ] || [ $EncrypType == 'AES' ] || [ $EncrypType == 'TKIP' ]; then
	iwpriv ra0 set WPAPSK="$passwd"
fi

if [ "$dhcp" == "1" ]; then
	if [ -f "/tmp/udhcpc.pid" ]; then
		kill -9 `cat /tmp/udhcpc.pid`
	fi
	udhcpc -b -i ra0 -p /tmp/udhcpc.pid
	ip=`grep ip= /var/lib/misc/udhcpd.leases|cut -d= -f2`
	mask=`grep mask= /var/lib/misc/udhcpd.leases|cut -d= -f2`
	gateway=`grep gateway= /var/lib/misc/udhcpd.leases|cut -d= -f2`
else
	ifconfig ra0 inet $ip netmask $mask
	route delete default
	route add default gw $gateway ra0
fi

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

if [ $status == 1 ]; then
	status=$s91
else
	status=$s90
fi

essid=`iwconfig ra0|grep ESSID|awk -F"ESSID:" '{print $2}'|awk '{print $1}'|tr -d \"`

echo Content-type: text/html
echo ""
/bin/cat << EOM
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
	<script type="text/javascript" src="/javascripts/wifi.js"></script>                                              
	            <script type="text/javascript" src="/javascripts/jquery.js"></script>
	<title></title>
</head>
<body>
	<div>Wifi: $ESSID </div>
	<hr size="1">
	<table width="100%">
		<tr>
			<td width="150">
				$s95
			</td>
			<td>
				$AuthMode
			</td>
		</tr>
		<tr>
			<td>
				$s96
			</td>
			<td>
				$EncrypType
			</td>
		</tr>
		<tr>
			<td>
				$s23
			</td>
			<td>
				$passwd
			</td>
		</tr>
		<tr>
			<td>
				$s9
			</td>
			<td>
				$ip
			</td>
		</tr>
		<tr>
			<td>
				$s10
			</td>
			<td>
				$mask
			</td>
		</tr>
		<tr>
			<td>
				$s98
			</td>
			<td>
				$gateway
			</td>
		</tr>
	</table>
	</div>
	<hr size="1"/>
	<input type="button" value="test" onclick="test_connection()"/>
</body>
</html>


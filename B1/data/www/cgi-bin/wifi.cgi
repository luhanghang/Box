#!/bin/sh

#read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

case $index in
	1)
		ifconfig ra0 up	
	;;
esac

status=`ifconfig|grep ra0 -c`

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
	button="<input type='button' value='$s93' id="searchap" onclick='search_ap()'>"
else
	status=$s90
	button="<input type='submit' value='$s92'>"
fi

if [ -f "/etc/wificonf/current" ]; then
	essid=`cat /etc/wificonf/current`
fi
if [ "$essid" != "" ]; then
	auth=`grep AuthMode= /etc/wificonf/$essid|cut -d= -f2`
	case $auth in
		"OPEN")
			auth_0="selected"
		;;
		"SHARED")
			auth_1="selected"
		;;
		"WEPAUTO")
			auth_2="selected"
		;;
		"WPAPSK")
			auth_3="selected"
		;;
		"WPANONE")
			auth_4="selected"
		;;
		"WPA2PSK")
			auth_5="selected"
		;;
	esac
	encrypt=`grep EncrypType= /etc/wificonf/$essid|cut -d= -f2`
	case $encrypt in
		"NONE")
			encrypt_0="selected"
		;;
		"WEP")
			encrypt_1="selected"
		;;
		"AES")
			encrypt_2="selected"
		;;
		"WPA2PSK")
			encrypt_3="selected"
		;;
		"TKIP")
			encrypt_4="selected"
		;;
	esac
	
	passwd=`grep passwd= /etc/wificonf/$essid|cut -d= -f2`
	
	dhcp_checked=" checked"
	manual_checked=""
	dhcp=`grep dhcp= /etc/wificonf/$essid|cut -d= -f2`
	if [ "$dhcp" != "1" ]; then
		dhcp_checked=""
		manual_checked=" checked"
	fi
	if [ "$dhcp_checked" == " checked" ]; then
		ip=`grep ip= /var/lib/misc/udhcpd.leases|cut -d= -f2`
		mask=`grep mask= /var/lib/misc/udhcpd.leases|cut -d= -f2`
		gateway=`grep gateway= /var/lib/misc/udhcpd.leases|cut -d= -f2`
	else
		ip=`grep ip= /etc/wificonf/$essid|cut -d= -f2`
		mask=`grep mask= /etc/wificonf/$essid|cut -d= -f2`
		gateway=`grep gateway= /etc/wificonf/$essid|cut -d= -f2`
	fi
fi

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
	<form id="form1" method="get" action="/cgi-bin/wifi.cgi">
		<input type="hidden" value="1" name="index">
		<input type="hidden" value="$lan" name="lan">
	<div>Wifi <span id="wifistatus">$status</span><span style="margin-left:20px">$button</span></span></div>
	</form>
	<hr size="1">
	<form id="form2" action="/cgi-bin/wificonf.cgi" method="post">
	<input type="hidden" name="index" value="2">
	<input type="hidden" value="$lan" name="lan">
	<div id="chooseap">
	<table width="100%">
		<tr>
			<td width="150">
				$s94
			</td>
			<td>
				<select id="essid" name="ESSID">
					<option>$essid</option>
				</select>	
			</td>
		</tr>
		<tr>
			<td>
				$s95
			</td>
			<td>
				<select name="AuthMode">
					<option $auth_0>OPEN</option>
					<option $auth_1>SHARED</option>
					<option $auth_2>WEPAUTO</option>
					<option $auth_3>WPAPSK</option>
					<option $auth_4>WPANONE</option>
					<option $auth_5>WPA2PSK</option>
				</select>
			</td>
		</tr>
		<tr>
			<td>
				$s96
			</td>
			<td>
				<select name="EncrypType">
					<option $encrypt_0>NONE</option>
					<option $encrypt_1>WEP</option>
					<option $encrypt_2>AES</option>
					<option $encrypt_3>WPA2PSK</option>
					<option $encrypt_4>TKIP</option>
				</select>
			</td>
		</tr>
		<tr>
			<td>
				$s23
			</td>
			<td>
				<input type="text" size="20" name="passwd" value="$passwd">
			</td>
		</tr>
		<tr>
			<td>
				TCP/IP
			</td>
			<td>
				<input type="radio" name="dhcp" value="1"$dhcp_checked>DHCP 
				<input type="radio" name="dhcp" value="0"$manual_checked>$s106
			</td>
		</tr>
		<tr>
			<td>
				$s9
			</td>
			<td>
				<input type="text" size="20" name="ip" value="$ip">
			</td>
		</tr>
		<tr>
			<td>
				$s10
			</td>
			<td>
				<input type="text" size="20" name="mask" value="$mask">
			</td>
		</tr>
		<tr>
			<td>
				$s98
			</td>
			<td>
				<input type="text" size="20" name="gateway" value="$gateway">
			</td>
		</tr>
	</table>
	</div>
	<hr size="1">
	<input type="submit" value="$s97"> &nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="Test" onclick="test_connection()"/>
	</form>
</body>
</html>


#!/bin/sh
eth0=`ifconfig eth0 | head -n 5|tr "\n" " "|awk '{print $5,$7,$9,$17,$23}'|sed 's/addr://g'|sed 's/Mask://g'|sed 's/packets://g'`
mac0=$(echo $eth0|awk '{print $1}')
ip0=$(echo $eth0|awk '{print $2}')
mask0=$(echo $eth0|awk '{print $3}')
rev0=$(echo $eth0|awk '{print $4}')
sent0=$(echo $eth0|awk '{print $5}')

dns=`cat /etc/resolv.conf|awk '{print $2}'|tr "\n" " "`
speed=`fwstate|awk '{print $8,$9,$10,$11}`
lev0=0
lev1=0
csq0_l='65'
csq1_l='65'

csq0='N/A'
#if [ -f "/tmp/path1-1" ]; then
	#path=`cat /tmp/path1-1`
	path="/sys/devices/platform/ep93xx-ohci/usb1/1-1"
	card0=`find $path|grep ttyUSB|sort|head -n1`
	if [ -n "$card0" ]; then
		l=`echo "$card0"|awk '{print length($0)}'`
		min=`echo "$card0"|cut -c$l-$l`
		offset=2
		product=`cat /tmp/product1-1`                                           
		dial_conf=`grep "$product" /etc/dial_conf`
		if [ -n ${product} ] && [ -n ${dial_conf} ]; then
			offset=`echo $dial_conf|awk '{print $5}'`   
		fi                   
		min=$(expr $min '+' $offset)
		csq0=`3gstate -p /dev/ttyUSB$min|cut -d, -f1|awk '{print $2}'`
		if [ -z $csq0 ]; then
			csq0=$csq0_l
			lev0=$(expr $csq0 '/' 20)
			csq0="$csq0%"
		else
			if [ $csq0 == 99 ]; then
				csq0='No Signal'
			else
				csq0=$(expr $csq0 '*' 100 '/' 32)
				csq0_l=$csq0
				lev0=$(expr $csq0 '/' 20)
				csq0="$csq0%"
			fi
		fi
	fi
#fi

csq1='N/A'
#if [ -f "/tmp/path1-3" ]; then
	#path=`cat /tmp/path1-3`
	path="/sys/devices/platform/ep93xx-ohci/usb1/1-3"
	card1=`find $path|grep ttyUSB|sort|head -n1`
	if [ -n "$card1" ]; then
		l=`echo "$card1"|awk '{print length($0)}'`
		offset=2
		min=`echo "$card1"|cut -c$l-$l`
		product=`cat /tmp/product1-3`                                           
		dial_conf=`grep "$product" /etc/dial_conf`
		if [ -n ${product} ] && [ -n ${dial_conf} ]; then 
			offset=`echo $dial_conf|awk '{print $5}'`
		fi                      
		min=$(expr $min '+' $offset)
		csq1=`3gstate -p /dev/ttyUSB$min|cut -d, -f1|awk '{print $2}'`
	
		if [ -z $csq1 ]; then
			csq1=$csq1_l
			lev1=$(expr $csq1 '/' 20)
			csq1="$csq1%"
		else
			if [ $csq1 == 99 ]; then
				csq1='No Signal'
			else
				csq1=$(expr $csq1 '*' 100 '/' 32)
				csq1_l=$csq1
				lev1=$(expr $csq1 '/' 20)
				csq1="$csq1%"
			fi
		fi
	fi
#fi

#status="{eth0:'$eth0',dns:'$dns',speed:'$speed',csq0:'$csq0', csq1:'$csq1'"

ppp0=`ifconfig|grep ppp0 -c`
online0="<font color='red'>offline</font>"
if [ ${ppp0} == 1 ]; then
	ppp0=`ifconfig ppp0|sed -n '2,$'p|tr ":" " "|tr "\n" " "|awk '{print $3,$5,$7,$46$47,$51$52}''`
	online0="<font color='green'>online</font>"
#	status="$status,ppp0:'$ppp0'"
fi
p0=$(echo $ppp0|awk '{print $1}')
ptp0=$(echo $ppp0|awk '{print $2}')
pmask0=$(echo $ppp0|awk '{print $3}')
in0=$(echo $ppp0|awk '{print $4}')
out0=$(echo $ppp0|awk '{print $5}')

online1="<font color='red'>offline</font>"
ppp1=`ifconfig|grep ppp1 -c`
if [ ${ppp1} == 1 ]; then
	ppp1=`ifconfig ppp1|sed -n '2,$'p|tr ":" " "|tr "\n" " "|awk '{print $3,$5,$7,$46$47,$51$52}'`
	online1="<font color='green'>online</font>"
#	status="$status,ppp1:'$ppp1'"
fi
p1=$(echo $ppp1|awk '{print $1}')
ptp1=$(echo $ppp1|awk '{print $2}')
pmask1=$(echo $ppp1|awk '{print $3}')
in1=$(echo $ppp1|awk '{print $4}')
out1=$(echo $ppp1|awk '{print $5}')

#status="$status}"
#echo
#echo $status
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

echo Content-type: text/html
echo ""
/bin/cat << EOM
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
	<title></title>
</head>
<body>
	<div>$s1</div>
	<hr size="1">
	<div>
		<div>
			<div>
				$s7
			</div>
			<hr size="1">
			<table cellpadding="0" cellspacing="0" width="100%">
				<tr>
					<td class="label">
						$s8
					</td>
					<td class="value">
						<div id="eth0_mac">$mac0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s9
					</td>
					<td class="value">
						<div id="eth0_ip">$ip0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s10
					</td>
					<td class="value">
						<div id="eth0_mask">$mask0</div>	
					</td>
				</tr>
				<tr>
					<td class="label">
						$s11
					</td>
					<td class="value">
						$s12 $rev0 $s14	
					</td>
				</tr>
				<tr>
					<td class="label">
						&nbsp;
					</td>
					<td class="value">
						$s13 $sent0 $s14	
					</td>
				</tr>
			</table>
		</div>
		<hr size="1">
		<div>
			<div>
				$s10
			</div>
			<hr size="1">
			<div>
				ppp0
			</div>
			<hr size="1">
			<table cellpadding="0" cellspacing="0" width="100%">
				<tr>
					<td class="label">
						$s16
					</td>
					<td class="value">
						<img src="/images/level$lev0.gif" border="0" id="img_csq0">
						<span id="csq0" style="margin-left:5px">$csq0</span>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s9
					</td>
					<td class="value">
						<div id="ppp0_ip">$p0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s10
					</td>
					<td class="value">
						<div id="ppp0_mask">$pmask0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s17
					</td>
					<td class="value">
						<div id="ppp0_ptp">$ptp0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s18
					</td>
					<td class="value">
						<div id="ppp0_status">$online0</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s11
					</td>
					<td class="value">
						$s12 <span id="ppp0_rx">$in0</span>	
					</td>
				</tr>
				<tr>
					<td class="label">
						&nbsp;
					</td>
					<td class="value">
						$s13 <span id="ppp0_tx">$out0</span>
					</td>
				</tr>
			</table>
			<hr size="1">
			<div>
				ppp1
			</div>
			<hr size="1">
			<table cellpadding="0" cellspacing="0" width="100%">
				<tr>
					<td class="label">
						$s16
					</td>
					<td class="value">
						<img src="/images/level$lev1.gif" border="0" id="img_csq1">
						<span id="csq1" style="margin-left:5px">$csq1</span>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s9
					</td>
					<td class="value">
						<div id="ppp1_ip">$p1</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s10
					</td>
					<td class="value">
						<div id="ppp1_mask">$pmask1</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s17
					</td>
					<td class="value">
						<div id="ppp1_ptp">$ptp1</div>
					</td>
				</tr>

				<tr>
					<td class="label">
						$s18
					</td>
					<td class="value">
						<div id="ppp1_status">$online1</div>
					</td>
				</tr>
				<tr>
					<td class="label">
						$s11
					</td>
					<td class="value">
						$s12 <span id="ppp1_rx">$in1</span>
					</td>
				</tr>
				<tr>
					<td class="label">
						&nbsp;
					</td>
					<td class="value">
						$s13 <span id="ppp1_tx">$out1</span>
					</td>
				</tr>
			</table>
			<hr size="1">
			<table cellpadding="0" cellspacing="0" width="100%">
				<tr>
					<td class="label">
						$s19
					</td>
					<td class="value">
						<div id="dns">$dns</div>
					</td>
				</tr>
			</table>
			<hr size="1">
			<table cellpadding="0" cellspacing="0" width="100%">
				<tr>
					<td class="label">
						$s21
					</td>
					<td class="value">
						<span id="speed">$speed</span>
					</td>
				</tr>
			</table>	
		</div>
		<div style="margin-top:10px"><input type="button" value="$s20" onclick="window.location.reload()"></div>
	</div>
</body>
</html>


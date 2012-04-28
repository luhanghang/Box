#!/bin/sh
o_ip=`cat /etc/encoder/conf|awk '{print $1}`

do_save() {
	#if [ -z $session ]; then
	#	session=`curl -d @/etc/encoder/encoder_login.xml http://$o_ip/cgi-bin/authen -s|grep session|awk '{print $1}'|cut -d\" -f2`
	#fi
	#xml=`cat /etc/encoder/set_encoder.xml|sed "s/INDEX/$1/g"|sed "s/MODULE/$2/g"|sed "s/SESSION/$session/g"|sed s/PARAS/$3/g`
	#result=`curl -d "$xml" http://$o_ip/cgi-bin/$2 -s|grep Succeed -c`
	#if [ $result == 1 ]; then
	#	xml=`cat /etc/encoder/save_encoder.xml|sed "s/SESSION/$session/g"`
	#	result=`curl -d "$xml" http://$o_ip/cgi-bin/baseinfo -s|grep Succeed -c`
	#fi
	result="OK"
}


read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
case $index in
	0)
		#eth0_ip=`httpd -d $eth0_ip`
		r=`./valid_ip $eth0_ip`
		if [ $r != 0 ]; then
			error="eth0_ip"
		fi
		#eth0_mask=`httpd -d $eth0_mask`
		r=`./valid_ip $eth0_mask`
		if [ $r != 0 ]; then
			error="$error:eth0_mask"
		fi
		if [ -z ${error} ]; then
			paras="\<videoEncode\>\<index\>1\<\/index\>\<remoteIp\>$eth0_ip\<\/remoteIp\>\<\/videoEncode\>"
			do_save 1 "udpsession" $paras
			if [ $result == 0 ]; then
				echo "failure"
			else
				echo "$eth0_ip $eth0_mask" > /etc/netconf
			fi
		fi
	;;
	1)
		ppp0_dial=`httpd -d $ppp0_dial`
		ppp0_apn=`httpd -d $ppp0_apn`
		if [ -n "$ppp0_user" ]; then
			ppp0_user=`httpd -d $ppp0_user`
		fi
		if [ -n "$ppp0_passwd" ]; then
			ppp0_passwd=`httpd -d $ppp0_passwd`
		fi	
		sed "s/user \".*\"/user \"$ppp0_user\"/g" /etc/ppp/peers/wcdma0|sed "s/password \".*\"/password \"$ppp0_passwd\"/g" > /etc/ppp/peers/w.tmp
		cp /etc/ppp/peers/w.tmp /etc/ppp/peers/wcdma0
		sed "s/user \".*\"/user \"$ppp0_user\"/g" /etc/ppp/peers/evdo0|sed "s/password \".*\"/password \"$ppp0_passwd\"/g" > /etc/ppp/peers/e.tmp
		cp /etc/ppp/peers/e.tmp /etc/ppp/peers/evdo0
		sed "s/OK-AT-OK \"ATDT.*\"/OK-AT-OK \"ATDT$ppp0_dial\"/g" /etc/ppp/chat-wcdma.tmp|sed "s/\"IP\"\,\".*\"/\"IP\"\,\"$ppp0_apn\"/g"> /etc/ppp/chat-wcdma
		standard1=`cat /etc/ppp/standard|grep 1=`
		echo "0=$standard0" > /etc/ppp/standard
		echo $standard1 >> /etc/ppp/standard
	;;
	2)
		ppp1_dial=`httpd -d $ppp1_dial`
		ppp1_apn=`httpd -d $ppp1_apn`
		if [ -n "$ppp1_user" ]; then
			ppp1_user=`httpd -d $ppp1_user`
		fi
		if [ -n "$ppp1_passwd" ]; then
			ppp1_passwd=`httpd -d $ppp1_passwd`
		fi
	
		sed "s/user \".*\"/user \"$ppp1_user\"/g" /etc/ppp/peers/wcdma1|sed "s/password \".*\"/password \"$ppp1_passwd\"/g" > /etc/ppp/peers/w1.tmp
		cp /etc/ppp/peers/w1.tmp /etc/ppp/peers/wcdma1
		sed "s/user \".*\"/user \"$ppp1_user\"/g" /etc/ppp/peers/evdo1|sed "s/password \".*\"/password \"$ppp1_passwd\"/g" > /etc/ppp/peers/e1.tmp
		cp /etc/ppp/peers/e1.tmp /etc/ppp/peers/evdo1
	
		sed "s/OK-AT-OK \"ATDT.*\"/OK-AT-OK \"ATDT$ppp1_dial\"/g" /etc/ppp/chat-wcdma-1.tmp|sed "s/\"IP\"\,\".*\"/\"IP\"\,\"$ppp1_apn\"/g"> /etc/ppp/chat-wcdma-1
		standard0=`cat /etc/ppp/standard|grep 0=`
		echo $standard0 > /etc/ppp/standard
		echo "1=$standard1" >> /etc/ppp/standard
	;;
	3)
		host=`httpd -d $host`
		#local_port=`httpd -d $local_port`
		destination_port=`httpd -d $destination_port`
		tcp=`httpd -d $tcp`
		#uuid=`httpd -d $uuid`
		encaddr=`cat /etc/mg.conf|grep encaddr=|cut -d= -f2`
		if [ "$encaddr" == "" ]; then
			encaddr="192.168.1.12";
		fi
		paras="\<videoEncode\>\<index\>1\<\/index\>\<remotePort\>$local_port\<\/remotePort\>\<\/videoEncode\>"
		do_save 1 "udpsession" $paras
		if [ $result == 0 ]; then
			echo "failure"
		else
			#buffer=`grep buffer /etc/mg.conf`
			echo "host=$host">/etc/mg.conf
			echo "local_port=6008">>/etc/mg.conf
			echo "destination_port=$destination_port">>/etc/mg.conf
			echo "tcp=$tcp">>/etc/mg.conf
			#echo "uuid=$uuid">>/etc/mg.conf
			echo "buffer=$buffer">>/etc/mg.conf
			echo "rate_min=$rate_min">>/etc/mg.conf
			echo "rate_max=$rate_max">>/etc/mg.conf
			echo "encaddr=$encaddr">>/etc/mg.conf
			echo "encport=6180">>/etc/mg.conf
		fi
	;;
	4)
		conf=`cat /etc/encoder/conf`
		o_mask=`echo $conf|awk '{print $2}'`
		o_fs=`echo $conf|awk '{print $3}'`
		o_br=`echo $conf|awk '{print $4}'`
		o_kf=`echo $conf|awk '{print $5}'`
		o_fr=`echo $conf|awk '{print $6}'`
		o_p=`echo $conf|awk '{print $7}'`
		o_s=`echo $conf|awk '{print $8}'`
		echo "$encoder $o_mask $o_fs $o_br $o_kf $o_fr $o_p $o_s" > /etc/encoder/conf
	;;
	11)
		echo "$trans" > /etc/trans
	;;
esac
echo "$error"

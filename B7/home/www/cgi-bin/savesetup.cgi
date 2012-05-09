#!/bin/sh
encaddr='192.168.240.12'
encport=6180
o_ip=`cat /etc/encoder/conf|awk '{print $1}'`

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
echo ""
case $index in
	0)
		#eth1_ip=`httpd -d $eth1_ip`
		r=`./valid_ip $eth1_ip`
		if [ $r != 0 ]; then
			error="eth1_ip"
		fi
		#eth1_mask=`httpd -d $eth1_mask`
		r=`./valid_ip $eth1_mask`
		if [ $r != 0 ]; then
			error="$error:eth1_mask"
		fi
		
		if [ -z ${error} ]; then
			if [ $result == 0 ]; then
				echo "failure"
			else
				echo "$eth1_ip" > /etc/netconf
				echo "$eth1_mask" >> /etc/netconf
				echo "$eth1_gateway" >> /etc/netconf
			fi
		fi
	;;
	3)
		host=`httpd -d $host`
		local_port='6008'
		destination_port=`httpd -d $destination_port`
		tcp=`httpd -d $tcp`
		#uuid=`httpd -d $uuid`
		encaddr=`cat /etc/mg.conf|grep encaddr=|cut -d= -f2`
		if [ "$encaddr" == "" ]; then
			encaddr="192.168.240.12";
		fi
		
		paras="\<videoEncode\>\<index\>1\<\/index\>\<remotePort\>$local_port\<\/remotePort\>\<\/videoEncode\>"
		do_save 1 "udpsession" $paras
		if [ $result == 0 ]; then
			echo "failure"
		else
			#buffer=`grep buffer /etc/mg.conf`
			echo "host=$host">/etc/mg.conf
			echo "local_port=$local_port">>/etc/mg.conf
			echo "destination_port=$destination_port">>/etc/mg.conf
			echo "tcp=$tcp">>/etc/mg.conf
			#echo "uuid=$uuid">>/etc/mg.conf
			echo "buffer=$buffer">>/etc/mg.conf
			echo "transmit=$t_method">>/etc/mg.conf
			echo "rate_min=$rate_min">>/etc/mg.conf
			echo "rate_max=$rate_max">>/etc/mg.conf
			echo "encaddr=$encaddr">>/etc/mg.conf
			echo "encport=6180">>/etc/mg.conf
			killall fw_client
			killall fw_server
			#if [ "$t_method" == "4" ]; then
				/usr/sbin/encoder_params $encaddr $encport 3 "enc0.stream_url=|"
			#else
				#result=`/usr/sbin/encoder_params $encaddr $encport 3 "enc0.stream_url=rtp://$host:$destination_port|"`
			#fi
		fi
	;;
	11)
		echo "$trans" > /etc/trans
	;;
esac
echo "$error"

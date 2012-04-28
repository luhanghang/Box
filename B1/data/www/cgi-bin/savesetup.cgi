#!/bin/sh
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
		
		if [ -z ${error} ]; then
			if [ $result == 0 ]; then
				echo "failure"
			else
				sed -i "s/CONFIG_NETWORK_IPADDR=.*/CONFIG_NETWORK_IPADDR=\"$eth1_ip\"/" /etc/sysconfig/config
				sed -i "s/CONFIG_NETWORK_GATEWAY_IPADDR=.*/CONFIG_NETWORK_GATEWAY_IPADDR=\"$eth1_gateway\"/" /etc/sysconfig/config
			fi
		fi
	;;
	3)
		host=`httpd -d $host`
		local_port='6008'
		destination_port=`httpd -d $destination_port`
		tcp=`httpd -d $tcp`
		
		echo "host=$host">/etc/mg.conf
		echo "local_port=$local_port">>/etc/mg.conf
		echo "destination_port=$destination_port">>/etc/mg.conf
		echo "tcp=$tcp">>/etc/mg.conf
		echo "buffer=$buffer">>/etc/mg.conf
		echo "rate_min=$rate_min">>/etc/mg.conf
		echo "rate_max=$rate_max">>/etc/mg.conf
		/usr/sbin/encoder_params 127.0.0.1 6180 3 "enc0.stream_url=rtp://$host:$destination_port|"
	;;
esac
echo "$error"

#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

if [ "$encaddr" == "" ]; then
	encaddr="192.168.1.12";
fi

encport=`cat /etc/mg.conf|grep encport=|cut -d= -f2`
if [ "$encport" == "" ]; then
	encport="6180";
fi


case $index in
	0)
		if [ `grep -c encaddr /etc/mg.conf` == 0 ]; then
			echo "encaddr=$encaddr">>/etc/mg.conf
		fi
		if [ `grep -c encport /etc/mg.conf` == 0 ]; then
			echo "encport=$encport">>/etc/mg.conf
		fi
		reactive=0
		if [ $old_vidin != $vidin ] || [ $old_audrate != $audrate ] || [ $old_aud_sample_rate != $aud_sample_rate ] || [ $old_res != $vidres ]; then
			reactive=1
		fi
		sed -i "s/encaddr=.*/encaddr=$encaddr/g" /etc/mg.conf
		/usr/sbin/encoder_params $encaddr $encport 3 "enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_res=$vidres|" $reactive
	;;
esac
echo ""

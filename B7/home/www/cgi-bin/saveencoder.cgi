#!/bin/sh
encaddr='192.168.240.12'
encport=6180
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
case $index in
	0)
         reactive=0
         if [ $old_vidin != $vidin ] || [ $old_audrate != $audrate ] || [ $old_aud_sample_rate != $aud_sample_rate ] || [ $old_res != $vidres ]; then
              reactive=1
         fi
         /usr/sbin/encoder_params $encaddr $encport 3 "enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_mode=$vidres|" $reactive
         #/usr/sbin/encoder_params $encaddr $encport 3 "enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_res=$vidres|" $reactive
	;;
esac
echo ""

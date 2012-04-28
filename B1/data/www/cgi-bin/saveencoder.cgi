#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
case $index in
	0)
         reactive=0
         if [ $old_vidin != $vidin ] || [ $old_audrate != $audrate ] || [ $old_aud_sample_rate != $aud_sample_rate ] || [ $old_res != $vidres ]; then
              reactive=1
         fi
         /usr/sbin/encoder_params 127.0.0.1 6180 3 "enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_res=$vidres|" $reactive
         echo "/usr/sbin/encoder_params 127.0.0.1 6180 3 \"enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_res=$vidres|\" $reactive" > /tmp/saveencoder
         #/usr/sbin/encoder_params $encaddr $encport 3 "enc0.vid_bitrate=$vidrate|enc0.vid_in=$vidin|enc0.aud_bitrate=$audrate|enc0.aud_sample_rate=$aud_sample_rate|enc0.vid_res=$vidres|" $reactive
	;;
esac
echo ""

#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
/usr/sbin/encoder_params 127.0.0.1 6180 3 "enc1.vid_bitrate=$vidrate|"
echo ""

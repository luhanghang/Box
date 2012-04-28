#!/bin/sh
echo AT+CGACT=0,1 > /dev/ttyUSB0
echo "0" > /etc/ppp/4g
echo ""
echo "1"

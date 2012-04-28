#!/bin/sh
led=`cat /tmp/led`
if [ $led == 2 ]; then
	led=1
else
	led=2
fi
result=`3gled -p /dev/ttyAM1 -c $led`
result=`echo $led > /tmp/led`
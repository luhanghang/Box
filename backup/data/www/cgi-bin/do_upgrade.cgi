#!/bin/sh
v_conf=`cat /etc/version`
c_version=`echo $v_conf|awk '{print $1}'`
server=`echo $v_conf|awk '{print $2}'`
c_ver=`echo $c_version|cut -d. -f1,2`
echo 10 > /tmp/progress
ftpget -u longcent -p 1 $server /backup.tar backup$c_ver.tar
echo 20 > /tmp/progress
tar -vx -f /backup.tar -C /tmp
echo 50 > /tmp/progress
rm /backup.tar
cp -R /tmp/backup/* /
echo 70 > /tmp/progress
rm -rf /backup
echo 90 > /tmp/progress
mv /tmp/backup /backup
echo 100 > /tmp/progress
sleep 3
reboot

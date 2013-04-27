#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

echo ""
config="auto=$auto\n"
config="${config}standard=$standard\n"
config="${config}service_number=$service_number\n"
config="${config}apn=$apn\n"
config="${config}username=$username\n"
config="${config}password=$passwd\n"

echo -e `httpd -d $config|tr -d ' '` > /etc/ppp/setup.cfg
echo ""
#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

echo ""
config="auto=$auto\n"
for i in $(seq 7); do
	eval standard="$"standard$i
	config="${config}standard$i=$standard\n"
	eval service_number="$"service_number$i
	config="${config}service_number$i=$service_number\n"
	eval apn="$"apn$i
	config="${config}apn$i=$apn\n"
	eval username="$"username$i
	config="${config}username$i=$username\n"
	eval password="$"passwd$i
	config="${config}password$i=$password\n"
done

echo -e `httpd -d $config|tr -d ' '` > /etc/ppp/setup.cfg
echo ""
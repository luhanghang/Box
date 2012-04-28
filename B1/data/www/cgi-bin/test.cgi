#!/bin/sh
read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
echo Content-type: text/html          
echo ""
echo ""
httpd -d $deletefiles|awk '{ split($1,files,"|"); for(i in files) if(files[i]!="") print "rm ../records/"files[i] }'

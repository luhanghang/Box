#!/bin/sh

cat|sed '1,4d;$d' > /backup.tar
cd /
tar vxf backup.tar
rm /backup.tar

echo Content-type: text/html
echo
cat << EOF
<HTML>
<meta http-equiv="Refresh" content="1; url=/cgi-bin/version.cgi">
</HTML>
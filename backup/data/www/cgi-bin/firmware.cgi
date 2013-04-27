#!/bin/sh

cat|sed '1,4d;$d' > /data/backup.tar
cd /data
tar vxf backup.tar
backup.tar

echo Content-type: text/html
echo
cat << EOF
<HTML>
<meta http-equiv="Refresh" content="1; url=/cgi-bin/version.cgi">
</HTML>
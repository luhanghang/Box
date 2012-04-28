#!/bin/sh
eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')
l=`cat /etc/lan`
if [ -z $lan ]; then
	lan=$l
else
	echo $lan > /etc/lan
fi

echo Content-type: text/html
echo "Set-Cookie: lan=$lan"
echo ""
/bin/cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<title>3G Live Super Box</title>
</head>
<frameset cols="*,800,*" border="0">
		<frame src="../blank.html"/>
		<frameset rows="30,*" border="0">
			<frame src="menu.cgi?lan=$lan" scrolling="no"/>
   			<frame name="main" src="setup.cgi?lan=$lan"/>
		</frameset>
		<frame src="../blank.html"/>
<frameset>
</html>  

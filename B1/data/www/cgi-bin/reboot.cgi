#!/bin/sh

eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

case $lan in
	1)
		. ../lan/set_strings_1
	;;
	3)
		. ../lan/set_strings_3
	;;
	*)
		. ../lan/set_strings_2
esac

echo Content-type: text/html
echo ""

/bin/cat << EOM
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
	<script type="text/javascript">
		window.onload=init;
		function init() {
			var img=document.getElementById("img");
			setInterval("redirect()",3000);
		}
	
		function redirect() {
			img.src="/load.gif?" + new Date();
		}
	</script>
</head>
<body>
<img id="img" onload="top.location='/'" style="display:none">
$s33...
</body>	
</html>
EOM
reboot
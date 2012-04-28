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

encaddr=`cat /etc/mg.conf|grep encaddr=|cut -d= -f2`
if [ "$encaddr" == "" ]; then
	encaddr="192.168.1.12";
fi

echo Content-type: text/html
echo ""
/bin/cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title></title>
<link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
<script type="text/javascript">
	function change_color(index) {
		for(var i=1; i < 9; i++) {
			var el = document.getElementById("a" + i);
			if(el) {
				el.className = "";
			}
		}
		document.getElementById("a" + index).className = "current";
	}
</script>
</head>
<body style="background-color:#666666;margin:0">
	<table width="100%" cellpadding="0" cellspacing="10">
		<tr>	
			<td>
				<a href="/cgi-bin/status.cgi?lan=$lan" class="current" id="a1" target="main" onclick="change_color(1)">$s1</a>
				<a href="/cgi-bin/setup.cgi?lan=$lan" target="main" id="a2" onclick="change_color(2)">$s2</a>
				<a href="/cgi-bin/encoder.cgi?lan=$lan" target="main" id="a4" onclick="change_color(4)">$s48</a>
				<a href="http://$encaddr:8000/cgi-bin/records.cgi?lan=$lan" target="main" id="a8" onclick="change_color(8)">$s119</a>
				<a href="/cgi-bin/changepass.cgi?lan=$lan" target="main" id="a3" onclick="change_color(3)">$s3</a>
				<a href="/cgi-bin/version.cgi?lan=$lan" target="main" id="a5" onclick="change_color(5)">$s71</a>
				<!--<a href="/cgi-bin/reset.cgi?lan=$lan" target="main" onclick="return confirm('$s46？')">$s5</a>-->
				<a href="/cgi-bin/reboot.cgi?lan=$lan" target="main" onclick="return confirm('$s47？')">$s6</a>
			</td>
			<td style="text-align:right">
				<a href="/cgi-bin/index.cgi?lan=2" target="_top">简体</a>
				<a href="/cgi-bin/index.cgi?lan=3" target="_top">繁體</a>
				<a href="/cgi-bin/index.cgi?lan=1" target="_top">English</a>
			</td>
		</tr>
	</table>
</body>
</html>

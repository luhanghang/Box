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
	<link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
	<script type="text/javascript" src="/javascripts/jquery.js"></script>
	<script type="text/javascript" src="/javascripts/prototype.js"></script>
	<script type="text/javascript" src="/javascripts/changepass.js"></script>
	<title></title>
</head>
<body>
	<div>$s3</div>
	<hr size="1">
	<form method="post" action="javascript:void(0)" onsubmit="do_submit('$s29',$lan)">
	<table width="100%">
		<tr>
			<td class="label">$s22</td>
			<td>
				admin
			</td>
		</tr>
		<tr>
			<td class="label">$s24</td>
			<td>
				<input type="password" name="curpass" id="curpass">
			</td>
		</tr>
		<tr>
			<td class="label">$s25</td>
			<td>
				<input type="password" name="newpass" id="newpass"> <font color="green">$s31</font>
			</td>
		</tr>
		<tr>
			<td class="label">$s26</td>
			<td>
				<input type="password" name="confirmpass" id="confirmpass">
			</td>
		</tr>
		<tr>
			<td>&nbsp;</td>
			<td><div id="error" style="color:red"></div></td>
		</tr>
		<tr>
			<td colspan="2">
				<input type="submit" value="$s3">
			</td>
		</tr>
	</table>
	</form>
</body>
</html>
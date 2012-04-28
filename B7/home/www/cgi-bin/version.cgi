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

v_conf=`cat /etc/version`
c_version=`echo $v_conf|awk '{print $1}'`
l_version=$c_version
server=`echo $v_conf|awk '{print $2}'`

display_install="none";
uploaded_ver=$s113;
if [ -f "/backup/etc/version" ]; then
	uploaded_ver=`cat /backup/etc/version|awk '{print $1}'`
	display_install="inline";
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
<script type="text/javascript" src="/javascripts/prototype.js"></script>
    <script type="text/javascript" src="/javascripts/jquery.js"></script>
<script type="text/javascript" src="/javascripts/version.js"></script>
</head>
<body>
	<div id="waiting" style="display:none">
		<div id="upload" style="margin-top:30px;">
			$s115
		</div>
		<div style="margin-top:20px">
			<img src="/images/uploading.gif"/>
		</div>	
	</div>
	<div>$s71</div>
	<hr size="1">
	<form id="form1" action="firmware.cgi" method="post" enctype="multipart/form-data">
	<table width="100%">
		<tr>
			<td class="label">$s74</td>
			<td>
				<span id="c_version">$c_version</span>
			</td>
		</tr>
		<tr id="uploaded_version">
			<td class="label">$s111</td>
			<td>
				<span id="new_ver">$uploaded_ver</span>
			</td>
		</tr>
		<tr>
			<td class="label">$s109</td>
			<td>
				<input id="file" name="file" type="file">	
				<input type="button" value="$s114" onclick="check_upload_file();">
			</td>
		</tr>
		<tr id="connect_error" style="display:none">
			<td class="label">&nbsp;</td>
			<td>
				<span class="error_tip">$s80</span>
			</td>
		</tr>
		<tr id="caution" style="display:none">
			<td class="label">&nbsp;</td>
			<td>
				<span class="error_tip">$s78</span>
			</td>
		</tr>
		<tr id="progress" style="display:none">
			<td class="label">$s81</td>
			<td>
				<div>
					<div id="block0" class="bar_block"></div>
					<div id="block1" class="bar_block"></div>
					<div id="block2" class="bar_block"></div>
					<div id="block3" class="bar_block"></div>
					<div id="block4" class="bar_block"></div>
					<div id="block5" class="bar_block"></div>
					<div id="block6" class="bar_block"></div>
					<div id="block7" class="bar_block"></div>
					<div id="block8" class="bar_block"></div>
					<div id="block9" class="bar_block"></div>
				</div>
				<div id="u_progress" style="margin-left:5px;float:left">0%</div>
			</td>
		</tr>
		<tr>
			<td colspan="2"><hr size="1"/></td>
		</tr>
		<tr>
			<td colspan="2">
				<input type="button" value="$s110" style="margin-right:10px;display:$display_install" onclick="if(confirm('$s112$uploaded_ver?')) {start_install()}">	
			</td>
		</tr>
	</table>
	</form>
</body>
</html>
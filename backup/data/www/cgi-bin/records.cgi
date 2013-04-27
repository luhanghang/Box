#!/bin/sh
read QUERY_STRING

eval $(echo "$QUERY_STRING"|awk -F'&' '{for(i=1;i<=NF;i++){print $i}}')

if [ ! -d "../records/1" ]; then
	echo Content-type: text/html
	echo ""
	echo "SD Card Format Error!"
	exit
fi

src=`httpd -d $src`
files=`httpd -d $deletefiles`
if [ "X$files" != "X" ]; then
	httpd -d $deletefiles|awk '{ split($1,files,"|"); for(i in files) if(files[i]!="") system("rm -f ../records/"files[i]) }'
fi
case $lan in
	1)
        	. ../lan/set_strings_1
        ;;
        3)
       		. ../lan/set_strings_3
        ;;
        *)
       		. ../lan/set_strings_2
       	;;
esac
cd ../records

params=`/usr/sbin/encoder_params 127.0.0.1 6180 2 "enc1.vid_bitrate|"`
vidrate=`echo $params|awk '{print $1}'|cut -d= -f2`

echo Content-type: text/html
echo ""
/bin/cat << EOM
<!DOCTYPE HTML>
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <script type="text/javascript" src="/javascripts/prototype.js"></script>
    <script type="text/javascript" src="/javascripts/jquery.js"></script>	
    <script type="text/javascript" src="/javascripts/records.js"></script>	
    <link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
    <style type="text/css">
    	#filelist {
    		float:left;width:220px;marign-right:20px;
    	}
    	
    	.filename {
    		border-bottom: 1px solid #aaa;
    		height:20px;
    	}
    	
    	.filename div {
    		float:left;
    	}
    	
    	.file {
    		margin:10px;
    		margin-left:0;
    		clear:both;
    	}
    	
    	.info div{
    		float:left;
    		height:30px;
    		color:green;
    	}
    </style>
    <script type="text/javascript">
    	function play(src) {
    		document.getElementById("src").value=src;
    		document.getElementById("form").submit();
    	}
    	function to_delete(file) {
    		if(confirm('$s120')) {
    			document.getElementById("deletefiles").value=file;
    			document.getElementById("form").submit();
    		}
    	}
    </script>
    <title></title>
</head>
<body>
<form id="form" method="POST" action="records.cgi">
	<input type="hidden" name="src" id="src">
	<input type="hidden" name="deletefiles" id="deletefiles">
</form>
<form id="form1" method="POST" action="javascript:void(0)" onsubmit="change_vidrate()">
	$s51$s53 <input type="text" value="$vidrate" id="vidrate"/> <input id="save0" type="submit" value="$s27">
</form>
<hr size="1"/>

<div id="filelist">
EOM
for dir in `ls`
do
	ls -A -l -h $dir|awk -v dir=$dir -v title=$s121 '{print "<div class=\"filename\"><div style=\"width:184px\"><input type=\"checkbox\" class=\"checkbox\" name=\"ck_file\" value=\""dir"/"$9"\"/><a style=\"font-size:14px;color:#666\" href=\"/records/"dir"/"$9"\">"$9"</a></div><div><a href=\"javascript:to_delete('"'"'"dir"/"$9"'"'"')\"><img src=\"/images/delete.png\" width=16 border=0/></a></div></div><div class=\"info\"><div style=\"width:180px;\">"$5"</div><div><a href=\"javascript:play('"'"'/records/"dir"/"$9"'"'"')\"><img style=\"margin-top:-3px;width:24px\" src=\"/images/play.png\" title=\""title"\" border=0/></a></div></div>"}'|awk '{{printf"<div class=\"file\">%s</div>",$0}}'
done

/bin/cat << EOM1
	<div style="clear:both"></div>
	<hr size="1"/>
	<input type="checkbox" onclick="toggle_all(this)"/>
	<input type="button" value="$s122" onclick="if(confirm('$s120')) { delete_multi();}"/>
</div>
<div style="float:left;">
	<object id="vlcIE" classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" codebase="http://download.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab" width="540" height="432">
		<param id="vlcSrc" name="Src" value="$src"/>
		<param name="ShowDisplay" value="True" /> 
		<param name="AutoLoop" value="False" /> 
		<param name="AutoPlay" value="True" />
		<embed id="vlc" src="$src" type="application/x-vlc-plugin" pluginspage="http://www.videolan.org" width="540" height="432"/>
	</object>	
</div>
</body>
</html>

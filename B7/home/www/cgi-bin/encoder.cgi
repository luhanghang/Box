#!/bin/sh
encaddr=`cat /etc/mg.conf|grep encaddr=|cut -d= -f2`
if [ "$encaddr" == "" ]; then
	encaddr="192.168.240.12";
fi

encport=`cat /etc/mg.conf|grep encport=|cut -d= -f2`
if [ "$encport" == "" ]; then
	encport="6180";
fi
params=`/usr/sbin/encoder_params $encaddr $encport 2 "enc0.vid_bitrate|enc0.vid_in|enc0.aud_bitrate|enc0.aud_sample_rate|enc0.vid_mode|"`
vidrate=`echo $params|awk '{print $1}'|cut -d= -f2`
vidin=`echo $params|awk '{print $2}'|cut -d= -f2`
audrate=`echo $params|awk '{print $3}'|cut -d= -f2`
audsamplerate=`echo $params|awk '{print $4}'|cut -d= -f2`
res=`echo $params|awk '{print $5}'|cut -d= -f2`
if [ $vidin == 'sdi' ]; then
	sdi=" checked"
else
	cvbs=" checked"
	audisabled=" disabled"
fi

if [ "$res" == "" ]; then
	res="PAL"
fi

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

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <link href="/css/stylesheet.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="/javascripts/prototype.js"></script>
    <script type="text/javascript" src="/javascripts/jquery.js"></script>
    <script type="text/javascript" src="/javascripts/encoder.js"></script>
    <script type="text/javascript">
    	window.onload = init;
    	function init() {
    		document.getElementById("vidres").value = "$res";
    	}
    </script>
    <title></title>
</head>
<body>
	<div>$s48</div>
    
   <form id="form0" method="post" action="javascript:void(0)" onsubmit="do_submit(0,'$s28')">  
   	<input type="hidden" name="index" value="0">       
        <hr size="1">
    
            <table cellpadding="0" cellspacing="0" width="100%">
				        <input type="hidden" name="encaddr" value="$encaddr">
                <tr>
                    <td class="label">
                        $s51$s118
                    </td>
                    <td class="value">
                        <input type="hidden" name="old_res" value="$res">
                        <select name="vidres" value="$res" id="vidres">
                        	<option value="1080p30">1080p30</option>
                        	<option value="1080p25">1080p25</option>
                        	<option value="1080i50">1080i50</option>
                        	<option value="720p60">720p60</option>
                        	<option value="720p50">720p50</option>
                        	<option value="720p30">720p30</option>
                        	<option value="720p25">720p25</option>
                        	<option value="PAL">720x576</option>
                        	<option value="352x288">352x288</option>
                        </select>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s51$s53
                    </td>
                    <td class="value">
                        <input type="text" name="vidrate" value="$vidrate"> 128～8000Kbps
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s87
                    </td>
                    <td class="value">
                    	<input type="radio" id="cvbs" name="vidin" value="composite"$cvbs>CVBS
                    	<input type="radio" id="sdi" name="vidin" value="sdi"$sdi>SDI
                    	<input type="hidden" name="old_vidin" value="$vidin">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s108
                    </td>
                    <td class="value">
                        <input type="text" id="audrate" name="audrate" value="$audrate">
                        <input type="hidden" id="old_audrate" name="old_audrate" value="$audrate">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s88
                    </td>
                    <td class="value">
                        <input type="text" id="aud_sample_rate" name="aud_sample_rate" value="$audsamplerate">
                        <input type="hidden" id="old_aud_sample_rate" name="old_aud_sample_rate" value="$audsamplerate">
                    </td>
                </tr>
            </table>    
        
        <hr size="1">
        <div>
            <input id="save0" type="submit" value="$s27">
            <input type="reset" value="$s37">
        </div>
</form>
</body>
</html>

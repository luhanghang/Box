#!/bin/sh

conf=`cat /etc/encoder/conf`
encoder=`echo $conf|awk '{print $1}'`
eth0_ip=`cat /etc/netconf|awk '{print $1}'`
eth0_mask=`cat /etc/netconf|awk '{print $2}'`
host=`cat /etc/mg.conf|grep host=|cut -d= -f2`
local_port=`cat /etc/mg.conf|grep local_port=|cut -d= -f2`
buffer=`cat /etc/mg.conf|grep buffer=|cut -d= -f2`
rate_min=`cat /etc/mg.conf|grep rate_min=|cut -d= -f2`
rate_max=`cat /etc/mg.conf|grep rate_max=|cut -d= -f2`
destination_port=`cat /etc/mg.conf|grep destination_port=|cut -d= -f2`
ppp0_dial=`cat /etc/ppp/chat-wcdma|grep ATDT|tr "\"" " "|sed 's/ATDT//g'|awk '{print $2}'`
ppp0_apn=`grep "AT+CGDCONT=1" /etc/ppp/chat-wcdma|cut -d, -f3|tr "\"" " "|awk '{print $1}'`
ppp1_dial=`cat /etc/ppp/chat-wcdma-1|grep ATDT|tr "\"" " "|sed 's/ATDT//g'|awk '{print $2}'`
ppp1_apn=`grep "AT+CGDCONT=1" /etc/ppp/chat-wcdma-1|cut -d, -f3|tr "\"" " "|awk '{print $1}'`
ppp0_user=`cat /etc/ppp/peers/wcdma0|grep "^user "|tr "\"" " "|awk '{print $2}'`
ppp0_passwd=`cat /etc/ppp/peers/wcdma0|grep "^password "|tr "\"" " "|awk '{print $2}'`
ppp1_user=`cat /etc/ppp/peers/wcdma1|grep "^user "|tr "\"" " "|awk '{print $2}'`
ppp1_passwd=`cat /etc/ppp/peers/wcdma1|grep "^password "|tr "\"" " "|awk '{print $2}'`
standard0=`cat /etc/ppp/standard|grep 0=|cut -d= -f2`
standard1=`cat /etc/ppp/standard|grep 1=|cut -d= -f2`
tcp=`grep tcp= /etc/mg.conf|cut -d= -f2`
uuid=`gen_uuid`
trans=`cat /etc/trans`

if [ "$rate_min" == "" ]; then
	rate_min=500	
fi

if [ "$rate_max" == "" ]; then
	rate_max=800	
fi


if [ ${tcp} == 1 ]; then
	tcpchecked="checked"
else
	udpchecked="checked"
fi

if [ ${standard0} == 'wcdma' ]; then
	wcdma0="checked"
else
	evdo0="checked"
fi

if [ ${standard1} == 'wcdma' ]; then
	wcdma1="checked"
else
	evdo1="checked"
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
    <script type="text/javascript" src="/javascripts/setup.js"></script>
    <script type="text/javascript">
    	var trans = $trans;
    </script>
    <title></title>
</head>
<body>

<form id="form0" method="post" action="javascript:void(0)" onsubmit="do_submit(0,'$s28')">
	<input type="hidden" name="index" value="0">
    <div>$s2</div>
    <hr size="1">
	$s86 <img id="switch_trans" src="/images/switch_$trans.png" style="vertical-align:-5px;cursor:pointer" onclick="toggle_trans('$s28')"/> $s85
    <hr size="1">
    <div>
        <div>
            <div>
                $s7
            </div>
            <hr size="1">
            <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s9
                    </td>
                    <td class="value" valign="middle">
                        <input type="text" name="eth0_ip" id="eth0_ip" value="$eth0_ip">
                    </td>
                    <td class="error" valign="middle">
                    	<span id="error_eth0_ip" class="error_tip" style="display:none">$s35</span>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s10
                    </td>
                    <td class="value">
                        <input type="text" name="eth0_mask" id="eth0_mask" value="$eth0_mask">
                    </td>
                    <td class="error">
                    	<span id="error_eth0_mask" class="error_tip" style="display:none">$s36</span>
                    </td>
                </tr>
            </table>
        </div>
        <hr size="1">
        <div>
            <input type="submit" id="save0" value="$s27">
            <input type="reset" value="$s37">
        </div>
</form>
        <hr size="1">
        $s15
        <hr size="1">
        <table style="width:100%" cellspacing="0" cellpadding="0">
        	<tr>
        		<td style="width:50%">
        		Card0
        		<hr size="1">
<form id="form1" method="post" action="javascript:void(0)" onsubmit="do_submit(1,'$s28')">
	<input type="hidden" name="index" value="1">
        <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s83
                    </td>
                    <td class="value">
                        <input type="radio" value="wcdma" name="standard0" $wcdma0>WCDMA
                        <input type="radio" value="evdo" name="standard0" $evdo0>EVDO
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s38
                    </td>
                    <td class="value">
                        <input type="text" name="ppp0_dial" id="ppp0_dial" value="$ppp0_dial">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s39
                    </td>
                    <td class="value">
                        <input type="text" name="ppp0_apn" id="ppp0_apn" value="$ppp0_apn">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s40
                    </td>
                    <td class="value">
                        <input type="text" name="ppp0_user" id="ppp0_user" value="$ppp0_user">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s23
                    </td>
                    <td class="value">
                        <input type="text" name="ppp0_passwd" id="ppp0_passwd" value="$ppp0_passwd">
                    </td>
                </tr>
            </table>
        </div>
        <hr size="1">
        <div>
            <input type="submit" id="save1" value="$s27">
            <input type="reset" value="$s37">
        </div>
</form>
	</td>
	<td>
		Card1
        <hr size="1">
<form id="form2" method="post" action="javascript:void(0)" onsubmit="do_submit(2,'$s28')">
	<input type="hidden" name="index" value="2">
        <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s83
                    </td>
                    <td class="value">
                        <input type="radio" value="wcdma" name="standard1" $wcdma1>WCDMA
                        <input type="radio" value="evdo" name="standard1" $evdo1>EVDO
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s38
                    </td>
                    <td class="value">
                        <input type="text" name="ppp1_dial" id="ppp1_dial" value="$ppp1_dial">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s39
                    </td>
                    <td class="value">
                        <input type="text" name="ppp1_apn" id="ppp1_apn" value="$ppp0_apn">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s40
                    </td>
                    <td class="value">
                        <input type="text" name="ppp1_user" id="ppp1_user" value="$ppp1_user">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s23
                    </td>
                    <td class="value">
                        <input type="text" name="ppp1_passwd" id="ppp1_passwd" value="$ppp1_passwd">
                    </td>
                </tr>
            </table>
        </div>
        <hr size="1">
        <div>
            <input type="submit" id="save2" value="$s27">
            <input type="reset" value="$s37">
        </div>
</form>
		</td>
	</tr>
</table>		
<form id="form3" method="post" action="javascript:void(0)" onsubmit="do_submit(3,'$s28')">
	<input type="hidden" name="index" value="3">
        <hr size="1">
        <div>
            <div>
                $s41
            </div>
            <hr size="1">
            <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s42
                    </td>
                    <td class="value">
                        <input type="text" name="host" id="host" value="$host">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s69
                    </td>
                    <td class="value">
                        <input type="text" name="rate_min" id="rate_min" value="$rate_min" minlength=3 maxlength=4 size="4" style="text-align:right" onblur="var n=parseInt(this.value);this.value=isNaN(n)?500:n;">Kb
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s68
                    </td>
                    <td class="value">
                        <input type="text" name="rate_max" id="rate_max" value="$rate_max" minlength=3 maxlength=4 size="4" style="text-align:right" onblur="var n=parseInt(this.value);this.value=isNaN(n)?800:n;">Kb
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s44
                    </td>
                    <td class="value">
                        <input type="text" name="destination_port" id="destination_port" value="$destination_port">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s45
                    </td>
                    <td class="value">
                        <input type="radio" name="tcp" value="1" $tcpchecked>TCP
                        <input type="radio" name="tcp" value="0" $udpchecked>UDP
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s82
                    </td>
                    <td class="value">
                        <input type="text" name="buffer" id="buffer" value="$buffer">
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        UUID
                    </td>
                    <td class="value">
                        <input type="text" value="$uuid" readonly style="color:#ff0000">
                    </td>
                </tr>
            </table>
        </div>
        <hr size="1">
        <div>
            <input type="submit" id="save3" value="$s27">
            <input type="reset" value="$s37">
        </div>
    </div>
</form>
<!--
<form id="form4" method="post" action="javascript:void(0)" onsubmit="do_submit(4,'$s28')">
	<input type="hidden" name="index" value="4">
        <hr size="1">
            <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s66
                    </td>
                    <td class="value">
                        <input type="text" name="encoder" id="encoder" value="$encoder">
                    </td>
                </tr>
            </table>
        <hr size="1">
        <div>
            <input type="submit" id="save4" value="$s27">
            <input type="reset" value="$s37">
        </div>
    </div>
</form>
-->
</body>
</html>

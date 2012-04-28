#!/bin/sh

eth1_ip=`cat /etc/netconf|sed -n 1p`
eth1_mask=`cat /etc/netconf|sed -n 2p`
eth1_gateway=`cat /etc/netconf|sed -n 3p`

host=`cat /etc/mg.conf|grep host=|cut -d= -f2`
local_port=`cat /etc/mg.conf|grep local_port=|cut -d= -f2`
buffer=`cat /etc/mg.conf|grep buffer=|cut -d= -f2`
destination_port=`cat /etc/mg.conf|grep destination_port=|cut -d= -f2`
tcp=`grep tcp= /etc/mg.conf|cut -d= -f2`
uuid=`gen_uuid`
rate_min=`cat /etc/mg.conf|grep rate_min=|cut -d= -f2`
rate_max=`cat /etc/mg.conf|grep rate_max=|cut -d= -f2`
transmit=`cat /etc/mg.conf|grep transmit=|cut -d= -f2`
trans=`cat /etc/trans`

if [ "$rate_min" == "" ]; then
	rate_min=500	
fi

if [ "$rate_max" == "" ]; then
	rate_max=800	
fi

if [ ${tcp} = 1 ]; then
	tcpchecked="checked"
else
	udpchecked="checked"
fi

case $transmit in
	1)
		tran1="checked"
	;;
	2)
		tran2="checked"
	;;
	3)
		tran3="checked"
	;;
	4)
		tran4="checked"
	;;
	5)
		tran5="checked"
	;;
	*)
		tran0="checked"
	;;
esac

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
                        <input type="text" name="eth1_ip" id="eth1_ip" value="$eth1_ip">
                    </td>
                    <td class="error" valign="middle">
                    	<span id="error_eth1_ip" class="error_tip" style="display:none">$s35</span>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s10
                    </td>
                    <td class="value">
                        <input type="text" name="eth1_mask" id="eth1_mask" value="$eth1_mask">
                    </td>
                    <td class="error">
                    	<span id="error_eth1_mask" class="error_tip" style="display:none">$s36</span>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        $s98
                    </td>
                    <td class="value">
                        <input type="text" name="eth1_gateway" id="eth1_gateway" value="$eth1_gateway">
                    </td>
                    <td class="error">
                    	<span id="error_eth1_gateway" class="error_tip" style="display:none">$s36</span>
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
<form id="form3" method="post" action="javascript:void(0)" onsubmit="do_submit(3,'$s28')">
	<input type="hidden" name="index" value="3">
        <hr size="1">
        <div>
            <div>
            	<table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td class="label">
                        $s101
                    </td>
                    <td class="value">
                        <input type="radio" name="t_method" value="0" $tran0>Ethernet
                		<input type="radio" name="t_method" value="1" $tran1>Wifi
                		<input type="radio" name="t_method" value="2" $tran2>Wimax
                		<!--<input type="radio" name="t_method" value="3" $tran3>$s102-->
                		<input type="radio" name="t_method" value="4" $tran4>$s102
                		<input type="radio" name="t_method" value="5" $tran5>4G
                    </td>
                </tr>
				</table>
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
                <tr style="display:none">
                    <td class="label">
                        $s43
                    </td>
                    <td class="value">
                        <input type="text" name="local_port" id="local_port" value="6008">
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

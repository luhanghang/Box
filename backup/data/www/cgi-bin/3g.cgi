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

config="/etc/ppp/setup.cfg"
auto=`grep auto= $config|cut -d= -f2`
if [ "$auto" == "1" ]; then
	auto_checked="checked"
else
	manual_checked="checked"
fi

standard=`grep standard= $config|cut -d= -f2`
wcdma_checked=''
evdo_checked=''
if [ $standard = 'wcdma' ]; then
	wcdma_checked='checked'
else
	evdo_checked='checked'
fi

servicenumber=`grep service_number= $config|cut -d= -f2`                                
apn=`grep apn= $config|cut -d= -f2`                                
username=`grep username= $config|cut -d= -f2`                                
password=`grep password= $config|cut -d= -f2`                                

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
    <script type="text/javascript" src="/javascripts/3g.js"></script>
    <title></title>
    <style>
    	td.label {
    		width:120px;
    	}
    </style>
</head>
<body>

<form id="form0" method="post" action="javascript:void(0)" onsubmit="do_submit(0,'$s28')">
	<input type="hidden" name="index" value="0">
    <div>
    	<table cellpadding="0" cellspacing="0" width="100%">
        	<tr>
            	<td class="label">
                	$s104
             	</td>
                <td class="value" valign="middle">
                    <input type="radio" value="1" name="auto" $auto_checked> $s105 
    				<input type="radio" value="0" name="auto" style="margin-left:20px" $manual_checked> $s106                    
    			</td>
            </tr>
         </table>
         <hr size="1"/>
         <table cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td class="label">
                 	$s83                     
    		</td>
    		<td>
    			$s38
    		</td>
    		<td>
    			$s39
    		</td>
    		<td>
    			$s22
    		</td>
    		<td>
    			$s23
    		</td>
            </tr>
            <tr>
            	<td style="text-align:center" colspan="10">
            		<hr size="1"/>
            	</td>
            </tr>
	    <tr>
                <td class="label">
    			<input type='radio' name='standard' value='wcdma' $wcdma_checked> wcdma
    			<input type='radio' name='standard' value='evdo' $evdo_checked> evdo                                
    		</td>
    	    	<td>
    			<input type='text' name='service_number' value='$servicenumber'>                                
    		</td>
    		<td>
    			<input type='text' name='apn' value='$apn'>                                
    		</td>
    		<td>
    			<input type='text' name='username' value='$username'>                                
    		</td>
    		<td>
    			<input type='text' name='passwd' value='$password'>                                
    		</td>
   	    </tr>                	
		<tr>
            	<td style="text-align:center" colspan="10">
            		<hr size="1"/>
            	</td>
            </tr>
            <tr>
            	<td colspan="10" style="padding-left:20px">
            		<input type="submit" value="$s27">
            	</td>
            </tr>
	</table>
    </div>
</form>
</body>
</html>
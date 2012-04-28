window.onload=init;

function init() {
	read();
//	setInterval('read()',3000);
}

function read() {
	$.post('/cgi-bin/status.cgi', {}, 
		function(result) {
			var status = eval('('+result+')');
			var eth0 = status.eth0.split(" ");
			$_("eth0_mac").innerHTML = eth0[0];
			$_("eth0_ip").innerHTML = eth0[1];
			$_("eth0_mask").innerHTML = eth0[2];
			$_("eth0_rx").innerHTML = eth0[3];
			$_("eth0_tx").innerHTML = eth0[4];
			$_("dns").innerHTML = status.dns;
			
			if(typeof(status.speed) != 'undefined') {
				$_("speed").innerHTML = status.speed;
			}
			
			var c0 = status.csq0;
			if( c0 != 'N/A') {
				c0 += "%";
			} else {
				status.csq0=0;
			}
			var c1 = status.csq1;
			if(c1 != 'N/A') {
				c1 += "%";
			} else {
				status.csq1=0;
			}
			$_("csq0").innerHTML = c0;
			$_("csq1").innerHTML = c1;
			

			$_("img_csq0").src = "/images/level" + Math.round(status.csq0/20) + ".gif";
			$_("img_csq1").src = "/images/level" + Math.round(status.csq1/20) + ".gif";
			
		
			if(typeof(status.ppp0) != 'undefined') {
				var ppp0 = status.ppp0.split(" ");
				$_("ppp0_ip").innerHTML = ppp0[0];
				$_("ppp0_ptp").innerHTML = ppp0[1];
				$_("ppp0_mask").innerHTML = ppp0[2];
				$_("ppp0_rx").innerHTML = ppp0[3];
				$_("ppp0_tx").innerHTML = ppp0[4];
				$_("ppp0_status").innerHTML = "<font color='green'>online</font>";				
			} else {
				$_("ppp0_ip").innerHTML = '';
				$_("ppp0_ptp").innerHTML = '';
				$_("ppp0_mask").innerHTML = '';
				$_("ppp0_rx").innerHTML = '0';
				$_("ppp0_tx").innerHTML = '0';
				$_("ppp0_status").innerHTML = "<font color='red'>offline</font>";				
			}
			if(typeof(status.ppp1) != 'undefined') {
				var ppp1 = status.ppp1.split(" ");
				$_("ppp1_ip").innerHTML = ppp1[0];
				$_("ppp1_ptp").innerHTML = ppp1[1];
				$_("ppp1_mask").innerHTML = ppp1[2];
				$_("ppp1_rx").innerHTML = ppp0[3];
				$_("ppp1_tx").innerHTML = ppp0[4];
				$_("ppp1_status").innerHTML = "<font color='green'>online</font>";				
			} else {
				$_("ppp1_ip").innerHTML = '';
				$_("ppp1_ptp").innerHTML = '';
				$_("ppp1_mask").innerHTML = '';
				$_("ppp1_rx").innerHTML = '0';
				$_("ppp1_tx").innerHTML = '0';
				$_("ppp1_status").innerHTML = "<font color='red'>offline</font>";				
			}
		}
	);
}

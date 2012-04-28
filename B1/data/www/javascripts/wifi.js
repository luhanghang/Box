function search_ap() {
	var sa = document.getElementById('searchap');
	sa.disabled = true;
	$.post('/cgi-bin/wificonf.cgi', {'index':'1'},
		function(result) {
			var pas = result.split(" ");	
			var essid = document.getElementById('essid');
			essid.options.length = pas.length;
			for(var i = 0; i < pas.length; i++) {
				essid.options[i].text = pas[i];
			}
			sa.disabled = false;
		}
	);
}

function test_connection() {
	$.post('/cgi-bin/wifitest.cgi', {},
		function(result) {
			alert(result);
		}
	);
}
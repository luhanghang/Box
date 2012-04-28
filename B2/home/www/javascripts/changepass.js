function do_submit(msg,lan) {
	if($_("newpass").value != $_("confirmpass").value) {
		$_("error").innerHTML = msg;
		return;
	}
	$.post('/cgi-bin/chpass.cgi', {lan:lan, curpass:$_("curpass").value, newpass:$_("newpass").value},
		function(result) {
			$_("error").innerHTML = result;	
		}
	);
}
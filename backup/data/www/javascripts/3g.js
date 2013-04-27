function do_submit(index,msg) {
	var data = $('form#form'+index).serialize();
	$.post('/cgi-bin/save3g.cgi', data,
		function(result) {
			alert(msg);		
		}
	);
}

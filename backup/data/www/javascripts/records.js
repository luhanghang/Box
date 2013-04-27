function change_vidrate() {
	var vidrate = document.getElementById('vidrate').value;
	$.post('/cgi-bin/encoder1.cgi', {'vidrate':vidrate},
		function(result) {
		}
	);
}

function delete_multi() {
	var files = "";
	jQuery.each($(".checkbox"),
		function() {
			if(this.checked) {
				files += this.value + "|";
			}
		}
	);
	if(files != "") {
		$('#deletefiles').val(files);
		document.getElementById('form').submit();	
	}		
}

function toggle_all(ck_all) {
	jQuery.each($(".checkbox"),
		function() {
			this.checked = ck_all.checked;
		}
	);
}

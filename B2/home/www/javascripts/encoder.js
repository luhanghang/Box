function do_submit(index,msg) {
	var data = $('form#form'+index).serialize();
	document.getElementById("save" + index).disabled=true;
	$.post('/cgi-bin/saveencoder.cgi', data,
		function(result) {
			document.getElementById("save" + index).disabled=false;
			var errors = document.getElementsByClassName("error_tip");
			for(var i=0; i < errors.length; i++) {
				errors[i].style.display = "none";
			}
			if(trim(result)=='') {
				alert(msg);
				return;
			}
			if(result == 'failure') {
				alert("Operation Failure");
				return;
			}
			errors=result.split(":");
			for(var i = 0; i < errors.length; i++) {
				var error=$_("error_" + trim(errors[i]));
				if(error) {
					error.style.display="block";
				}
			}		
		}
	);
}

function toggle_switch(msg) {
	onoff = 1 - onoff;
	document.getElementById("switch_onoff").src = "/images/switch_" + onoff + ".png";
	$.post('/cgi-bin/saveencoder.cgi', {'onoff':onoff, 'index':5},
		function(result) {
			if(trim(result)=='') {
				alert(msg);
				return;
			}
			if(result == 'failure') {
				alert("Operation Failure");
				return;
			}		
		}
	);
}

function toggle_auto(msg) {
	auto = 1 - auto;
	document.getElementById("switch_auto").src = "/images/switch_" + auto + ".png";
	$.post('/cgi-bin/saveencoder.cgi', {'auto':auto, 'index':6, 'top':document.getElementById('top').value,'low':document.getElementById('low').value,'step':document.getElementById('step').value},
		function(result) {
			if(trim(result)=='') {
				alert(msg);
				return;
			}
			if(result == 'failure') {
				alert("Operation Failure");
				return;
			}		
		}
	);
}

function reboot_encoder() {
	$.post('/cgi-bin/saveencoder.cgi', {'index':4},
		function(result) {
			alert(result);
		}
	);
}

function toggle_tr_audio_sample() {
	document.getElementById("audrate").disabled = !document.getElementById("sdi").checked;
	document.getElementById("aud_sample_rate").disabled = !document.getElementById("sdi").checked;
}

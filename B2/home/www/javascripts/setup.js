function do_submit(index,msg) {
	var data = $('form#form'+index).serialize();
	document.getElementById("save" + index).disabled=true;
	$.post('/cgi-bin/savesetup.cgi', data,
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

function toggle_passive(msg) {
	passive = 1 - passive;
	document.getElementById("switch_passive").src = "/images/switch_" + passive + ".png";
	$.post('/cgi-bin/savesetup.cgi', {'passive':passive,'index':12},
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
function toggle_trans(msg) {
	trans = 1 - trans;
	document.getElementById("switch_trans").src = "/images/switch_" + trans + ".png";
	$.post('/cgi-bin/savesetup.cgi', {'trans':trans,'index':11},
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

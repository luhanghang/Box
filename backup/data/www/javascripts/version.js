function check_upgrade() {
	server = document.getElementById("server").value;
	$.post('/cgi-bin/check_update.cgi', {"server":server},
		function(result) {
			if(trim(result) == '-1') {
				document.getElementById("connect_error").style.display = '';
			} else {
				document.getElementById("connect_error").style.display = 'none';
				document.getElementById("new_version").style.display = '';
				document.getElementById("new_ver").innerHTML = result;
				var sub_ver = result.split('.');
				var c_ver = trim(document.getElementById("c_version").innerHTML).split('.');
				if(parseInt(sub_ver[2]) > parseInt(c_ver[2])) {
					document.getElementById("b_upgrade").style.display = '';
				} else {
					document.getElementById("b_upgrade").style.display = 'none';
				}
			}
		}
	);
}

var progress;
var msg;

function do_upgrade(success) {
	msg = success;
	$.post('/cgi-bin/do_upgrade.cgi', null,
		function(result) {
			
		}
	);
	for(var i = 0; i < 10 ; i++) {
		document.getElementById("block" + i).className = "bar_block";
	}
	document.getElementById("caution").style.display = '';
	document.getElementById("progress").style.display = '';
	refresh_progress();
}

function refresh_progress() {
	progress = setInterval("get_progress()",1000);
}

function get_progress() {
	$.post('/cgi-bin/get_update_progress.cgi', null,
		function(result) {
			result = parseInt(trim(result));
			for(var i = 0; i < parseInt(result/10) ; i++) {
				document.getElementById("block" + i).className = "bar_block1";
			}
			document.getElementById("u_progress").innerHTML = result + "%";
			if(result == 100) {
				stop_progress();
			}
		}
	);	
}

function stop_progress() {
	clearInterval(progress);
	alert(msg);
}

function check_upload_file() {
    var filename=document.getElementById('file').value;
    if(filename.indexOf('backup') > 0 && filename.indexOf('.tar') > 0) {
        document.getElementById("waiting").style.display = "block";
        document.getElementById("form1").submit();     
    } 
}

function start_install() {
    window.location="install_firmware.cgi";
}

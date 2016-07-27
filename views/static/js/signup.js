/**
 * 
 */

$(document).ready(function() {
	var xsrf = getCookie("_xsrf");
	var pageName = document.location.href.match(/[^\/]+$/)[0];
	if (pageName == "signup") {
		fetchSubSCMS(xsrf);
	}

    setInterval(comradeBlinker, 1000);


	$('#subscms-selectall').change(function(event) {
		if ($(this).is(':checked')) {
			$('#subscms-option option').prop('selected', true) ;
			$('#subscms-option').trigger('change');
		} else {
			$('#subscms-option option').prop('selected', false) ;
			$('#gtmu-option').find('option').remove();
			$('#region-option').find('option').remove();
			$('#sl6-option').find('option').remove();
			$('#salesagent-option').find('option').remove();
		}
	});

	$('#gtmu-selectall').change(function(event) {
		if ($(this).is(':checked')) {
			$('#gtmu-option option').prop('selected', true) ;
			$('#gtmu-option').trigger('change');
		} else {
			$('#gtmu-option option').prop('selected', false) ;
			$('#region-option').find('option').remove();
			$('#sl6-option').find('option').remove();
			$('#salesagent-option').find('option').remove();
		}
	});
	
	$('#region-selectall').change(function(event) {
		if ($(this).is(':checked')) {
			$('#region-option option').prop('selected', true) ;
			$('#region-option').trigger('change');
		} else {
			$('#region-option option').prop('selected', false) ;
			$('#sl6-option').find('option').remove();
			$('#salesagent-option').find('option').remove();
		}
	});

	$('#sl6-selectall').change(function(event) {
		if ($(this).is(':checked')) {
			$('#sl6-option option').prop('selected', true) ;
			$('#sl6-option').trigger('change');
		} else {
			$('#sl6-option option').prop('selected', false) ;
			$('#salesagent-option').find('option').remove();
		}
	});

	$('#salesagent-selectall').change(function(event) {
		if ($(this).is(':checked')) {
			$('#salesagent-option option').prop('selected', true) ;
		} else {
			$('#salesagent-option option').prop('selected', false) ;
		}
	});

	$('#subscms-option').change(function(event) {
		var xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/validation/user',
			type: 'POST',
			data: {
				action: 'gtmu_fetch',
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$('#progress').show();
			},
			success: function(data, status, xhr) {
				$('#progress').hide();
				if (data['status'] == 'success') {
					var listObj = data['gtmus'];
					$('#gtmu-option').find('option').remove();
					$('#region-option').find('option').remove();
					$('#sl6-option').find('option').remove();
					$('#salesagent-option').find('option').remove();
					for (i=0; i<listObj.length; i++) {
						listObj.sort();
						var str = JSON.stringify(listObj[i]);
						str = str.replace(/\"/g, "");
						$('#gtmu-option').append($('<option />').val(str).text(str));
					}
				}
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});

	
	$('#gtmu-option').change(function(event) {
		var gtmu = [];
		var sub_scms = [];
	
		$('#subscms-option option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
	
		$('#gtmu-option option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
	
		if ((gtmu && gtmu.length != 0) && (sub_scms && sub_scms.length != 0)) {
			var xsrf = getCookie("_xsrf");
			jQuery.ajax({
				url: '/validation/user',
				type: 'POST',
				data: {
					sub_scms: sub_scms.toString(),
					gtmu: gtmu.toString(),
					action: 'region_fetch',
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					$('#progress').hide();
					if (data['status'] == 'success') {
						var listObj = data['regions'];
						$('#region-option').find('option').remove();
						$('#sl6-option').find('option').remove();
						$('#salesagent-option').find('option').remove();
						for (i=0; i<listObj.length; i++) {
							listObj.sort();
							var str = JSON.stringify(listObj[i]);
							str = str.replace(/\"/g, "");
							$('#region-option').append($('<option />').val(str).text(str));
						}
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		} else {
			alert("Nothing Selected!");
		}
	});
	
	$('#region-option').change(function(event) {
		var gtmu = [];
		var sub_scms = [];
		var region = [];
	
		$('#subscms-option option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
	
		$('#gtmu-option option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
	
		$('#region-option option:selected').each(function(i, selected) {
			region[i] = $(selected).text();
		});
		
		if ((gtmu && gtmu.length != 0) && 
				(sub_scms && sub_scms.length != 0) && 
				(region && region.length != 0)) {
			var xsrf = getCookie("_xsrf");
			jQuery.ajax({
				url: '/validation/user',
				type: 'POST',
				data: {
					sub_scms: sub_scms.toString(),
					gtmu: gtmu.toString(),
					region: region.toString(),
					action: 'sl6_fetch',
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					$('#progress').hide();
					if (data['status'] == 'success') {
						var listObj = data['sl6s'];
						$('#sl6-option').find('option').remove();
						for (i=0; i<listObj.length; i++) {
							listObj.sort();
							var str = JSON.stringify(listObj[i]);
							str = str.replace(/\"/g, "");
							$('#sl6-option').append($('<option />').val(str).text(str));
						}
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		} else {
			alert("Nothing Selected!");
		}
	});
	
	$('#sl6-option').change(function(event) {
		var gtmu = [];
		var sub_scms = [];
		var region = [];
		var sl6 = [];
	
		$('#subscms-option option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
		$('#gtmu-option option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
		$('#region-option option:selected').each(function(i, selected) {
			region[i] = $(selected).text();
		});
		$('#sl6-option option:selected').each(function(i, selected) {
			sl6[i] = $(selected).text();
		});
		
		if ((gtmu && gtmu.length != 0) && 
				(sub_scms && sub_scms.length != 0) && 
				(region && region.length != 0) && 
				(sl6 && sl6.length != 0)) {
			var xsrf = getCookie("_xsrf");
			jQuery.ajax({
				url: '/validation/user',
				type: 'POST',
				data: {
					sub_scms: sub_scms.toString(),
					gtmu: gtmu.toString(),
					region: region.toString(),
					sl6: sl6.toString(),
					action: 'salesagents_fetch',
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					$('#progress').hide();
					if (data['status'] == 'success') {
						var listObj = data['sales_agents'];
						$('#salesagent-option').find('option').remove();
						for (i=0; i<listObj.length; i++) {
							listObj.sort();
							var str = JSON.stringify(listObj[i]);
							str = str.replace(/\"/g, "");
							str = str.replace(/,/g, "_|");
							$('#salesagent-option').append($('<option />').val(str).text(str));
						}
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		} else {
			alert("Nothing Selected!");
		}
	});
	
	
	$('#userName').focus(function(event) {
		$('#span-exist-or-not').hide();
	});
	
	$('#userName').focusin(function(event) {
		$('#span-exist-or-not').hide();
	});

	$('#reset').click(function(event) {
		resetUserForm();
		$('#success-message').hide();
	});


	$('#password-change').click(function(event) {
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName').val();
		var old_password = $('#old-password').val();
		var new_password = $('#new-password').val();
		var confirm_password = $('#confirm-password').val();
        jQuery.ajax({
            url: '/admin/profile',
            type: 'POST',
            data: {
                userName: userName,
                old_password: old_password,
                new_password: new_password,
                confirm_password: confirm_password,
                _xsrf: xsrf
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $('#error').hide();
                $('#progress').show();
            },
            success: function(data, status, xhr) {
                $('#progress').hide();
                if (data['status'] == 'success') {
                    $('#change-message').show();
                    $('#change-message').html(data['message']);
                    $('#change-form').remove();
                } else {
                    $('#error').show();
                    $('#error').empty();
                    $('#error').html(data['err']);
                }
            },
            error: function(data, status, xhr) {
                $('#progress').hide();
                alert(status + "|" + xhr);
            }
        });
	});


	$('#signup-user').click(function(event) {
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName').val();
		var firstName = $('#firstName').val();
		var lastName = $('#lastName').val();
		var password = $('#password').val();
		var confirmPassword = $('#confirmPassword').val();
		var emailid = $('#email').val();
		var reportingTo = $('#reportingTo').val();
		var op_location = $('#location-option').val();
		var designation = $('#designation-option').val();
		var gtmu = [];
		var sub_scms = [];
		var region = [];
		var sl6 = [];
		var sas = [];
		$('#subscms-option option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
		$('#gtmu-option option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
		$('#region-option option:selected').each(function(i, selected) {
			region[i] = $(selected).text();
		});
		$('#sl6-option option:selected').each(function(i, selected) {
			sl6[i] = $(selected).text();
		});
		$('#salesagent-option option:selected').each(function(i, selected) {
			sas[i] = $(selected).text();
		});
		if (password == confirmPassword) {
			if (validateEmailID(emailid)) {
				if ((userName && userName.length != 0) &&
						(firstName) && (lastName) && (password) &&
						(emailid) && (reportingTo) && (op_location) &&
						(designation) && (gtmu && gtmu.length != 0) && 
						(sub_scms && sub_scms.length != 0) && 
						(region && region.length != 0) && 
						(sl6 && sl6.length != 0) && 
						(sas && sas.length != 0)) {
							jQuery.ajax({
								url: '/signup',
								type: 'POST',
								data: {
									userName: userName,
									firstName: firstName,
									lastName: lastName,
									password: password,
									emailid: emailid,
									reportingTo: reportingTo,
									op_location: op_location,
									designation: designation,
									sub_scms: sub_scms.toString(),
									gtmu: gtmu.toString(),
									region: region.toString(),
									sl6: sl6.toString(),
									sas: sas.toString(),
									_xsrf: xsrf
								},
								dataType: 'json',
								beforeSend: function(xhr, settings) {
									$('#error').hide();
									$('#progress').show();
								},
								success: function(data, status, xhr) {
									$('#progress').hide();
									if (data['status'] == 'success') {
										resetUserForm();
										$('#success-message').show();
										$('#success-message').html(data['message']);
										$('#user-form').remove();
									} else {
										$('#error').show();
										$('#error').empty();
										$('#error').html(data['err']);
									}
								},
								error: function(data, status, xhr) {
									$('#progress').hide();
									alert(status + "|" + xhr);
								}
							});
					} else {
						$('#error').show();
						$('#error').html('<span>Some of the fields are Empty or Unselected!</span>');
					}
			} else {
				$('#error').show();
				$('#error').html('<span>Email ID is not a valid Cisco email id!</span>');
			}
		} else {
			$('#error').show();
			$('#error').html('<span>Password does not match with Confirm Password!</span>');
		}
	});
	
	
	$('#userName').focusout(function(event) {
		var userID = $(event.target).val();
		xsrf = getCookie("_xsrf");
		if (userID) {
			jQuery.ajax({
				url: '/validation/user',
				type: 'POST',
				data: {
					username: userID,
					action: 'username_check',
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					$('#progress').hide();
					if (data['status'] == 'error') {
						$('#span-exist-or-not').show();
						$('#img-exist-or-not').attr("src", "/static/icons/red_cross_mark.png");
						disableAllUserFormElements();
						$('#error').show();
						$('#error').html(data['err']);
					} else {
						$('#error').empty();
						$('#error').hide();
						enableAllUserFormElements();
						$('#span-exist-or-not').show();
						var listObj = data['locations'];
						$('#img-exist-or-not').attr("src", "/static/icons/green_tick2.png");
						$('#location-option').find('option').remove().end().append($('<option />').val('Select Option').text('Select Option'));
						for (i=0; i<listObj.length; i++) {
							var locationString = JSON.stringify(listObj[i]);
							locationString = locationString.replace(/\"/g, "");
							$('#location-option').append($('<option />').val(locationString).text(locationString));
						}
						listObj = data['designations'];
						$('#designation-option').find('option').remove().end().append($('<option />').val('Select Option').text('Select Option'));
						for (i=0; i<listObj.length; i++) {
							var designationString = JSON.stringify(listObj[i]);
							designationString = designationString.replace(/\"/g, "");
							$('#designation-option').append($('<option />').val(designationString).text(designationString));
						}
						$('#email').val(userID + '@cisco.com');
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		}
	});

	
	$('#reportingTo').focusout(function(event) {
		var userID = $(event.target).val();
		xsrf = getCookie("_xsrf");
		if (userID) {
			jQuery.ajax({
				url: '/validation/user',
				type: 'POST',
				data: {
					username: userID,
					action: 'reporting_check',
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					$('#progress').hide();
					if (data['status'] == 'error') {
						$('#span-rpt-exist-or-not').show();
						$('#img-rpt-exist-or-not').attr("src", "/static/icons/red_cross_mark.png");
						disableAllUserFormElements();
						$('#error').show();
						$('#error').html(data['err']);
						$('#signup-user').attr('disabled', 'disabled');
					} else {
						$('#error').empty();
						$('#error').hide();
						enableAllUserFormElements();
						$('#span-rpt-exist-or-not').show();
						$('#img-rpt-exist-or-not').attr("src", "/static/icons/green_tick2.png");
						$('#signup-user').removeAttr('disabled');
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		}
	});

	
	$('#userName').focus(function(event) {
		$('#span-exist-or-not').hide();
	});
	
	$('#userName').focusin(function(event) {
		$('#span-exist-or-not').hide();
	});
	
	$('#reportingTo').focus(function(event) {
		$('#span-rpt-exist-or-not').hide();
	});
	
	$('#reportingTo').focusin(function(event) {
		$('#span-rpt-exist-or-not').hide();
	});


});

function validateEmailID(emailid) {
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(emailid)) {
		return true;
	}
	return false;
}
function getCookie(name) {
	var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return c ? c[1] : undefined;
}

function resetUserForm() {
	$('#userName').val('');
	$('#firstName').val('');
	$('#lastName').val('');
	$('#password').val('');
	$('#confirmPassword').val('');
	$('#email').val('');
	$('#reportingTo').val('');
	$('#location-option').val('');
	$('#location-option').find('option').remove();
	$('#designation-option').val('');
	$('#designation-option').find('option').remove();
	$('#gtmu-option').find('option').remove();
	$('#region-option').find('option').remove();
	$('#sl6-option').find('option').remove();
	$('#salesagent-option').find('option').remove();
	$('#subscms-option').find('option').remove();


	$('#location-option-update').val('');
	$('#location-option-update').find('option').remove();
	$('#designation-option-update').val('');
	$('#designation-option-update').find('option').remove();
	$('#gtmu-option-update').find('option').remove();
	$('#region-option-update').find('option').remove();
	$('#sl6-option-update').find('option').remove();
	$('#salesagent-option-update').find('option').remove();
	$('#subscms-update').find('option').remove();

	$('#location-option-edit').val('');
	$('#location-option-edit').find('option').remove();
	$('#designation-option-edit').val('');
	$('#designation-option-edit').find('option').remove();
	$('#gtmu-option-edit').find('option').remove();
	$('#region-option-edit').find('option').remove();
	$('#sl6-option-edit').find('option').remove();
	$('#salesagent-option-edit').find('option').remove();
	$('#subscms-edit').find('option').remove();

	$('#error').hide();
}

function enableAllUserFormElements() {
	$('#firstName').removeAttr('disabled');
	$('#lastName').removeAttr('disabled');
	$('#password').removeAttr('disabled');
	$('#confirmPassword').removeAttr('disabled');
	$('#email').removeAttr('disabled');
	$('#reportingTo').removeAttr('disabled');
	$('#location-option').removeAttr('disabled');
	$('#designation-option').removeAttr('disabled');
	$('#subscms-option').removeAttr('disabled');
	$('#gtmu-option').removeAttr('disabled');
	$('#region-option').removeAttr('disabled');
	$('#sl6-option').removeAttr('disabled');
	$('#salesagent-option').removeAttr('disabled');
	$('#subscms-selectall').removeAttr('disabled');
	$('#gtmu-selectall').removeAttr('disabled');
	$('#region-selectall').removeAttr('disabled');
	$('#sl6-selectall').removeAttr('disabled');
	$('#salesagent-selectall').removeAttr('disabled');
	$('#submit-user').removeAttr('disabled');
	$('#reset').removeAttr('disabled');
}

function fetchSubSCMS(xsrf) {
	jQuery.ajax({
		url: '/validation/user',
		type: 'POST',
		data: {
			action: 'subscms_fetch',
			_xsrf: xsrf
		},
		dataType: 'json',
		beforeSend: function(xhr, settings) {
			$('#progress').show();
		},
		success: function(data, status, xhr) {
			$('#progress').hide();
			if (data['status'] == 'error') {
				alert("Some Error after Success!");
			} else {
				var listObj = data['sub_scms'];
				$('#subscms-option').find('option').remove();
				listObj.sort();
				for (i=0; i<listObj.length; i++) {
					var str = JSON.stringify(listObj[i]);
					str = str.replace(/\"/g, "");
					$('#subscms-option').append($('<option />').val(str).text(str));
				}
			}
		},
		error: function(data, status, xhr) {
			$('#progress').hide();
			alert(status + "|" + xhr);
		}
	});

}

function disableAllUserFormElements() {
	$('#firstName').attr('disabled', 'disabled');
	$('#lastName').attr('disabled', 'disabled');
	
	if (('#password').length) {
		$('#password').attr('disabled', 'disabled');
	}
	if (('#confirmPassword').length) {
		$('#confirmPassword').attr('disabled', 'disabled');
	}
	
	$('#email').attr('disabled', 'disabled');
	$('#reportingTo').attr('disabled', 'disabled');
	$('#location-option').attr('disabled', 'disabled');
	$('#designation-option').attr('disabled', 'disabled');
	$('#subscms-option').attr('disabled', 'disabled');
	$('#gtmu-option').attr('disabled', 'disabled');
	$('#region-option').attr('disabled', 'disabled');
	$('#sl6-option').attr('disabled', 'disabled');
	$('#salesagent-option').attr('disabled', 'disabled');
	$('#subscms-selectall').attr('disabled', 'disabled');
	$('#gtmu-selectall').attr('disabled', 'disabled');
	$('#region-selectall').attr('disabled', 'disabled');
	$('#sl6-selectall').attr('disabled', 'disabled');
	$('#salesagent-selectall').attr('disabled', 'disabled');
	$('#submit-user').attr('disabled', 'disabled');
	$('#reset').attr('disabled', 'disabled');
}


function comradeBlinker() {
    $('.comrade-name-span').fadeOut(500);
    $('.comrade-name-span').fadeIn(500);
}

/**
 * 
 */

$(document).ready(function() {
	$('#sort-option2').change(function(event) {
		var userID = $(event.target).attr('id');
		var sortOption = $('#sort-option').val();
		xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/admin',
			type: 'GET',
			data: {
				sort_option: sortOption,
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
				}
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert("Error Caught in Ajax call return error 	" + status + "|" + xhr);
			}
		});
	});

	$('#sort-option').change(function(event) {
		event.target.form.submit();
	});

	$('#image-adduser').click(function(event) {
		userID = $(event.target).attr('id');
		xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/validation/user',
			type: 'POST',
			data: {
				action: 'subscms_fetch',
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
				$('#progress').show();
			},
			success: function(data, status, xhr) {
				$(event.target).removeAttr('disabled');
				$('#progress').hide();
				$('#adduser').show();
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
	});
	$('td.delete-cell').click(function(event) {
		var action = 'remove';
		var userID = $(event.target).attr('id');
		var xsrf = getCookie("_xsrf");	
		jQuery.ajax({
			url: '/admin/user',
			type: 'POST',
			data: {
				userName: userID,
				action: action,
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
				$('#progress').show();
			},
			success: function(data, status, xhr) {
				if (data['text'] == 'error') {
					alert(data['err']);
				} else {
					window.location.href = '/admin';
				}
				$('#progress').hide();
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});
	
	$('td.edit-cell').click(function(event) {
        console.log("this script got excecuted");
		var action = 'fetch_user';
		var userID = $(event.target).attr('id');
		var xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/admin',
			type: 'POST',	
			data: {
				username: userID,
				action: action,
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$('#progress').show();
				$(event.target).attr('disabled', 'disabled');
			},
			success: function(data, status, xhr) {
                $('#main-user-list').hide();
				$(event.target).removeAttr('disabled');
				var approvalStatus = data['approval_status'];
				var allLocArray = data['allLocations'];
                var subSCMSArray = data['subSCMS'];
                var gtmuArray = data['gtmu'];
                var regionArray = data['region'];
                var salesLevel6Array = data['salesLevel6'];
                var salesAgentsArray = data['salesAgents'];
				var allSubSCMSArray = data['allSubSCMS'];
				var authentiCode = data['authenti_code'];
				if (authentiCode == 1) {
					$('#edituser').hide();
					$('#updateuser').show();
					$('#hidden-update').val(data['username'])
					$('#userName-update').val(data['username']);
					$('#firstName-update').val(data['firstname']);
					$('#lastName-update').val(data['lastname']);
					$('#password-update').val("");
					$('#confirmPassword-update').val("");
					$('#email-update').val(data['email']);
					$('#reportingTo-update').val(data['reportingto']);
					$('#designation-update').val(data['designation']);
					// Fill the Op Location Select Option
					
					for (i=0; i<allLocArray.length; i++) {
						var string = JSON.stringify(allLocArray[i]);
						string = string.replace(/\"/g, "");
						$('#location-option-update').append($('<option />').val(string).text(string));
					}
					$('#location-option-update').val(data['op_location']); // Select the appropriate matching

					// Fill the Sub SCMS Select Option
					for (i=0; i<subSCMSArray.length; i++) {
						var string = JSON.stringify(subSCMSArray[i]);
						string = string.replace(/\"/g, "");
						$('#subscms-option-update').append($('<option />').val(string).text(string));
					}
					$('#subscms-selectall-update').prop('checked', true);
					$('#subscms-option-update option').prop('selected', true);
					

					// Fill the GTMu selection
					for (i=0; i<gtmuArray.length; i++) {
						var string = JSON.stringify(gtmuArray[i]);
						string = string.replace(/\"/g, "");
						$('#gtmu-option-update').append($('<option />').val(string).text(string));
					}
					$('#gtmu-selectall-update').prop('checked', true);
					$('#gtmu-option-update option').prop('selected', true);

					// Fill the Region selection
					for (i=0; i<regionArray.length; i++) {
						var string = JSON.stringify(regionArray[i]);
						string = string.replace(/\"/g, "");
						$('#region-option-update').append($('<option />').val(string).text(string));
					}
					$('#region-selectall-update').prop('checked', true);
					$('#region-option-update option').prop('selected', true);

					// Fill the Sales_Level_6 selection
					for (i=0; i<salesLevel6Array.length; i++) {
						var string = JSON.stringify(salesLevel6Array[i]);
						string = string.replace(/\"/g, "");
						$('#sl6-option-update').append($('<option />').val(string).text(string));
					}
					$('#sl6-selectall-update').prop('checked', true);
					$('#sl6-option-update option').prop('selected', true);

					// Fill the Sales Agents selection
					for (i=0; i<salesAgentsArray.length; i++) {
						var string = JSON.stringify(salesAgentsArray[i]);
						string = string.replace(/\"/g, "");
						string = string.replace(/,/g, "_|");
						$('#salesagent-option-update').append($('<option />').val(string).text(string));
					}
					$('#salesagent-selectall-update').prop('checked', true);
					$('#salesagent-option-update option').prop('selected', true);
				 } else {
						$('#edituser').show();
						$('#hidden-edit').val(data['username'])
						$('#userName-edit').val(data['username']);
						$('#userName-edit').attr('disabled', 'disabled');
						$('#firstName-edit').val(data['firstname']);
						$('#firstName-edit').attr('disabled', 'disabled');
						$('#lastName-edit').val(data['lastname']);
						$('#lastName-edit').attr('disabled', 'disabled');
						$('#email-edit').val(data['email']);
						$('#email-edit').attr('disabled', 'disabled');
						$('#reportingTo-edit').val(data['reportingto']);
						$('#reportingTo-edit').attr('disabled', 'disabled');
						$('#designation-edit').val(data['designation']);
						$('#designation-edit').attr('disabled', 'disabled');
						// Fill the Op Location Select Option
						
						for (i=0; i<allLocArray.length; i++) {
							var string = JSON.stringify(allLocArray[i]);
							string = string.replace(/\"/g, "");
							$('#location-option-edit').append($('<option />').val(string).text(string));
						}
						$('#location-option-edit').val(data['op_location']); // Select the appropriate matching
						$('#location-option-edit').attr('disabled', 'disabled');

						// Fill the Sub SCMS Select Option
						for (i=0; i<subSCMSArray.length; i++) {
							var string = JSON.stringify(subSCMSArray[i]);
							string = string.replace(/\"/g, "");
							$('#subscms-option-edit').append($('<option />').val(string).text(string));
						}
						$('#subscms-selectall-edit').prop('checked', true);
						$('#subscms-option-edit option').prop('selected', true);
						$('#subscms-option-edit').attr('disabled', 'disabled');
						$('#subscms-selectall-edit').attr('disabled', 'disabled');
						

						// Fill the GTMu selection
						for (i=0; i<gtmuArray.length; i++) {
							var string = JSON.stringify(gtmuArray[i]);
							string = string.replace(/\"/g, "");
							$('#gtmu-option-edit').append($('<option />').val(string).text(string));
						}
						$('#gtmu-selectall-edit').prop('checked', true);
						$('#gtmu-option-edit option').prop('selected', true);
						$('#gtmu-option-edit').attr('disabled', 'disabled');
						$('#gtmu-selectall-edit').attr('disabled', 'disabled');

						// Fill the Region selection
						for (i=0; i<regionArray.length; i++) {
							var string = JSON.stringify(regionArray[i]);
							string = string.replace(/\"/g, "");
							$('#region-option-edit').append($('<option />').val(string).text(string));
						}
						$('#region-selectall-edit').prop('checked', true);
						$('#region-option-edit option').prop('selected', true);
						$('#region-option-edit').attr('disabled', 'disabled');
						$('#region-selectall-edit').attr('disabled', 'disabled');

						// Fill the Sales_Level_6 selection
						for (i=0; i<salesLevel6Array.length; i++) {
							var string = JSON.stringify(salesLevel6Array[i]);
							string = string.replace(/\"/g, "");
							$('#sl6-option-edit').append($('<option />').val(string).text(string));
						}
						$('#sl6-selectall-edit').prop('checked', true);
						$('#sl6-option-edit option').prop('selected', true);

						// Fill the Sales Agents selection
						for (i=0; i<salesAgentsArray.length; i++) {
							var string = JSON.stringify(salesAgentsArray[i]);
							string = string.replace(/\"/g, "");
							string = string.replace(/,/g, "_|");
							$('#salesagent-option-edit').append($('<option />').val(string).text(string));
						}
						$('#salesagent-selectall-edit').prop('checked', true);
						$('#salesagent-option-edit option').prop('selected', true);
						
						if (approvalStatus == 1) {
							$('#edit-user').hide();
							$('#approve-user').css("background-color", "#C8C5DC");
							$('#reject-user').css("background-color", "#C8C5DC");
							$('#approve-user').attr('disabled', 'disabled');
							$('#reject-user').attr('disabled', 'disabled');
							$('#reject-user').show();
						} else {
							$('#edit-user').hide();
							$('#approve-user').removeAttr('disabled');
							$('#reject-user').removeAttr('disabled');
							$('#approve-user').css("background-color", "#5A5097");
							$('#reject-user').css("background-color", "#5A5097");
							$('#reject-user').show();
						}
				 }
				$('#progress').hide();
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});
	
	$('#button-cancel').click(function() {
        $('#main-user-list').show();
		resetUserForm();
		$('#success-message').hide();
		$('#adduser').hide();
	});

	$('#reset-add').click(function(event) {
		resetUserForm();
		$('#success-message').hide();
	});

	$('#button-cancel-edit').click(function() {
        $('#main-user-list').show();
		resetUserForm();
		$('#success-message').hide();
		$('#edituser').hide();
	});

	$('#button-cancel-update').click(function() {
        $('#main-user-list').show();
		resetUserForm();
		$('#updateuser').hide();
	});
	
	$('#approve-user').click(function(event) {
		var action = "approve";
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName-edit').val();
		var sl6 = [];
		var sas = [];
		$('#sl6-option-edit option:selected').each(function(i, selected) {
			sl6[i] = $(selected).text();
		});
		$('#salesagent-option-edit option:selected').each(function(i, selected) {
			sas[i] = $(selected).text();
		});
		if ((sl6 && sl6.length != 0) && (sas && sas.length != 0)) {
				jQuery.ajax({
					url: '/admin/user',
					type: 'POST',
					data: {
						userName: userName,
						sl6: sl6.toString(),
						sas: sas.toString(),
						action: action,
						_xsrf: xsrf
					},
					dataType: 'json',
					beforeSend: function(xhr, settings) {
						$('#error-edit').hide();
						$('#progress').show();
					},
					success: function(data, status, xhr) {
						if (data['status'] == 'success') {
							resetUserForm();
							$('#error-edit').hide();
							$('#edituser').hide();
							window.location.href = '/admin';
						} else {
							$('#error-edit').show();
							$('#error-edit').empty();
							$('#error-edit').html(data['err']);
							$('html, body').animate({scrollTop: 0}, 'fast');
						}
						$('#progress').hide();
					},
					error: function(data, status, xhr) {
						$('#progress').hide();
						alert(status + "|" + xhr);
					}
				});
			} else {
				$('#error-edit').show();
				$('#error-edit').html('<span>Some of the fields are Empty or Unselected!</span>');
				$('html, body').animate({scrollTop: 0}, 'fast');
			}
	});

	
	$('#reject-user').click(function(event) {
		var action = 'reject';
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName-edit').val();
		if ((sl6 && sl6.length != 0) && (sas && sas.length != 0)) {
				jQuery.ajax({
					url: '/admin/user',
					type: 'POST',
					data: {
						username: userName,
						action: action,
						_xsrf: xsrf
					},
					dataType: 'json',
					beforeSend: function(xhr, settings) {
						$('#error-edit').hide();
						$('#progress').show();
					},
					success: function(data, status, xhr) {
						if (data['status'] == 'success') {
							resetUserForm();
							$('#error-edit').hide();
							$('#edituser').hide();
							window.location.href = '/admin';
						} else {
							$('#error-edit').show();
							$('#error-edit').empty();
							$('#error-edit').html(data['err']);
							$('html, body').animate({scrollTop: 0}, 'fast');
						}
						$('#progress').hide();
					},
					error: function(data, status, xhr) {
						$('#progress').hide();
						alert(status + "|" + xhr);
					}
				});
			} else {
				$('#error-edit').show();
				$('#error-edit').html('<span>Some of the fields are Empty or Unselected!</span>');
				$('html, body').animate({scrollTop: 0}, 'fast');
			}
	});
	
	$('#sl6-selectall-edit').change(function(event) {
		if ($(this).is(':checked')) {
			$('#sl6-option-edit option').prop('selected', true) ;
			$('#sl6-option-edit').trigger('change');
		} else {
			$('#sl6-option-edit option').prop('selected', false) ;
			$('#salesagent-option-edit').find('option').remove();
		}
	});

	$('#salesagent-selectall-edit').change(function(event) {
		if ($(this).is(':checked')) {
			$('#salesagent-option-edit option').prop('selected', true) ;
		} else {
			$('#salesagent-option-edit option').prop('selected', false) ;
		}
	});

	$('#sl6-option-edit').change(function(event) {
		var gtmu = [];
		var sub_scms = [];
		var region = [];
		var sl6 = [];
	
		$('#subscms-option-edit option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
		$('#gtmu-option-edit option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
		$('#region-option-edit option:selected').each(function(i, selected) {
			region[i] = $(selected).text();
		});
		$('#sl6-option-edit option:selected').each(function(i, selected) {
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
						$('#salesagent-option-edit').find('option').remove();
						for (i=0; i<listObj.length; i++) {
							listObj.sort();
							var str = JSON.stringify(listObj[i]);
							str = str.replace(/\"/g, "");
							str = str.replace(/,/g, "_|");
							$('#salesagent-option-edit').append($('<option />').val(str).text(str));
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

	$('#submit-user-add').click(function(event) {
		var action = 'add';
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName').val();
		var firstName = $('#firstName').val();
		var lastName = $('#lastName').val();
		var password = $('#password').val();
		var confirmPassword = $('#confirmPassword').val();
		var emailid = $('#email').val();
		var reportingTo = $('#reportingTo').val();
		var op_location = $('#location-option').val();
		var designation = $('#designation').val();
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
								url: '/admin/user',
								type: 'POST',
								data: {
									userName: userName,
									action: action,
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
									if (data['status'] == 'success') {
										resetUserForm();
										$('#success-message').show();
										$('#success-message').html(data['message']);
										$('#user-form').remove();
										window.location.href = '/admin';
									} else {
										$('#error').show();
										$('#error').empty();
										$('#error').html(data['err']);
										$('html, body').animate({scrollTop: 0}, 'fast');
									}
									$('#progress').hide();
								},
								error: function(data, status, xhr) {
									$('#progress').hide();
									alert(status + "|" + xhr);
								}
							});
					} else {
						$('#error').show();
						$('#error').html('<span>Some of the fields are Empty or Unselected!</span>');
						$('html, body').animate({scrollTop: 0}, 'fast');
					}
			} else {
				$('#error').show();
				$('#error').html('<span>Email ID is not a valid Cisco email id!</span>');
				$('html, body').animate({scrollTop: 0}, 'fast');
			}
		} else {
			$('#error').show();
			$('#error').html('<span>Password does not match with Confirm Password!</span>');
			$('html, body').animate({scrollTop: 0}, 'fast');
		}
	});

	$('#submit-user-update').click(function(event) {
		var action = 'update';
		var xsrf = getCookie("_xsrf");
		var userName = $('#userName-update').val();
		var firstName = $('#firstName-update').val();
		var lastName = $('#lastName-update').val();
		var password = $('#password-update').val();
		var confirmPassword = $('#confirmPassword-update').val();
		var emailid = $('#email-update').val();
		var reportingTo = $('#reportingTo-update').val();
		var op_location = $('#location-option-update').val();
		var designation = $('#designation-update').val();
		var gtmu = [];
		var sub_scms = [];
		var region = [];
		var sl6 = [];
		var sas = [];
		$('#subscms-option-update option:selected').each(function(i, selected) {
			sub_scms[i] = $(selected).text();
		});
		$('#gtmu-option-update option:selected').each(function(i, selected) {
			gtmu[i] = $(selected).text();
		});
		$('#region-option-update option:selected').each(function(i, selected) {
			region[i] = $(selected).text();
		});
		$('#sl6-option-update option:selected').each(function(i, selected) {
			sl6[i] = $(selected).text();
		});
		$('#salesagent-option-update option:selected').each(function(i, selected) {
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
								xhr: function () {
									var xhr = new window.XMLHttpRequest();
									xhr.upload.addEventListener("progress", function(evt) {
										if (evt.lengthComputable) {
											var percentComplete = evt.loaded / evt.total;
											console.log(percentComplete);
											$('.progress').css({
												width: percentComplete * 100 + '%'
											});
											if (percentComplete === 1) {
												$('.progress').addClass('hide');
											}
										}
									}, false);
									xhr.addEventListener("progress", function(evt) {
										if (evt.lengthComputable) {
											var percentComplete = evt.loaded / evt.total;
											console.log(percentComplete);
											$('.progress').css({
												width: percentComplete * 100 + '%'
											});
										}
									}, false);
									return xhr;
								},
								url: '/admin/user',
								type: 'POST',
								data: {
									userName: userName,
									action: action,
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
									$('#error-update').hide();
									$('#progress').show();
								},
								success: function(data, status, xhr) {
									$('#progress').hide();
									if (data['status'] == 'success') {
										resetUserForm();
										$('#user-form-update').remove();
										window.location.href = '/';
									} else {
										$('#error-update').show();
										$('#error-update').empty();
										$('#error-update').html(data['err']);
										$('html, body').animate({scrollTop: 0}, 'fast');
									}
								},
								error: function(data, status, xhr) {
									$('#progress').hide();
									alert(status + "|" + xhr);
								}
							});
					} else {
						$('#error-update').show();
						$('#error-update').html('<span>Some of the fields are Empty or Unselected!</span>');
						$('html, body').animate({scrollTop: 0}, 'fast');
					}
			} else {
				$('#error-update').show();
				$('#error-update').html('<span>Email ID is not a valid Cisco email id!</span>');
				$('html, body').animate({scrollTop: 0}, 'fast');
			}
		} else {
			$('#error-update').show();
			$('#error-update').html('<span>Password does not match with Confirm Password!</span>');
			$('html, body').animate({scrollTop: 0}, 'fast');
		}
	});

	
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	$('#image-addlocation').click(function(event) {
		var action = 'display_container';
		var locationString = $(event.target).attr('id');
		xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/admin',
			type: 'POST',
			data: {
				username: "",
				locationString: locationString,
				action: action,
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
				$('#progress').show();
			},
			success: function(data, status, xhr) {
				$('#addlocation').show();
				$(event.target).removeAttr('disabled');
				$('#country').focus();
				$('#button-addlocation').val('Add');
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});

	$('#button-addlocation').click(function() {
		xsrf = getCookie("_xsrf");
		var admin_action = 	$('#button-addlocation').val();
		if (admin_action == 'Add') {
			var action = 'add';
		} else {
			var action = 'edit';
		}
		var oldlocation = $('#hidden').val();
		var locationString = $('#locationName').val();
		var country = $('#country').val();
		var gtmu = $('#gtmu').val();
		var region = $('#region').val();
		if ((locationString != null && locationString != "") && 
		(country != null && country != "") && 
		(gtmu != null && gtmu != "") && 
		(region != null && region != "")) {
			jQuery.ajax({
				url: '/admin/location',
				type: 'POST',
				data: {
					action : action,
					oldlocation : oldlocation,
					locationString : locationString,
					country : country,
					gtmu : gtmu,
					region : region,
					_xsrf: xsrf
				},
				dataType: 'json',
				beforeSend: function(xhr, settings) {
					$('#addlocation').hide();
					$('#progress').show();
				},
				success: function(data, status, xhr) {
					if (data['text'] == 'error') {
						alert(data['err']);
					} else {
						window.location.href = '/admin';
					}
					$('#progress').hide();
				},
				error: function(data, status, xhr) {
					alert(status + "|" + xhr);
				}
			});
		} else {
			$('#progress').hide();
			alert("!! Please fill in all the fields.");
		}
	});

	$('td.delete-cell-location').click(function(event) {
		var action = 'remove';
		var locationString = $(event.target).attr('id');
		xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/admin/location',
			type: 'POST',
			data: {
				username: "",
				locationString: locationString,
				action: action,
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$('#progress').show();
			},
			success: function(data, status, xhr) {
				if (data['text'] == 'error') {
					alert(data['err']);
				} else {
					window.location.href = '/admin';
				}
				$('#progress').hide();
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});
	
	$('td.edit-cell-location').click(function(event) {
		var action = 'fetch_location';
		var locationString = $(event.target).attr('id');
		xsrf = getCookie("_xsrf");
		jQuery.ajax({
			url: '/admin',
			type: 'POST',
			data: {
				username: '',
				locationString: locationString,
				action: action,
				_xsrf: xsrf
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				$(event.target).attr('disabled', 'disabled');
				$('#progress').show();
			},
			success: function(data, status, xhr) {
                $('#main-user-list').hide();
				$('#progress').hide();
				if (data['text'] == 'error') {
					alert(data['err']);
				} else {
					$('#addlocation').show();
					$(event.target).removeAttr('disabled');
					$('#hidden').val(data['locationString'])
					$('#country').focus();
					$('#country').val(data['country']);
					$('#gtmu').val(data['gtmu']);
					$('#locationName').val(data['location']);
					$('#region').val(data['region']);
					$('#addlocation h2').text('Update Location');
					$('#button-addlocation').val('Update');
				}
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
	});
	$('#button-cancel-location').click(function() {
        $('#main-user-list').show();
		$('#locationName').val('');
		$('#country').val('');
		$('#gtmu').val('');
		$('#region').val('');
		$('#addlocation').hide();
	});

	////////////////////////////////////////////////////////////////
	/*UPDATE USERS SELCTION CHANGE CONTROLLERS*/
	///////////////////////////////////////////////////////////////

	$('#location-option-update').change(function(event) {
		var xsrf = getCookie("_xsrf");
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
				$('#subscms-selectall-update').prop('checked', false);
				$('#gtmu-selectall-update').prop('checked', false);
				$('#region-selectall-update').prop('checked', false);
				$('#sl6-selectall-update').prop('checked', false);
				$('#salesagent-selectall-update').prop('checked', false);
				if (data['status'] == 'error') {
					alert("Some Error after Success!");
				} else {
					var listObj = data['sub_scms'];
					$('#subscms-option-update').find('option').remove();
					listObj.sort();
					for (i=0; i<listObj.length; i++) {
						var str = JSON.stringify(listObj[i]);
						str = str.replace(/\"/g, "");
						$('#subscms-option-update').append($('<option />').val(str).text(str));
					}
				}
			},
			error: function(data, status, xhr) {
				$('#progress').hide();
				alert(status + "|" + xhr);
			}
		});
		
		$('#subscms-selectall-update').change(function(event) {
			if ($(this).is(':checked')) {
				$('#subscms-option-update option').prop('selected', true) ;
				$('#subscms-option-update').trigger('change');
			} else {
				$('#subscms-option-update option').prop('selected', false) ;
				$('#gtmu-option-update').find('option').remove();
				$('#region-option-update').find('option').remove();
				$('#sl6-option-update').find('option').remove();
				$('#salesagent-option-update').find('option').remove();
			}
		});
		
		$('#gtmu-selectall-update').change(function(event) {
			if ($(this).is(':checked')) {
				$('#gtmu-option-update option').prop('selected', true) ;
				$('#gtmu-option-update').trigger('change');
			} else {
				$('#gtmu-option-update option').prop('selected', false) ;
				$('#region-option-update').find('option').remove();
				$('#sl6-option-update').find('option').remove();
				$('#salesagent-option-update').find('option').remove();
			}
		});

		$('#region-selectall-update').change(function(event) {
			if ($(this).is(':checked')) {
				$('#region-option-update option').prop('selected', true) ;
				$('#region-option-update').trigger('change');
			} else {
				$('#region-option-update option').prop('selected', false) ;
				$('#sl6-option-update').find('option').remove();
				$('#salesagent-option-update').find('option').remove();
			}
		});

		$('#sl6-selectall-update').change(function(event) {
			if ($(this).is(':checked')) {
				$('#sl6-option-update option').prop('selected', true) ;
				$('#sl6-option-update').trigger('change');
			} else {
				$('#sl6-option option').prop('selected', false) ;
				$('#salesagent-option').find('option').remove();
			}
		});

		$('#salesagent-selectall-update').change(function(event) {
			if ($(this).is(':checked')) {
				$('#salesagent-option-update option').prop('selected', true) ;
			} else {
				$('#salesagent-option-update option').prop('selected', false) ;
			}
		});

		$('#subscms-option-update').change(function(event) {
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
						$('#gtmu-option-update').find('option').remove();
						$('#region-option-update').find('option').remove();
						$('#sl6-option-update').find('option').remove();
						$('#salesagent-option-update').find('option').remove();
						for (i=0; i<listObj.length; i++) {
							listObj.sort();
							var str = JSON.stringify(listObj[i]);
							str = str.replace(/\"/g, "");
							$('#gtmu-option-update').append($('<option />').val(str).text(str));
						}
					}
				},
				error: function(data, status, xhr) {
					$('#progress').hide();
					alert(status + "|" + xhr);
				}
			});
		});

		
		$('#gtmu-option-update').change(function(event) {
			var gtmu = [];
			var sub_scms = [];
		
			$('#subscms-option-update option:selected').each(function(i, selected) {
				sub_scms[i] = $(selected).text();
			});
		
			$('#gtmu-option-update option:selected').each(function(i, selected) {
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
							$('#region-option-update').find('option').remove();
							$('#sl6-option-update').find('option').remove();
							$('#salesagent-option-update').find('option').remove();
							for (i=0; i<listObj.length; i++) {
								listObj.sort();
								var str = JSON.stringify(listObj[i]);
								str = str.replace(/\"/g, "");
								$('#region-option-update').append($('<option />').val(str).text(str));
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
		
		$('#region-option-update').change(function(event) {
			var gtmu = [];
			var sub_scms = [];
			var region = [];
		
			$('#subscms-option-update option:selected').each(function(i, selected) {
				sub_scms[i] = $(selected).text();
			});
		
			$('#gtmu-option-update option:selected').each(function(i, selected) {
				gtmu[i] = $(selected).text();
			});
		
			$('#region-option-update option:selected').each(function(i, selected) {
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
							$('#sl6-option-update').find('option').remove();
							for (i=0; i<listObj.length; i++) {
								listObj.sort();
								var str = JSON.stringify(listObj[i]);
								str = str.replace(/\"/g, "");
								$('#sl6-option-update').append($('<option />').val(str).text(str));
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
		
		$('#sl6-option-update').change(function(event) {
			var gtmu = [];
			var sub_scms = [];
			var region = [];
			var sl6 = [];
		
			$('#subscms-option-update option:selected').each(function(i, selected) {
				sub_scms[i] = $(selected).text();
			});
			$('#gtmu-option-update option:selected').each(function(i, selected) {
				gtmu[i] = $(selected).text();
			});
			$('#region-option-update option:selected').each(function(i, selected) {
				region[i] = $(selected).text();
			});
			$('#sl6-option-update option:selected').each(function(i, selected) {
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
							$('#salesagent-option-update').find('option').remove();
							for (i=0; i<listObj.length; i++) {
								listObj.sort();
								var str = JSON.stringify(listObj[i]);
								str = str.replace(/\"/g, "");
								str = str.replace(/,/g, "_|");
								$('#salesagent-option-update').append($('<option />').val(str).text(str));
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
		
		
		$('#userName-update').focus(function(event) {
			$('#span-exist-or-not-update').hide();
		});
		
		$('#userName-update').focusin(function(event) {
			$('#span-exist-or-not-update').hide();
		});

		$('#userName-update').focusout(function(event) {
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
							$('#span-exist-or-not-update').show();
							$('#img-exist-or-not-update').attr("src", "/static/icons/red_cross_mark.png");
							disableAllUserFormElements();
							$('#error-update').show();
							$('#error-update').html(data['err']);
							$('html, body').animate({scrollTop: 0}, 'fast');
						} else {
							$('#error-update').empty();
							$('#error-update').hide();
							enableAllUserFormElements();
							$('#span-exist-or-not-update').show();
							var listObj = data['locations'];
							$('#img-exist-or-not-update').attr("src", "/static/icons/green_tick2.png");
							$('#location-option-update').find('option').remove().end().append($('<option />').val('Select Option').text('Select Option'));
							for (i=0; i<listObj.length; i++) {
								var locationString = JSON.stringify(listObj[i]);
								locationString = locationString.replace(/\"/g, "");
								$('#location-option-update').append($('<option />').val(locationString).text(locationString));
							}
							$('#email-update').val(userID + '@cisco.com');
						}
					},
					error: function(data, status, xhr) {
						$('#progress').hide();
						alert(status + "|" + xhr);
					}
				});
			}
		});

		$('#reportingTo-update').focus(function(event) {
			$('span-rpt-exist-or-not').hide();
		});
		
		$('#reportingTo-update').focusin(function(event) {
			$('span-rpt-exist-or-not').hide();
		});

		
		$('#reportingTo-update').focusout(function(event) {
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
							$('#span-rpt-exist-or-not').show();
							$('#img-rpt-exist-or-not').attr("src", "/static/icons/red_cross_mark.png");
							disableAllUserFormElements();
							$('#error-update').show();
							$('#error-update').html(data['err']);
							$('submit-user-update').attr('disabled', 'disabled');
						} else {
							$('#error-update').empty();
							$('#error-update').hide();
							enableAllUserFormElements();
							$('#span-rpt-exist-or-not').show();
							$('#img-rpt-exist-or-not').attr("src", "/static/icons/green_tick2.png");
							$('submit-user-update').removeAttr('disabled');
						}
					},
					error: function(data, status, xhr) {
						$('#progress').hide();
						alert(status + "|" + xhr);
					}
				});
			}
		});

		
	});
	
});



function getCookie(name) {
	var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return c ? c[1] : undefined;
}

function requestAdminUserListStatus() {
	jQuery.getJSON('/admin/statususerlist', {session:""}, 
			function(data, status, xhr) {
				//alert("Call Finished!");
				window.location.href = '/admin';
				setTimeout(requestAdminUserListStatus, 0);
			}
	);
}

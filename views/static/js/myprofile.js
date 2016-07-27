$(document).ready(function() {
	var xsrf = getCookie("_xsrf");
	var pageName = document.location.href.match(/[^\/]+$/)[0];
	if (pageName == "myprofile") {
        fetchSelfData(xsrf, '/myprofile');
    }
	
	$('#myprofile-menubar').click(function(event) {
		var xsrf = getCookie("_xsrf");
		window.location.href = '/myprofile';
	});

    $('#myteam-menubar').click(function(event) {
        fetchAllUsersData(xsrf, '/myteam');
    });

});


function fetchSelfData(xsrf, url) {
	jQuery.ajax({
		url: url,
		type: 'POST',
		data: {
			_xsrf: xsrf,
            username: '',
            email: '',
            firstname: '',
            newpassword: '',
            action: 'get_userdata',
		},
		dataType: 'json',
		beforeSend: function(xhr, settings) {
            $('#left-panel-profile').show();
            $('#right-panel-profile').show();
		},
		success: function(data, status, xhr) {
			if (data['status'] == 'success') {
				$('#footer').show();
                $('#profile-menu-container-1').css({"background-color": "#5A5097","color": "white"});
                $('#myprofile-menubar').css({"color": "white"});
                displayUserProfile(data);

			} else {
                console.log("Data of fetchSelfData method does not have success as status");
			}
		},
		error: function(data, status, xhr) {
			$('#progress').hide();
			console.log(status + "|" + xhr);
		}
	});
}

function fetchAllUsersData(xsrf, url) {
	jQuery.ajax({
		url: url,
		type: 'POST',
		data: {
			_xsrf: xsrf,
		},
		dataType: 'json',
		beforeSend: function(xhr, settings) {
            $('#middle-panel-profile').empty();
		},
		success: function(data, status, xhr) {
			if (data['status'] == 'success') {
                alterMenuDecoration();
                displayMyTeam(data, xsrf);

			} else {
                console.log("Data of fetchSelfData method does not have success as status");
			}
		},
		error: function(data, status, xhr) {
			$('#progress').hide();
			console.log(status + "|" + xhr);
		}
	});
}



function displayMyTeam(data, xsrf) {
    var allUsers = data['allUsers'];
    var trID = ''; 
    var tableTDCSS = {
        "text-align":"left",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
        "padding-top" : "5%",
        "padding-left" : "15%",
        "padding-bottom" : "2%",
        "height" : "40%",
        "width" : "40%",
    };
    var tableTDRightCSS = {
        "text-align":"left",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
        "padding-top" : "2%",
        "padding-left" : "15%",
        "padding-bottom" : "2%",
        "height" : "40%",
        "width" : "40%",
    };
    var tableCSS = {
        "text-align":"left",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
        "width": "100%",
    };
    var anchorCSS = {
        "display":"block",
    };
    $('#middle-panel-profile').append('<div class="myteam-div-table" style="display: table; width: 100%; margin-top: 2%; font-size: 15px;">' + 
        '<div class="myteam-div-tablecell" id="table-container" style="display: table-cell; padding: 10px;"></div></div>');
    $('#table-container').append('<table class="myteam-table" id="myteam-table01"></table>');
    $('.myteam-table').css(tableCSS);
    for (var i=0; i<allUsers.length; i++) {
        if (i % 2 == 0) {
            trID = 'tr'+i;
            $('#myteam-table01').append('<tr class="myteam-tr" id="' + trID + '"></tr>');
        }
        var tdID = allUsers[i]["username"];
        $('#'+trID).append('<td class="myteam-td" id="' + tdID + '"></td>');
        $('#'+tdID).append('<a href="#" class="anchor-myteam-img" id="' + allUsers[i]["username"] + '">' + 
            '<img class="myteam-img" id="' + allUsers[i]["username"] + '" src="http://localhost:8000/static/icons/menu_icon_072.png" alt="Loading..." />' +
            '<span class="myteam-span" id="' + allUsers[i]["username"] + '" style="margin-left: 2%">' + allUsers[i]["firstname"] + ' ' + allUsers[i]["lastname"] + '</span></a>');
        if (i % 2 == 0) {
            $('#'+tdID).css(tableTDCSS);
        } else {
            $('#'+tdID).css(tableTDRightCSS);
        }
    }


    $('.myteam-td').click(function(event) {
		var username = $(event.target).attr('id');
        jQuery.ajax({
            url: '/comrade',
            type: 'POST',
            data: {
                _xsrf: xsrf,
                comrade: username,
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
            },
            success: function(data, status, xhr) {
                if (data['status'] == 'success') {
                    window.location.href = '/main';
                } else {
                    console.log("Success from service does not have success as status");
                }
            },
            error: function(data, status, xhr) {
                //console.log(status + "|" + xhr);
            }
        });
    });
}

function displayUserProfile(data) {
    var divMid = '#middle-panel-profile';
    var divUsernameContainerID = 'div-table-username';
    var divUsernameID = 'div-username';
    var tableID = 'table-profile';
    var trID1 = 'tr-username';
    var trID1_0 = 'tr-username-data';
    var trID1_1 = 'tr-email-data';
    var trID1_2 = 'tr-firstname-data';
    var trID1_3 = 'tr-lastname-data';
    var trID1_4 = 'tr-buttons';
    var tdUsernameLabelID = 'td-username-label';
    var tdUsernameDataID = 'td-username-data';
    var tdUsernameEditID = 'td-username-edit';
    var divUsernameDataID = 'div-username-data';
    var divUsernameDataHeaderID = 'div-username-data-header';
    var divUsernameDataDetailID = 'div-username-data-detail';



    var divPasswordContainerID = 'div-table-password';
    var divPasswordID = 'div-password';
    var tableID2 = 'table-profile2';
    var trID2 = 'tr-password';
    var trID2_0 = 'tr-oldpassword-data';
    var trID2_1 = 'tr-newpassword-data';
    var trID2_2 = 'tr-confirmpassword-data';
    var trID2_3 = 'tr-buttons2';
    var tdPasswordLabelID = 'td-password-label';
    var tdPasswordDataID = 'td-password-data';
    var tdPasswordEditID = 'td-password-edit';
    var divPasswordDataID = 'div-password-data';
    var divPasswordDataHeaderID = 'div-password-data-header';
    var divPasswordDataDetailID = 'div-password-data-detail';

    var tableTDCSS = {
        "text-align":"center",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
    };
    var tableTDLabelCSS = {
        "text-align":"left",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
        "color" : "black",
        "font-weight" : "bold",
        "vertical-align" : "top",
        "padding-left" : "15px",
    };
    var tableCSS = {
        "text-align":"center",
        "vertical-align":"middle",
        "border" : "none",
        "border-spacing" : "0",
        "border-collapse" : "collapse",
        "width": "100%",
    };
    var tdUsernameLabelCSS = {
        "text-align":"left",
        "width":"20%",
    };
    var tdUsernameDataCSS = {
        "text-align":"center",
        "width":"70%",
    };
    var tdUsernameEditCSS = {
        "text-align":"center",
        "width":"10%",
    };
    var divMidCSS = {
        "font-size":"10px",
        "color" : "grey",
        "background" : "#EEEEEE",
    };

    $(divMid).css(divMidCSS);
    // ===========================================================================
    // ===========================================================================
    // Add Username Container
    $(divMid).append('<div class="table-container" id="' + divUsernameContainerID + '" style="display: table; width: 100%; margin-top: 2%;"></div>');
    $(divMid).append('<div class="table-container" id="' + divPasswordContainerID + '" style="display: table; width: 100%; margin-top: 2%;"></div>');
    // ===========================================================================
    // ===========================================================================


    // ===========================================================================
    // ===========================================================================
    // Add Username Sub Container
    $('#'+divUsernameContainerID).append('<div class="my-profile" id="' + divUsernameID + '" style="display: table-cell; padding: 10px;"></div>');
    $('#'+divPasswordContainerID).append('<div class="my-profile" id="' + divPasswordID + '" style="display: table-cell; padding: 10px;"></div>');
    // Add Table to contain the Data Structure Body
    $('#'+divUsernameID).append('<table class="profile-table" id="' + tableID + '"></table>');
	$('#'+divUsernameID).append('<div class="" id="error-username" style="display: none; color:  red"></div>');
	$('#'+divUsernameID).append('<div class="progress-bar-profile" id="progress-save-username" style="display: none"><img class="loading-img" src="http://localhost:8000/static/icons/loading11.gif" alt="Loading..." height="100" width="80" /></div>');
    $('#'+tableID).append('<tr class="tr-profile" id="' + trID1 + '"></tr>');
    $('#'+trID1).append('<td class="td-profile-label" id="' + tdUsernameLabelID + '">Username</td>');
    $('#'+trID1).append('<td class="td-profile" id="' + tdUsernameDataID + '"></td>');
    $('#'+trID1).append('<td class="td-profile" id="' + tdUsernameEditID + '"></td>');

    $('#'+divPasswordID).append('<table class="profile-table2" id="' + tableID2 + '"></table>');
	$('#'+divPasswordID).append('<div class="" id="error-password" style="display: none; color:  red"></div>');
	$('#'+divPasswordID).append('<div class="progress-bar-profile" id="progress-save-password" style="display: none"><img class="loading-img" src="http://localhost:8000/static/icons/loading11.gif" alt="Loading..." height="100" width="80" /></div>');
    $('#'+tableID2).append('<tr class="tr-profile" id="' + trID2 + '"></tr>');
    $('#'+trID2).append('<td class="td-profile-label2" id="' + tdPasswordLabelID + '">Password</td>');
    $('#'+trID2).append('<td class="td-profile" id="' + tdPasswordDataID + '"></td>');
    $('#'+trID2).append('<td class="td-profile" id="' + tdPasswordEditID + '"></td>');

    // Add Structure to contain the ACTUAL data
    $('#'+tdUsernameDataID).append('<div class="my-profile" id="' + divUsernameDataID+ '"></div>');
    $('#'+tdUsernameEditID).append('<a href="#" id="anchor-username-edit">Edit</a>');
    $('#'+divUsernameDataID).append('<div class="my-profile-data" id="' + divUsernameDataHeaderID+ '"></div>');
    $('#'+divUsernameDataID).append('<div class="my-profile-data" id="' + divUsernameDataDetailID+ '" style="display: none"></div>');

    $('#'+divUsernameDataHeaderID).append(data['firstname'] + " " + data['lastname']);
    $('#'+divUsernameDataDetailID).append('<p>Edit Username</p>');

    
    $('#'+tdPasswordDataID).append('<div class="my-profile" id="' + divPasswordDataID+ '"></div>');
    $('#'+tdPasswordEditID).append('<a href="#" id="anchor-password-edit">Edit</a>');
    $('#'+divPasswordDataID).append('<div class="my-profile-data" id="' + divPasswordDataHeaderID+ '"></div>');
    $('#'+divPasswordDataID).append('<div class="my-profile-data" id="' + divPasswordDataDetailID+ '" style="display: none"></div>');

    $('#'+divPasswordDataHeaderID).append('Your secret phrase to gain admission to TrueNorth');
    $('#'+divPasswordDataDetailID).append('<p>Edit Password</p>');


    //Add CSS to all sub container elements
    
    //Add CSS to all sub container elements
    $('.td-profile').css(tableTDCSS);
    $('#'+tdUsernameLabelID).css(tdUsernameLabelCSS);
    $('#'+tdUsernameEditID).css(tdUsernameEditCSS);
    $('#'+tdUsernameDataID).css(tdUsernameDataCSS);
    $('#'+tdPasswordLabelID).css(tdUsernameLabelCSS);
    $('#'+tdPasswordEditID).css(tdUsernameEditCSS);
    $('#'+tdPasswordDataID).css(tdUsernameDataCSS);

    $('.profile-table').css(tableCSS);
    $('#anchor-username-edit').css({"text-decoration": "none !important", "color" : "grey"});
    $('#anchor-username-edit').css({"border-bottom": "1px solid grey"});
    $('#'+divUsernameID).css("border-bottom", "1px solid grey");
    $('.td-profile-label').css(tableTDLabelCSS);

    $('.profile-table2').css(tableCSS);
    $('#anchor-password-edit').css({"text-decoration": "none !important", "color" : "grey"});
    $('#anchor-password-edit').css({"border-bottom": "1px solid grey"});
    $('#'+divPasswordID).css("border-bottom", "1px solid grey");
    $('.td-profile-label2').css(tableTDLabelCSS);

    $('#'+divUsernameDataDetailID).append('<div class="data-table-container" id="user-data-table-container" style="display: table; width: 100%"></div>');
    $('#user-data-table-container').append('<div class="data-table" id="user-data-table-subcontainer" style="display: table-cell"></div>');
    $('#user-data-table-subcontainer').append('<table class="data-table" id="user-data-table" style="width: 100%"></table>');
    $('#user-data-table').append('<tr class="tr-profile" id="' + trID1_0 + '"></tr>');
    $('#user-data-table').append('<tr class="tr-profile" id="' + trID1_1 + '"></tr>');
    $('#user-data-table').append('<tr class="tr-profile" id="' + trID1_2 + '"></tr>');
    $('#user-data-table').append('<tr class="tr-profile" id="' + trID1_3 + '"></tr>');
    $('#user-data-table').append('<tr class="tr-profile" id="' + trID1_4 + '"></tr>');
    $('#'+trID1_0).append('<td class="td-profile" id="td-label-username" style="text-align: right"><label for="labelUserName">Username:</label></td>');
    $('#'+trID1_0).append('<td class="td-profile" id="td-text-username" style="text-align: left"><input class="input-text" id="input-username-text" type="text" name="userName" value="' + data['username'] + '"/></td>');
    $('#'+trID1_1).append('<td class="td-profile" id="td-label-email" style="text-align: right"><label for="labelEmailID">EmailID:</label></td>');
    $('#'+trID1_1).append('<td class="td-profile" id="td-text-email" style="text-align: left"><input class="input-text" id="input-email-text" type="text" name="emailID" value="' + data['email'] + '"/></td>');
    $('#'+trID1_2).append('<td class="td-profile" id="td-label-firstname" style="text-align: right"><label for="labelLastName">First Name:</label></td>');
    $('#'+trID1_2).append('<td class="td-profile" id="td-text-firstname" style="text-align: left"><input class="input-text" id="input-firstname-text" type="text" name="firstName" value="' + data['firstname'] + '"/></td>');
    $('#'+trID1_3).append('<td class="td-profile" id="td-label-lastname" style="text-align: right"><label for="labelLastName">Last Name:</label></td>');
    $('#'+trID1_3).append('<td class="td-profile" id="td-text-lastname" style="text-align: left"><input class="input-text" id="input-lastname-text" type="text" name="lastName" value="' + data['lastname'] + '"/></td>');

    $('#'+trID1_4).append('<td class="td-profile" id="td-button-save-username" style="text-align: right"><input type="button" id="save-changes-username" name="save-changes-username" value="Save Changes" /></td>');
    $('#'+trID1_4).append('<td class="td-profile" id="td-button-cancel-username" style="text-align: left"><input type="button" id="cancel-username" name="cancel-username" value="Cancel" /></td>');




    $('#'+divPasswordDataDetailID).append('<div class="data-table-container" id="password-data-table-container" style="display: table; width: 100%"></div>');
    $('#password-data-table-container').append('<div class="data-table" id="password-data-table-subcontainer" style="display: table-cell"></div>');
    $('#password-data-table-subcontainer').append('<table class="data-table" id="password-data-table" style="width: 100%"></table>');
    $('#password-data-table').append('<tr class="tr-profile" id="' + trID2_0 + '"></tr>');
    $('#password-data-table').append('<tr class="tr-profile" id="' + trID2_1 + '"></tr>');
    $('#password-data-table').append('<tr class="tr-profile" id="' + trID2_2 + '"></tr>');
    $('#password-data-table').append('<tr class="tr-profile" id="' + trID2_3 + '"></tr>');
    $('#'+trID2_0).append('<td class="td-profile" id="td-label-oldpassword" style="text-align: right"><label for="labelOldPassword">Old Password:</label></td>');
    $('#'+trID2_0).append('<td class="td-profile" id="td-text-oldpassword" style="text-align: left"><input class="input-text" id="input-oldpassword-text" type="password" name="oldPassword" value=""/></td>');
    $('#'+trID2_1).append('<td class="td-profile" id="td-label-newpassword" style="text-align: right"><label for="labelNewPassword">New Password:</label></td>');
    $('#'+trID2_1).append('<td class="td-profile" id="td-text-newpassword" style="text-align: left"><input class="input-text" id="input-newpassword-text" type="password" name="newPassword" value=""/></td>');
    $('#'+trID2_2).append('<td class="td-profile" id="td-label-confirmpassword" style="text-align: right"><label for="labelConfirmPassword">Confirm Password:</label></td>');
    $('#'+trID2_2).append('<td class="td-profile" id="td-text-confirmpassword" style="text-align: left"><input class="input-text" id="input-confirmpassword-text" type="password" name="confirmPassword" value=""/></td>');

    $('#'+trID2_3).append('<td class="td-profile" id="td-button-save-password" style="text-align: right"><input type="button" id="save-changes-password" name="save-changes-password" value="Save Changes" /></td>');
    $('#'+trID2_3).append('<td class="td-profile" id="td-button-cancel-password" style="text-align: left"><input type="button" id="cancel-password" name="cancel-password" value="Cancel" /></td>');


    $('.input-text').css({"padding" : "2px 1px 2px 5px"});


    // ================================================================================
    // ================================================================================
    // Event Handlers
    $('#anchor-username-edit').click(function() {
        $('#input-username-text').attr('disabled', 'disabled');
        $('#input-email-text').attr('disabled', 'disabled');
        $('#'+divUsernameDataHeaderID).hide();
        $('#'+divUsernameDataDetailID).show();
        $('.td-profile-label').css("vertical-align", "top");
        $('#anchor-username-edit').hide();
        $('.profile-table').css("background", "#FFFFFF");
    });

    $('#td-button-cancel-username').click(function() {
        $('#error-username').hide();
        $('#'+divUsernameDataHeaderID).show();
        $('#'+divUsernameDataDetailID).hide();
        $('.td-profile-label').css("vertical-align", "middle");
        $('#anchor-username-edit').show();
        $('.profile-table').css("background", "#EEEEEE");
    });


    $('#input-firstname-text').focus(function() {
        $('#td-button-save-username').removeAttr('disabled');
    });
    $('#input-firstname-text').focusin(function() {
        $('#td-button-save-username').removeAttr('disabled');
    });
    $('#input-lastname-text').focus(function() {
        $('#td-button-save-username').removeAttr('disabled');
    });
    $('#input-lastname-text').focusin(function() {
        $('#td-button-save-username').removeAttr('disabled');
    });

    $('#td-button-save-username').click(function() {
        var username = $('#input-username-text').val();
        var email = $('#input-email-text').val();
        var firstname = $('#input-firstname-text').val();
        var lastname = $('#input-lastname-text').val();
        if ((firstname) && (firstname.length != 0) && (lastname) && (lastname.length != 0)) {
            $('#error-username').hide();
            jQuery.ajax({
                url: '/myprofile',
                type: 'POST',
                data: {
                    _xsrf: '',
                    username: username,
                    email: email,
                    firstname: firstname,
                    lastname: lastname,
                    oldpassword: '',
                    newpassword: '',
                    action: 'save_username',
                },
                dataType: 'json',
                beforeSend: function(xhr, settings) {
                    $('#progress-save-username').show();
                },
                success: function(data, status, xhr) {
                    $('#progress-save-username').hide();
                    if (data['status'] == 'success') {
                        $('#td-button-save-username').attr('disabled', 'disabled');
                        $('#error-username').css("color", "blue");
                        $('#error-username').show();
                    } else {
                        $('#error-username').css("color", "red");
                        $('#error-username').show();
                        $('#error-username').html('No success');
                        console.log("Data of Saving method does not have success as status");
                    }
                },
                error: function(data, status, xhr) {
                    $('#progress-save-username').hide();
                    console.log(status + "|" + xhr);
                }
            });
        } else {
            $('#error-username').css("color", "red");
            $('#error-username').show();
            $('#error-username').html('Some of the fields are empty');
        }
    });



    $('#input-oldpassword-text').focus(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });
    $('#input-oldpassword-text').focusin(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });
    $('#input-newpassword-text').focus(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });
    $('#input-newpassword-text').focusin(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });
    $('#input-confirmpassword-text').focus(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });
    $('#input-confirmpassword-text').focusin(function() {
        $('#td-button-save-password').removeAttr('disabled');
    });

    $('#td-button-save-password').click(function() {
        var old_password = $('#input-oldpassword-text').val();
        var new_password = $('#input-newpassword-text').val();
        var confirm_password = $('#input-confirmpassword-text').val();
        if ((old_password) && (old_password.length != 0) && (new_password) && (new_password.length != 0) && 
            (confirm_password) && (confirm_password.length != 0)) {
                if (new_password == confirm_password) {
                    if (old_password != new_password) {
                        jQuery.ajax({
                            url: '/myprofile',
                            type: 'POST',
                            data: {
                                _xsrf: '',
                                username: '',
                                email: '',
                                firstname: '',
                                oldpassword: old_password,
                                newpassword: new_password,
                                action: 'save_password',
                            },
                            dataType: 'json',
                            beforeSend: function(xhr, settings) {
                                $('#progress-save-password').show();
                            },
                            success: function(data, status, xhr) {
                                $('#progress-save-password').hide();
                                if (data['status'] == 'success') {
                                    $('#td-button-save-password').attr('disabled', 'disabled');
                                    $('#error-password').css("color", "blue");
                                    $('#error-password').show();
                                    $('#error-password').html('New Password has been updated');
                                } else {
                                    $('#error-password').show();
                                    $('#error-password').css("color", "red");
                                    $('#error-password').html('Incorrect Old Password');
                                }
                            },
                            error: function(data, status, xhr) {
                                $('#progress-save-password').hide();
                                console.log(status + "|" + xhr);
                            }
                        });
                    } else {
                        $('#error-password').show();
                        $('#error-password').css("color", "red");
                        $('#error-password').html('Old and New Passwords are Same');
                    }
                } else {
                    $('#error-password').show();
                    $('#error-password').css("color", "red");
                    $('#error-password').html('New and Confirm Passwords are not matching');
                }
        } else {
            $('#error-password').show();
            $('#error-password').css("color", "red");
            $('#error-password').html('Some of the fields are empty');
        }
    });

    $('#anchor-password-edit').click(function() {
        $('#'+divPasswordDataHeaderID).hide();
        $('#'+divPasswordDataDetailID).show();
        $('.td-profile-label2').css("vertical-align", "top");
        $('#anchor-password-edit').hide();
        $('.profile-table2').css("background", "#FFFFFF");
    });

    $('#td-button-cancel-password').click(function() {
        $('#error-password').hide();
        $('#'+divPasswordDataHeaderID).show();
        $('#'+divPasswordDataDetailID).hide();
        $('.td-profile-label2').css("vertical-align", "middle");
        $('#anchor-password-edit').show();
        $('.profile-table2').css("background", "#EEEEEE");
        $('#input-oldpassword-text').val('');
        $('#input-newpassword-text').val('');
        $('#input-confirmpassword-text').val('');
    });
    // ================================================================================
    // ================================================================================

} // End of displayUserProfile function


function alterMenuDecoration() {
    $('#profile-menu-container-1').css({
        "overflow-x" : "auto",
        "overjlow-y" : "auto",
        "margin-bottom" : "2%",
        "margin-left" : "5%",
        "border-style": "none",
        "background-color": "#EEEEEE",
        "font-weight": "normal",
        "text-align": "left",
        "padding": "0.5em 0.5em 0.5em 0.5em",
    });
    $('#myprofile-menubar').css({
        "text-decoration" : "none", 
        "background-color": "#EEEEEE",
        "color": "#696969",
        "padding": "0",
    });
    $('#profile-menu-container-1').hover(function(){
        $('#profile-menu-container-1').css({
            "background-color":"#5A5097",
            "color": "white",
        });
        $('#myprofile-menubar').css({
            "background-color":"#5A5097",
            "color": "white",
        });
    }, function() {
        $('#profile-menu-container-1').css({
            "overflow-x" : "auto",
            "overjlow-y" : "auto",
            "margin-bottom" : "2%",
            "margin-left" : "5%",
            "border-style": "none",
            "background-color": "#EEEEEE",
            "font-weight": "normal",
            "text-align": "left",
            "padding": "0.5em 0.5em 0.5em 0.5em",
        });
        $('#myprofile-menubar').css({
            "text-decoration" : "none", 
            "background-color": "#EEEEEE",
            "color": "#696969",
            "padding": "0",
        });
    });
    $('#myprofile-menubar').hover(function(){
        $('#profile-menu-container-1').css({
            "background-color":"#5A5097",
            "color": "white",
        });
        $(this).css({
            "background-color":"#5A5097",
            "color": "white",
        });
    }, function() {
        $('#profile-menu-container-1').css({
            "overflow-x" : "auto",
            "overjlow-y" : "auto",
            "margin-bottom" : "2%",
            "margin-left" : "5%",
            "border-style": "none",
            "background-color": "#EEEEEE",
            "font-weight": "normal",
            "text-align": "left",
            "padding": "0.5em 0.5em 0.5em 0.5em",
        });
        $('#myprofile-menubar').css({
            "text-decoration" : "none", 
            "background-color": "#EEEEEE",
            "color": "#696969",
            "padding": "0",
        });
    });
    $('#profile-menu-container-2').css({"background-color": "#5A5097","color": "white"});
    $('#myteam-menubar').css({"color": "white"});
}



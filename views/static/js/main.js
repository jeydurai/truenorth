$(document).ready(function() {
    $('#news-ticker').telex({
        messages: [{
                id: 'msg1',
                content: 'Finance Booking Data is upto FY16H1 from FY11',
                class: 'news-1'
        }]
    });
	var xsrf = getCookie("_xsrf");
	var pageName = document.location.href.match(/[^\/]+$/)[0];
	if (pageName == "main") {
        fetchData(xsrf, '/home');
	} else if (pageName == "product") {
        fetchData(xsrf, '/home-product');
	} else if (pageName == "service") {
        fetchData(xsrf, '/home-service');
	} else if (pageName == "comrade") {
        fetchData(xsrf, '/home');
    }
	
	$('#home').click(function(event) {
		var xsrf = getCookie("_xsrf");
        jQuery.ajax({
            url: '/refresh-session',
            type: 'POST',
            data: {
                _xsrf: xsrf,
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


	$('#prod-ser').click(function(event) {
		var xsrf = getCookie("_xsrf");
		window.location.href = '/main';
	});
	$('#product').click(function(event) {
		var xsrf = getCookie("_xsrf");
		window.location.href = '/product';
	});
	$('#service').click(function(event) {
		var xsrf = getCookie("_xsrf");
		window.location.href = '/service';
	});

	$('#unhide-inactive-menu').click(function(event) {
        $('#inactive').show();
        $('#minimize-button').show();
        $('#maximize-button').hide();
	});
	$('#hide-inactive-menu').click(function(event) {
        $('#inactive').hide();
        $('#minimize-button').hide();
        $('#maximize-button').show();
	});

});

$(window).scroll(function() {   
    if($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
        var xsrf = getCookie("_xsrf");
        var pageName = document.location.href.match(/[^\/]+$/)[0];
        if (pageName == "main") {
            fetchData(xsrf, '/home');
        } else if (pageName == "product") {
            fetchData(xsrf, '/home-product');
        } else if (pageName == "service") {
            fetchData(xsrf, '/home-service');
        } else if (pageName == "comrade") {
            fetchData(xsrf, '/home');
        }
    }
});


function fetchData(xsrf, url) {
	jQuery.ajax({
		url: url,
		type: 'POST',
		data: {
			_xsrf: xsrf,
		},
		dataType: 'json',
		beforeSend: function(xhr, settings) {
			$('#progress').show();
            $('#left-panel-main').show();
            $('#right-panel-main').show();
		},
		success: function(data, status, xhr) {
			$('#progress').hide();
			if (data['status'] == 'success') {
				$('#footer').show();
                if (data['what_display'] == 'product') {
                    $('#menu-container-1').css({"background-color": "#5A5097","color": "white"});
                    $('#product').css({"color": "white"});
                } else if (data['what_display'] == 'service') {
                    $('#menu-container-2').css({"background-color": "#5A5097","color": "white"});
                    $('#service').css({"color": "white"});
                } else {
                    $('#menu-container-0').css({"background-color": "#5A5097","color": "white"});
                    $('#prod-ser').css({"color": "white"});
                    $('#menu-container-1').css({"text-decoration": "none"});
                    $('#menu-container-2').css({"text-decoration": "none"});
                    if (data['round_count'] != 0) {
                        $('#product').css({"color": "black"});
                        $('#service').css({"color": "black"});
                    }
                }
                if (data['round_count'] == 0) {
                    $('#middle-panel-main').show();
                    drawRightPanel(data);
                }
				drawMiddlePanel(data);
			} else {
				//alert(data['err']);
			}
		},
		error: function(data, status, xhr) {
			$('#progress').hide();
			alert(status + "|" + xhr);
		}
	});
}


function drawMiddlePanel(data) {
	var container_header = data['container_header'];
	var paneCSS = {
		"margin-left" : "2.2%",
		"margin-bottom" : "1.5%",
		"height" : "20em",
		"width" : "30%",
		"float" : "left",
		"background-color" : "#FFFFFF",
		"box-shadow": "10px 10px 5px #888888"
	};

	var paneCSSExpanded = {
			"margin-left" : "2.2%",
			"margin-bottom" : "1.5%",
			"height" : "20em",
			"width" : "95%",
			"float" : "left",
			"background-color" : "#FFFFFF",
			"box-shadow": "10px 10px 5px #888888"
		};

	var paneCSSExpanded2 = {
			"margin-left" : "2.2%",
			"margin-bottom" : "1.5%",
			"height" : "20em",
			"width" : "60%",
			"float" : "left",
			"background-color" : "#FFFFFF",
			"box-shadow": "10px 10px 5px #888888"
		};

	var subContainerCSS = {
		"overflow-x" : "auto",
		"overflow-y" : "auto",
		"margin-bottom" : "2%",
		"border-color": "#EEEEEE",
		"border-width": "2px",
		"border-style": "dashed",
		"background-color": "#FFFFFF",
	};
	
	var headerCSS = {
		"margin-bottom" : "1%",
		"padding-top" : "1%",
		"color" : "#5A5097",
	};
	
    var containerNo = data['container_no'];
	var subContainerID = 'sub-container' + containerNo;
	var containerHeaderID = 'header' + containerNo;
	var progressBarID = "progress-middle" + containerNo;
    var howManyCharts = data['how_many_charts'];
    var oneBeforeLastChart = howManyCharts-1;
    console.log("Total Chart: " + howManyCharts);
    console.log("Last Chart No.: " + oneBeforeLastChart);

	$('#middle-panel-main').append('<div class="sub-container" id="' + subContainerID + '"></div>');
	$('#' + subContainerID).append('<h4 class="sub-container-header" id="' + containerHeaderID + '">' + container_header + '</h4><hr/>');
	$('#' + subContainerID).append('<div class="progress-bar2" id="' + progressBarID + '" style="display: none"><img class="loading-img" src="http://localhost:8000/static/icons/loading11.gif" alt="Loading..." height="100" width="80" /></div>');
	for (i=0; i<howManyCharts; i++) {
		var imageID = "loading-img" + containerNo + "-" + i;
		var chartPaneID = "pane" + containerNo + "-" + i;
		if (i === oneBeforeLastChart) {
			$('#' + subContainerID).append('<div class="chart-pane-expanded" id="' + chartPaneID + '" style="display: none"></div>');
		/*} else if (i === 4) {
			$('#' + subContainerID).append('<div class="chart-pane-expanded2" id="' + chartPaneID + '" style="display: none"></div>');*/
		} else {
			$('#' + subContainerID).append('<div class="chart-pane" id="' + chartPaneID + '" style="display: none"></div>');
		}
		$('#' + progressBarID).css({ "z-index" : "100" });
	}
	$('.sub-container').css(subContainerCSS);
	$('.sub-container-header').css(headerCSS);
	$('.chart-pane').css(paneCSS);
	$('.chart-pane-expanded').css(paneCSSExpanded);
//	$('.chart-pane-expanded2').css(paneCSSExpanded2);
    $('#' + progressBarID).hide();
    var paneID = '#pane' + containerNo + '-';

    var chartDisplayConfig = data['chart_display_config'];
    var chartDictArray = prepareMiddlePanelOrder();
    var middlePanelCharts = [];
    for (var i=0; i<chartDictArray.length; i++) {
        chartDict = chartDictArray[i];
        key = chartDict['whatChart'];
        if (chartDisplayConfig[key] == 1) middlePanelCharts.push(chartDict['chartFunction']);
    }
    
    //var middlePanelCharts = prepareMiddlePanelOrder();
    for (var i=0; i<middlePanelCharts.length; i++) {
        middlePanelCharts[i](data, paneID + i); //callback function
    }
}


function drawRightPanel(data) {
    var chartDisplayConfig2 = data['chart_display_config2'];
	var container_header = 'YoY-Booking';

	var paneCSSExpanded = {
			"margin-left" : "2.2%",
			"margin-bottom" : "1.5%",
			"height" : "7em",
            "width" : "20%",
			"float" : "left",
			"background-color" : "#FFFFFF",
		};

	var subContainerCSS = {
		"overflow-x" : "auto",
		"overflow-y" : "auto",
		"margin-bottom" : "2%",
		"border-color": "#EEEEEE",
		"border-width": "2px",
		"border-style": "dashed",
		"background-color": "#FFFFFF",
	};
	
	var headerCSS = {
		"margin-bottom" : "1%",
		"padding-top" : "1%",
		"color" : "#5A5097",
	};
	
    var containerNo = "1";
	var subContainerID = 'right-sub-container' + containerNo;
	var containerHeaderID = 'header' + containerNo;
	var progressBarID = "progress-right" + containerNo;
	$('#right-panel-main').append('<div class="right-sub-container" id="' + subContainerID + '"></div>');
	$('#' + subContainerID).append('<h4 class="right-sub-container-header" id="' + containerHeaderID + '">' + container_header + '</h4><hr/>');
	for (i=0; i<25; i++) {
		var imageID = "loading-img" + containerNo + "-" + i;
		var chartPaneID = "right-pane" + containerNo + "-" + i;
        $('#' + subContainerID).append('<div class="right-chart-pane-expanded" id="' + chartPaneID + '" style="display: none"></div>');
	}
	$('.right-sub-container').css(subContainerCSS);
	$('.right-sub-container-header').css(headerCSS);
	$('.right-chart-pane-expanded').css(paneCSSExpanded);
   
    if (chartDisplayConfig2['td_booking'] == 1) displayYoYGauge(data['growth_data']['td_booking'], '#right-pane' + containerNo + '-' + '0');
    if (chartDisplayConfig2['ent_nw'] == 1) displayYoYGauge(data['growth_data']['ent_nw'], '#right-pane' + containerNo + '-' + '1');
    if (chartDisplayConfig2['security'] == 1) displayYoYGauge(data['growth_data']['security'], '#right-pane' + containerNo + '-' + '2');
    if (chartDisplayConfig2['collab'] == 1) displayYoYGauge(data['growth_data']['collab'], '#right-pane' + containerNo + '-' + '3');
    if (chartDisplayConfig2['dcv'] == 1) displayYoYGauge(data['growth_data']['dcv'], '#right-pane' + containerNo + '-' + '4');
    if (chartDisplayConfig2['switching'] == 1) displayYoYGauge(data['growth_data']['switching'], '#right-pane' + containerNo + '-' + '5');
    if (chartDisplayConfig2['wireless'] == 1) displayYoYGauge(data['growth_data']['wireless'], '#right-pane' + containerNo + '-' + '6');
    if (chartDisplayConfig2['ucs'] == 1) displayYoYGauge(data['growth_data']['ucs'], '#right-pane' + containerNo + '-' + '7');
    if (chartDisplayConfig2['routing'] == 1) displayYoYGauge(data['growth_data']['routing'], '#right-pane' + containerNo + '-' + '8');
    if (chartDisplayConfig2['ts'] == 1) displayYoYGauge(data['growth_data']['ts'], '#right-pane' + containerNo + '-' + '9');
    if (chartDisplayConfig2['as'] == 1) displayYoYGauge(data['growth_data']['as'], '#right-pane' + containerNo + '-' + '10');
    if (chartDisplayConfig2['mfg'] == 1) displayYoYGauge(data['growth_data']['mfg'], '#right-pane' + containerNo + '-' + '11');
    if (chartDisplayConfig2['edu'] == 1) displayYoYGauge(data['growth_data']['edu'], '#right-pane' + containerNo + '-' + '12');
    if (chartDisplayConfig2['ecom'] == 1) displayYoYGauge(data['growth_data']['ecom'], '#right-pane' + containerNo + '-' + '13');
    if (chartDisplayConfig2['at_attach'] == 1) displayYoYGauge(data['growth_data']['at_attach'], '#right-pane' + containerNo + '-' + '14');
    if (chartDisplayConfig2['select'] == 1) displayYoYGauge(data['growth_data']['select'], '#right-pane' + containerNo + '-' + '15');
    if (chartDisplayConfig2['mm'] == 1) displayYoYGauge(data['growth_data']['mm'], '#right-pane' + containerNo + '-' + '16');
    if (chartDisplayConfig2['geo_n'] == 1) displayYoYGauge(data['growth_data']['geo_n'], '#right-pane' + containerNo + '-' + '17');
    if (chartDisplayConfig2['geo_nn'] == 1) displayYoYGauge(data['growth_data']['geo_nn'], '#right-pane' + containerNo + '-' + '18');
    if (chartDisplayConfig2['product'] == 1) displayYoYGauge(data['growth_data']['product'], '#right-pane' + containerNo + '-' + '19');
    if (chartDisplayConfig2['service'] == 1) displayYoYGauge(data['growth_data']['service'], '#right-pane' + containerNo + '-' + '20');
  /*
  * Create Another Level of YoY Charts
  * */

    // Draw Discount YoY charts
	paneCSSExpanded = {
			"margin-left" : "2.2%",
			"margin-bottom" : "1.5%",
			"height" : "7em",
            "width" : "20%",
			"float" : "left",
			"background-color" : "#FFFFFF",
		};

	subContainerCSS = {
		"overflow-x" : "auto",
		"overflow-y" : "auto",
		"margin-bottom" : "2%",
		"border-style": "none",
		"background-color": "#FFFFFF",
	};
	
	headerCSS = {
		"margin-bottom" : "1%",
		"padding-top" : "1%",
		"color" : "#5A5097",
	};

	container_header = 'YoY-Avg. Discount';
    containerNo = "2";
	subContainerID = 'right-sub-container' + containerNo;
	containerHeaderID = 'header' + containerNo;
	progressBarID = "progress-right" + containerNo;
	$('#right-panel-main').append('<div class="right-sub-container" id="' + subContainerID + '"></div>');
	$('#' + subContainerID).append('<h4 class="right-sub-container-header" id="' + containerHeaderID + '">' + container_header + '</h4><hr/>');
	for (i=0; i<9; i++) {
		var imageID = "loading-img" + containerNo + "-" + i;
		var chartPaneID = "right-pane" + containerNo + "-" + i;
        $('#' + subContainerID).append('<div class="right-chart-pane-expanded" id="' + chartPaneID + '" style="display: none"></div>');
	}
	$('.right-sub-container').css(subContainerCSS);
	$('.right-sub-container-header').css(headerCSS);
	$('.right-chart-pane-expanded').css(paneCSSExpanded);
    
    if (chartDisplayConfig2['dis_overall'] == 1) displayYoYGauge(data['growth_data']['dis_overall'], '#right-pane' + containerNo + '-' + '0');
    if (chartDisplayConfig2['dis_ent_nw'] == 1) displayYoYGauge(data['growth_data']['dis_ent_nw'], '#right-pane' + containerNo + '-' + '1');
    if (chartDisplayConfig2['dis_security'] == 1) displayYoYGauge(data['growth_data']['dis_security'], '#right-pane' + containerNo + '-' + '2');
    if (chartDisplayConfig2['dis_collab'] == 1) displayYoYGauge(data['growth_data']['dis_collab'], '#right-pane' + containerNo + '-' + '3');
    if (chartDisplayConfig2['dis_dcv'] == 1) displayYoYGauge(data['growth_data']['dis_dcv'], '#right-pane' + containerNo + '-' + '4');
    if (chartDisplayConfig2['dis_cloud'] == 1) displayYoYGauge(data['growth_data']['dis_cloud'], '#right-pane' + containerNo + '-' + '5');
    if (chartDisplayConfig2['dis_service'] == 1) displayYoYGauge(data['growth_data']['dis_service'], '#right-pane' + containerNo + '-' + '6');
    if (chartDisplayConfig2['dis_others'] == 1) displayYoYGauge(data['growth_data']['dis_others'], '#right-pane' + containerNo + '-' + '7');



  /*
  * Create Another Level of YoY Charts
  * */

    // Draw Discount YoY charts
	paneCSSExpanded = {
			"margin-left" : "2.2%",
			"margin-bottom" : "1.5%",
			"height" : "7em",
            "width" : "20%",
			"float" : "left",
			"background-color" : "#FFFFFF",
		};

	subContainerCSS = {
		"overflow-x" : "auto",
		"overflow-y" : "auto",
		"margin-bottom" : "2%",
		"border-style": "none",
		"background-color": "#FFFFFF",
	};
	
	headerCSS = {
		"margin-bottom" : "1%",
		"padding-top" : "1%",
		"color" : "#5A5097",
	};

	container_header = 'YoY-Other Metrics';
    containerNo = "3";
	subContainerID = 'right-sub-container' + containerNo;
	containerHeaderID = 'header' + containerNo;
	progressBarID = "progress-right" + containerNo;
	$('#right-panel-main').append('<div class="right-sub-container" id="' + subContainerID + '"></div>');
	$('#' + subContainerID).append('<h4 class="right-sub-container-header" id="' + containerHeaderID + '">' + container_header + '</h4><hr/>');
	for (i=0; i<5; i++) {
		var imageID = "loading-img" + containerNo + "-" + i;
		var chartPaneID = "right-pane" + containerNo + "-" + i;
        $('#' + subContainerID).append('<div class="right-chart-pane-expanded" id="' + chartPaneID + '" style="display: none"></div>');
	}
	$('.right-sub-container').css(subContainerCSS);
	$('.right-sub-container-header').css(headerCSS);
	$('.right-chart-pane-expanded').css(paneCSSExpanded);
  

    if (chartDisplayConfig2['yld_per_cus'] == 1) displayYoYGauge(data['growth_data']['yld_per_cus'], '#right-pane' + containerNo + '-' + '0');
    if (chartDisplayConfig2['tech_pen'] == 1) displayYoYGauge(data['growth_data']['tech_pen'], '#right-pane' + containerNo + '-' + '1');
    if (chartDisplayConfig2['bld_cus'] == 1) displayYoYGauge(data['growth_data']['bld_cus'], '#right-pane' + containerNo + '-' + '2');
    if (chartDisplayConfig2['bld_par'] == 1) displayYoYGauge(data['growth_data']['bld_par'], '#right-pane' + containerNo + '-' + '3');

}


function prepareMiddlePanelOrder() {
    var funcArray = [
        {whatChart : 'td_booking', chartFunction : displayYTD},
        {whatChart : 'prod_ser_booking', chartFunction : displayProdSerSplit},
        {whatChart : 'arch_booking', chartFunction : displayArch2Split},
        {whatChart : 'tech_booking', chartFunction : displayTechSplit},
        {whatChart : 'top_customers_booking', chartFunction : displayTopCustomers},
        {whatChart : 'top_deals_booking', chartFunction : displayTopDeals},
        {whatChart : 'top_partners_booking', chartFunction : displayTopPartners},
        {whatChart : 'gtmu_booking', chartFunction : displayGTMu},
        {whatChart : 'region_booking', chartFunction : displayRegion},
        {whatChart : 'sub_scms_booking', chartFunction : displaySubSCMS},
        {whatChart : 'top_sl6_booking', chartFunction : displayTopSL6},
        {whatChart : 'qoq_booking', chartFunction : displayQoQ},
        {whatChart : 'mom_booking', chartFunction : displayMoM},
        {whatChart : 'wow_booking', chartFunction : displayWoW},
        {whatChart : 'yield_per_customer', chartFunction : displayYldPerCus},
        {whatChart : 'billed_counts', chartFunction : displayBilled},
        {whatChart : 'tech_penetration', chartFunction : displayTechPen},
        {whatChart : 'repeat_new_bubble', chartFunction : displayRepeatNew},
        {whatChart : 'dormant_bubble', chartFunction : displayDormant},
        {whatChart : 'industry_booking', chartFunction : displayVerticalSplit},
        {whatChart : 'at_attach_booking', chartFunction : displayATAttach},
        {whatChart : 'booking_history', chartFunction : displayBookingHistory},
        {whatChart : 'overall_discount', chartFunction : displayOverallDiscounts},
        {whatChart : 'archs_discount', chartFunction : displayDiscounts},
    ];
    return funcArray;
}



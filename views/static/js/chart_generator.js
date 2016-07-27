function displayYTD(data, paneID) {
	var totalBooking = data['booking_data']['booking'];
	
	var chartData = {
		redFrom: 0,
		redTo: totalBooking*75/100,
		yellowFrom: totalBooking*75/100,
		yellowTo: totalBooking*90/100,
		greenFrom: totalBooking*90/100,
		greenTo: totalBooking*180/100,
        startAngle: -150,
        endAngle: 150,
		valueInArray: toArray(totalBooking.toFixed(2)),
		unit: '$M',
		title: 'Total Booking',
		seriesName: 'Booking',
		toolTipValuePrefix: '$M',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'gauge',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

function displayYldPerCus(data, paneID) {
	var yld = data['yld_per_cus']['booking'];
	
	var chartData = {
		redFrom: 0,
		redTo: yld*75/100,
		yellowFrom: yld*75/100,
		yellowTo: yld*90/100,
		greenFrom: yld*90/100,
		greenTo: yld*180/100,
        startAngle: -150,
        endAngle: 150,
		valueInArray: toArray(yld.toFixed(2)),
        dialBGColor: 'silver',
		unit: "$K",
		title: 'Yield/Customer',
		seriesName: 'Booking',
		toolTipValuePrefix: '$K',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'gauge_special',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}


function displayTechPen(data, paneID) {
	var techPen = data['tech_pen']['booking'];
	
	var chartData = {
		redFrom: 0,
		redTo: techPen*75/100,
		yellowFrom: techPen*75/100,
		yellowTo: techPen*90/100,
		greenFrom: techPen*90/100,
		greenTo: 11,
        startAngle: -90,
        endAngle: 90,
		valueInArray: toArray(techPen.toFixed(2)),
        dialBGColor: 'silver',
		unit: '',
		title: 'Technology_Penetration/Cus',
		seriesName: 'Tech.Pen',
		toolTipValuePrefix: '',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'gauge_special',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

function displayYoYGauge(data, paneID) {
	var totalBooking = data['booking'];
	
	var chartData = {
        stops: data['color_config'],
		bookingInArray: toArray(totalBooking.toFixed(2)),
		unit: data['unit'],
		title: '',
		seriesName: data['series_name'],
		toolTipValueSuffix: '',
		fontSize : '8px',
	};
	var chartArray = [
  	    {
  	 	   chartType: 'solid_gauge',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

function displayYoYStack(data, paneID) {
	var totalBookingData = 0;
	var totalBooking = 0;
	
	var chartData = {
		redFrom: 0,
		redTo: 0,
		yellowFrom: 0,
		yellowTo: 0,
		greenFrom: 0,
		greenTo: 0,
		bookingInArray: null,
		unit: '$M',
		title: 'Booking-YTD',
		seriesName: 'Booking',
		toolTipValueSuffix: ' Mil USD',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'stack_col',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

function displayQoQ(data, paneID) {
	var qoqArrayObj = data['qoq_array'];
	var qoqBookingArrayObj = data['qoq_booking_array'];
	var qoqArray = convertPyJSArray(qoqArrayObj, 'str');
	var qoqBookingArray = convertPyJSArray(qoqBookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: qoqArray,
			yAxisData: qoqBookingArray,
			topTitle: 'Quarterly Linearity $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'vBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}



function displayRepeatNew(data, paneID) {
    var dataArray = [data['new_accounts_ly'], data['repeat_accounts_ly'], data['new_accounts_l3y'], data['repeat_accounts_l3y']];
    console.log(data['new_accounts_ly'].x);
	var chartData = {
			dataArray: dataArray,
			topTitle: 'Repeat-New Contribution',
			topSubTitle: '',
			xAxisTitle: 'Booking Value $K',
			yAxisTitle: 'No of Accounts',
			seriesName: 'Booking',
			unit: ' $K',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'bubble',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}


function displayDormant(data, paneID) {
    var dataArray = [data['dormant_accounts_ly'], data['dormant_accounts_l3y']];
	var chartData = {
			dataArray: dataArray,
			topTitle: 'Dormant Accounts',
			topSubTitle: '',
			xAxisTitle: 'Booking Value $K',
			yAxisTitle: 'No of Accounts',
			seriesName: 'Booking',
			unit: ' $K',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'bubble',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayMoM(data, paneID) {
	var arrayObj = data['mom_array'];
	var bookingArrayObj = data['mom_booking_array'];
	var array = convertPyJSArray(arrayObj, 'str');
	var bookingArray = convertPyJSArray(bookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: array,
			yAxisData: bookingArray,
			topTitle: 'Monthly Linearity $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'vBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}


function displayWoW(data, paneID) {
	var arrayObj = data['wow_array'];
	var bookingArrayObj = data['wow_booking_array'];
	var array = convertPyJSArray(arrayObj, 'str');
	var bookingArray = convertPyJSArray(bookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: array,
			yAxisData: bookingArray,
			topTitle: 'WoW $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'vBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayArch2Split(data, paneID) {
	var arch2ArrayObj = data['arch2_array'];
	var arch2BookingArrayObj = data['arch2_booking_array'];
	var arch2Array = convertPyJSArray(arch2ArrayObj, 'str');
	var arch2BookingArray = convertPyJSArray(arch2BookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(arch2Array, arch2BookingArray),
			topTitle: 'Architecture Split $M',
			seriesName: 'Archs',
			titleFontSize : '12px'
	};
	var chartArray = [
	    {
 	 	   chartType: 'pie',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}



function displayVerticalSplit(data, paneID) {
	var verticalArrayObj = data['vertical_array'];
	var verticalBookingArrayObj = data['vertical_booking_array'];
	var verticalArray = convertPyJSArray(verticalArrayObj, 'str');
	var verticalBookingArray = convertPyJSArray(verticalBookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: verticalArray,
			yAxisData: verticalBookingArray,
			topTitle: 'Industry Vertical Split $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#4682B4',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayTechSplit(data, paneID) {
	var techArrayObj = data['tech_array'];
	var techBookingArrayObj = data['tech_booking_array'];
	var techArray = convertPyJSArray(techArrayObj, 'str');
	var techBookingArray = convertPyJSArray(techBookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: techArray,
			yAxisData: techBookingArray,
			topTitle: 'Technology Split $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#006400',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayATAttach(data, paneID) {
	var atAttachArrayObj = data['atAttach_array'];
	var atAttachBookingArrayObj = data['atAttach_booking_array'];
	var atAttachArray = convertPyJSArray(atAttachArrayObj, 'str');
	var atAttachBookingArray = convertPyJSArray(atAttachBookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(atAttachArray, atAttachBookingArray),
			topTitle: 'AT Attach $M',
			seriesName: '',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'donut',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displaySubSCMS(data, paneID) {
	var subSCMSArrayObj = data['subscms_array'];
	var subSCMSBookingArrayObj = data['subscms_booking_array'];
	var subSCMSArray = convertPyJSArray(subSCMSArrayObj, 'str');
	var subSCMSBookingArray = convertPyJSArray(subSCMSBookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(subSCMSArray, subSCMSBookingArray),
			topTitle: 'Sub SCMS $M',
			seriesName: '',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: '3dpie',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayGTMu(data, paneID) {
	var gtmuArrayObj = data['gtmu_array'];
	var gtmuBookingArrayObj = data['gtmu_booking_array'];
	var gtmuArray = convertPyJSArray(gtmuArrayObj, 'str');
	var gtmuBookingArray = convertPyJSArray(gtmuBookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(gtmuArray, gtmuBookingArray),
			topTitle: 'GTMu Share $M',
			seriesName: '',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'donut_semi',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayRegion(data, paneID) {
	var regionArrayObj = data['region_array'];
	var regionBookingArrayObj = data['region_booking_array'];
	var regionArray = convertPyJSArray(regionArrayObj, 'str');
	var regionBookingArray = convertPyJSArray(regionBookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(regionArray, regionBookingArray),
			topTitle: 'Region Share $M',
			seriesName: '',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'donut_semi',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayTopCustomers(data, paneID) {
	var customerArrayObj = data['customer_array'];
	var customerBookingArrayObj = data['customer_booking_array'];
	var customerArray = convertPyJSArray(customerArrayObj, 'str');
	var customerBookingArray = convertPyJSArray(customerBookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: customerArray,
			yAxisData: customerBookingArray,
			topTitle: 'Top 10 Customers $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#0000CD',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}


function displayTopDeals(data, paneID) {
	var arrayObj = data['topdeals_array'];
	var bookingArrayObj = data['topdeals_booking_array'];
	var array = convertPyJSArray(arrayObj, 'str');
	var bookingArray = convertPyJSArray(bookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: array,
			yAxisData: bookingArray,
			topTitle: 'Top 10 Deals $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#D2691E',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}


function displayTopPartners(data, paneID) {
	var partnerArrayObj = data['partner_array'];
	var partnerBookingArrayObj = data['partner_booking_array'];
	var partnerArray = convertPyJSArray(partnerArrayObj, 'str');
	var partnerBookingArray = convertPyJSArray(partnerBookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: partnerArray,
			yAxisData: partnerBookingArray,
			topTitle: 'Top 10 Partners $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#C71585',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayTopSL6(data, paneID) {
	var sl6ArrayObj = data['sl6_array'];
	var sl6BookingArrayObj = data['sl6_booking_array'];
	var sl6Array = convertPyJSArray(sl6ArrayObj, 'str');
	var sl6BookingArray = convertPyJSArray(sl6BookingArrayObj, 'number');
	
	var chartData = {
			xAxisData: sl6Array,
			yAxisData: sl6BookingArray,
			topTitle: 'Top 5 Sales_Level_6 $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#708090',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'hBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayBookingHistory(data, paneID) {
	var yearArrayObj = data['year_array'];
	var yearBookingArrayObj = data['year_booking_array'];
	var yearArray = convertPyJSArray(yearArrayObj, 'str');
	var yearBookingArray = convertPyJSArray(yearBookingArrayObj, 'number');
	var yearGrowthArray = findGrowthInArray(yearBookingArray);
	
	var chartData = {
			xAxisData: yearArray,
			yAxisPrimaryData: yearBookingArray,
			yAxisSecondaryData: yearGrowthArray,
			topTitle: 'Booking (FY10-15) $M',
			topSubTitle: '',
			yAxisTitle: 'Booking',
			seriesName: 'Booking',
			unit: ' $M',
			toolTipValueSuffix: ' Mil USD',
			barColor: '#1E90FF',
			titleFontSize : '12px'
	};
	var chartArray = [
  	    {
 	 	   chartType: 'dual_vBar',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}


function displayProdSerSplit(data, paneID) {
	var prodSerArrayObj = data['prodSer_array'];
	var prodSerBookingArrayObj = data['prodSer_booking_array'];
	var prodSerArray = convertPyJSArray(prodSerArrayObj, 'str');
	var prodSerBookingArray = convertPyJSArray(prodSerBookingArrayObj, 'number');
	
	var chartData = {
			seriesData: unpackArrayPairAndRepackAsJSON(prodSerArray, prodSerBookingArray),
			topTitle: 'Product/Service Split $M',
			seriesName: 'Archs',
			titleFontSize : '12px'
	};
	var chartArray = [
	    {
 	 	   chartType: 'pie',
 	 	   chartPane: paneID,
 	 	   dataObj: chartData
 		},
	];

  	generateCharts(chartArray);
}

function displayDiscounts(data, paneID) {
	var discountArrayObj = data['discount_array'];
	var discountBookingArrayObj = data['discount_booking_array'];
	var discountArray = convertPyJSArray(discountArrayObj, 'str');
	var discountBookingArray = convertPyJSArray(discountBookingArrayObj, 'number');
	
	var chartData = {
		redFrom: 75,
		redTo: 100,
		yellowFrom: 60,
		yellowTo: 75,
		greenFrom: 0.0,
		greenTo: 60,
		xAxisData: discountArray,
		yAxisData: numberArrayIntoPercentageArray(discountBookingArray),
		min: 0,
		max: 100,
		unit: '%',
		title: 'Average Discount by Architectures%',
		seriesName: '',
		toolTipValueSuffix: ' %',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'vu_meter',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}


function displayBilled(data, paneID) {
	var customers = data['billed_customers']['booking'];
	var partners = data['billed_partners']['booking'];
    var cus_par_ratio = partners/customers;
    var customerMax = 4000;
    var partnerMax = customerMax * cus_par_ratio;


	var chartData = {
		redFrom: 0,
		customersInArray: toArray(customers),
		partnersInArray: toArray(partners),
        ratioCusPar: cus_par_ratio,
        customerMax: customerMax,
        partnerMax: partnerMax,
		unit: '',
		title: 'Billed Customers/Partners',
		seriesName: 'Numbers',
		toolTipValueSuffix: '',
		titleFontSize : '12px'
	};
	var chartArray = [
  	    {
  	 	   chartType: 'dual_axis_gauge',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

function displayOverallDiscounts(data, paneID) {
	var discountArrayObj = data['discount_overall_array'];
	var discountBookingArrayObj = data['discount_overall_booking_array'];
	var discountArray = convertPyJSArray(discountArrayObj, 'str');
	var discountBookingArray = convertPyJSArray(discountBookingArrayObj, 'number');
	
	var chartData = {
		redFrom: 75,
		redTo: 100,
		yellowFrom: 60,
		yellowTo: 75,
		greenFrom: 0.0,
		greenTo: 60,
		xAxisData: discountArray,
		yAxisData: numberArrayIntoPercentageArray(discountBookingArray),
		min: 0,
		max: 100,
		unit: '%',
		title: 'Average Discount (Overall)%',
		seriesName: '',
		toolTipValueSuffix: ' %',
		titleFontSize : '12px',
		paneTitle: "Overall"
	};
	var chartArray = [
  	    {
  	 	   chartType: 'vu_meter_single',
  	 	   chartPane: paneID,
  	 	   dataObj: chartData
  		},
	];

  	generateCharts(chartArray);
}

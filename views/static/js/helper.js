function generateCharts(chartConfig) {
	for (i=0; i<chartConfig.length; i++) {
		var chartType = chartConfig[i]["chartType"];
		var chartPane = chartConfig[i]["chartPane"];
		var dataObj = chartConfig[i]["dataObj"];
        $(chartPane).show();
		if (chartType === 'hBar') {
			drawHorizontalBarChart(dataObj, chartPane);
		} else if (chartType === 'pie') {
			drawPieChart(dataObj, chartPane);
		} else if (chartType === 'solid_gauge') {
			drawSolidGauge(dataObj, chartPane);
		} else if (chartType === 'stack_col') {
            $(chartPane).show();
			drawStackedColumn(dataObj, chartPane);
		} else if (chartType === 'gauge') {
			drawAngularGauge(dataObj, chartPane);
		} else if (chartType === 'gauge_special') {
			drawAngularGaugeSpecial(dataObj, chartPane);
		} else if (chartType === 'donut') {
			drawDonutChart(dataObj, chartPane);
		} else if (chartType === 'vBar') {
			drawVerticalBarChart(dataObj, chartPane);
		} else if (chartType === 'dual_vBar') {
			drawDualAxisVerticalChart(dataObj, chartPane);
		} else if (chartType === '3dpie') {
			draw3DPieChart(dataObj, chartPane);
		} else if (chartType === 'donut_semi') {
			drawDonutSemiCircleChart(dataObj, chartPane);
		} else if (chartType === 'vu_meter') {
			drawVUMeter(dataObj, chartPane);
		} else if (chartType === 'vu_meter_single') {
			drawVUMeterSingle(dataObj, chartPane);
		} else if (chartType === 'dual_axis_gauge') {
			drawDualAxisGauge(dataObj, chartPane);
		} else if (chartType === 'line') {
			drawLineGraph(dataObj, chartPane);
		} else if (chartType === 'bubble') {
			drawBubbleGraph(dataObj, chartPane);
		}
	}
}

function unpackArrayPairAndRepackAsJSON(keys, values) {
	var array = new Array(keys.length);
	var sliceArray = ['PL', 'Sales AT', 'Security', 'service'];
	
	for (i=0; i<keys.length; i++) {
		var jsObject = new Object();
		array[i] = {
				name: keys[i],
				y: values[i]
		};
		
		//Check for particular keys for which the Pie to be projected/sliced/selected
		for (j=0; j<sliceArray.length; j++) {
			if (keys[i] === sliceArray[j]) {
				array[i].sliced = true; 
				array[i].selected = true;
			}
		}
		
		//Disable the DataLabels of 0 values
		if (values[i] === 0) {
			array[i].dataLabels = { enabled: false };
		}
	
	}
	return array;
}

function maxInArray(array) {
	Array.prototype.max = function() {
		return Math.max.apply(null, this);
	};
	return array.max();
}

function minInArray(array) {
	Array.prototype.min = function() {
		return Math.min.apply(null, this);
	};
	return array.min();
}

function numberArrayIntoPercentageArray(numberArray) {
	var array = new Array(numberArray.length);
	for (i=0; i<numberArray.length; i++) {
		array[i] = numberArray[i]*100;
	}
	return array;
}

function convertPyJSArray(pythonObj, elementType) {
	var array = new Array(pythonObj.length);
	for (i=0; i<pythonObj.length; i++) {
		var str = JSON.stringify(pythonObj[i]);
		if (elementType === 'str') {
			array[i] = str.replace(/\"/g, "");
		} else if (elementType === 'number') {
			array[i] = parseFloat(str.replace(/\"/g, ""));
		}
	}
	return array;
}

function calculateGrowth(val1, val2) {
	var growth = 0.0;
	if (val1 === 0 || val1 === null) {
		growth = 0.0;
	} else if ((val1 < 0 && val2 > 0) || (val1 > 0 && val2 < 0)) {
		growth = 0.0;
	} else {
		growth = (val2-val1) / val1;
	}
	return growth*100;
}

function findGrowthInArray(arrayList) {
	var array = new Array(arrayList.length);
	array[0] = 0.0;
	for (i=1; i<arrayList.length; i++) {
		array[i] = calculateGrowth(arrayList[i-1], arrayList[i]);
	}
	return array;
}

function toArray(data) {
	var array = new Array(1);
	for (i=0; i<1; i++) {
		var str = JSON.stringify(data);
		array[i] = parseFloat(str.replace(/\"/g, ""));
	}
	return array;
}


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

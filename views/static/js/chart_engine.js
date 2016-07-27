function drawVUMeter(data, paneID) {
	$(function () {
	    $(paneID).highcharts({

	        chart: {
	            type: 'gauge',
	            plotBorderWidth: null,
	            plotBackgroundColor: null,
	            plotBackgroundImage: null,
	            //height: 200
	        },

	        title: {
	            text: data.title,
                style: {
                	fontSize: data.titleFontSize
                }
	        },

	        pane: [{
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	            center: ['10%', null],
	            //size: 200
	        }, {
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	            center: ['30%', null],
	            //size: 200
	        }, {
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	            center: ['50%', null],
	            //size: 200
	        }, {
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	            center: ['70%', null],
	            //size: 200
	        }, {
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	            center: ['90%', null],
	            //size: 200
	        }],

	        tooltip: {
	            enabled: false
	        },

	        yAxis: [{
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 0,
	            title: {
	                text: data.xAxisData[0] + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[0].toFixed(1) + '%</span>',
	                y: -20
	            }
	        }, {
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 1,
	            title: {
	                text: data.xAxisData[1] + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[1].toFixed(1) + '%</span>',
	                y: -20
	            }
	        }, {
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 2,
	            title: {
	                text: data.xAxisData[2] + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[2].toFixed(1) + '%</span>',
	                y: -20
	            }
	        }, {
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 3,
	            title: {
	                text: data.xAxisData[3] + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[3].toFixed(1) + '%</span>',
	                y: -20
	            }
	        }, {
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 4,
	            title: {
	                text: data.xAxisData[4] + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[4].toFixed(1) + '%</span>',
	                y: -20
	            }
	        }],

	        plotOptions: {
	            gauge: {
	                dataLabels: {
	                    enabled: false
	                },
	                dial: {
	                    radius: '100%'
	                }
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: data.xAxisData[0],
	            data: [data.yAxisData[0]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 0
	        }, {
	            name: data.xAxisData[1],
	            data: [data.yAxisData[1]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 1
	        }, {
	            name: data.xAxisData[2],
	            data: [data.yAxisData[2]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 2
	        }, {
	            name: data.xAxisData[3],
	            data: [data.yAxisData[3]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 3
	        }, {
	            name: data.xAxisData[4],
	            data: [data.yAxisData[4]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 4
	        }]

	    }

	    );
	});
}


function drawVUMeterSingle(data, paneID) {
	$(function () {
	    $(paneID).highcharts({

	        chart: {
	            type: 'gauge',
	            plotBorderWidth: null,
	            plotBackgroundColor: null,
	            plotBackgroundImage: null,
	        },

	        title: {
	            text: data.title,
                style: {
                	fontSize: data.titleFontSize
                }
	        },

	        pane: [{
	            startAngle: -45,
	            endAngle: 45,
	            background: null,
	        },],

	        tooltip: {
	            enabled: false
	        },

	        yAxis: [{
	            min: data.min,
	            max: data.max,
	            minorTickPosition: 'outside',
	            tickPosition: 'outside',
	            labels: {
	                rotation: 'auto',
	                distance: 20
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#C02316',
	                innerRadius: '100%',
	                outerRadius: '105%'
	            }],
	            pane: 0,
	            title: {
	                text: data.paneTitle + '<br/><span style="font-size:8px">Avg. Dis</span>' + '<br/><span style="font-size:8px">' + data.yAxisData[0].toFixed(1) + '%</span>',
	                y: -30
	            }
	        },],

	        plotOptions: {
	            gauge: {
	                dataLabels: {
	                    enabled: false
	                },
	                dial: {
	                    radius: '100%'
	                }
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: data.xAxisData[0],
	            data: [data.yAxisData[0]],
	            tooltip: {
	                valueSuffix: data.toolTipValueSuffix
	            },
	            yAxis: 0
	        },]

	    }

	    );
	});
}




function drawPieChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: null,
	            plotShadow: false,
	            type: 'pie'
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        tooltip: {
	            pointFormat: '{point.name}: <b>$M {point.y:.1f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                allowPointSelect: true,
	                cursor: 'pointer',
	                dataLabels: {
	                    enabled: true,
	                    distance: 5,
	                    borderWidth: 5,
	                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
	                    style: {
	                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
	                        fontSize: "8px",
	                    }
	                }
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: '',
	            colorByPoint: true,
	            data: data.seriesData
	        }]
	    });
	});
}

function draw3DPieChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: null,
	            plotShadow: false,
	            type: 'pie',
	            options3d: {
	            	enabled: true,
	            	alpha: 45,
	            	beta: 0
	            }
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        tooltip: {
	            pointFormat: '{point.name}: <b>$M {point.y:.1f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                allowPointSelect: true,
	                cursor: 'pointer',
	                depth: 35,
	                dataLabels: {
	                    enabled: true,
	                    distance: 5,
	                    borderWidth: 5,
	                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
	                    style: {
	                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
	                        fontSize: "8px",
	                    }
	                }
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: '',
	            colorByPoint: true,
	            data: data.seriesData
	        }]
	    });
	});
}


function drawDonutChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: null,
	            plotShadow: false,
	            type: 'pie',
	            options3d: {
	            	enabled: true,
	            	alpha: 45
	            }
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        tooltip: {
	            pointFormat: '{point.name}: <b>$M {point.y:.1f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                allowPointSelect: true,
	                cursor: 'pointer',
	                innerSize: 50,
	                depth: 45,
	                dataLabels: {
	                    enabled: true,
	                    distance: 3,
	                    borderWidth: 5,
	                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
	                    style: {
	                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
	                        fontSize: "8px",
	                    }
	                }
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            name: '',
	            colorByPoint: true,
	            data: data.seriesData
	        }]
	    });
	});
}


function drawDonutSemiCircleChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                },
	            align: 'center',
	            verticalAlign: 'top',
	            y: 10
	        },
	        tooltip: {
	            pointFormat: '{series.name}: <b>{point.percentage:.1f} % ({point.y:.1f} $M)</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -30,
	                    format: '<b>{point.name}</b>',
	                    style: {
	                        fontWeight: 'bold',
	                        fontSize: "9px",
	                        color: 'white',
	                        textShadow: '0px 1px 2px black',
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	            type: 'pie',
	            name: '',
	            innerSize: '50%',
	            data: data.seriesData,
	            dataLabels: {
	            	enabled: true
	            }
	        }]
	    });
	});
	
}


function drawAngularGaugeSpecial(data, paneID) {
	$(function () {

	    $(paneID).highcharts({

	        chart: {
	            type: 'gauge',
	            plotBackgroundColor: null,
	            plotBackgroundImage: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },

	        title: {
	            text: data.title,
                style: {
                	fontSize: data.titleFontSize
                }
	        },

	        pane: {
	            startAngle: data.startAngle,
	            endAngle: data.endAngle,
	        },
	        credits: {
	            enabled: false
	        },
	        // the value axis
	        yAxis: {
	            min: data.redFrom,
	            max: data.greenTo,

	            minorTickInterval: 'auto',
	            minorTickWidth: 1,
	            minorTickLength: 10,
	            minorTickPosition: 'inside',
	            minorTickColor: '#666',

	            tickPixelInterval: 30,
	            tickWidth: 2,
	            tickPosition: 'inside',
	            tickLength: 10,
	            tickColor: '#666',
	            labels: {
	                step: 2,
	                rotation: 'auto'
	            },
	            title: {
	                text: data.unit
	            },
	        },
	        gauge : {
	        	dataLables: {
	        		enabled: false,
	        	}
	        },
	        series: [{
	            name: data.seriesName,
	            data: data.valueInArray,
	            tooltip: {
	                valuePrefix: data.toolTipValuePrefix
	            }
	        }]
        });
    });
}




function drawAngularGauge(data, paneID) {
	$(function () {

	    $(paneID).highcharts({

	        chart: {
	            type: 'gauge',
	            plotBackgroundColor: null,
	            plotBackgroundImage: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },

	        title: {
	            text: data.title,
                style: {
                	fontSize: data.titleFontSize
                }
	        },

	        pane: {
	            startAngle: data.startAngle,
	            endAngle: data.endAngle,
	            background: [{
	                backgroundColor: {
	                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
	                    stops: [
	                        [0, '#FFF'],
	                        [1, '#333']
	                    ]
	                },
	                borderWidth: 0,
	                outerRadius: '109%'
	            }, {
	                backgroundColor: {
	                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
	                    stops: [
	                        [0, '#333'],
	                        [1, '#FFF']
	                    ]
	                },
	                borderWidth: 1,
	                outerRadius: '107%'
	            }, {
	                // default background
	            }, {
	                backgroundColor: '#DDD',
	                borderWidth: 0,
	                outerRadius: '105%',
	                innerRadius: '103%'
	            }]
	        },
	        credits: {
	            enabled: false
	        },
	        // the value axis
	        yAxis: {
	            min: data.redFrom,
	            max: data.greenTo,

	            minorTickInterval: 'auto',
	            minorTickWidth: 1,
	            minorTickLength: 10,
	            minorTickPosition: 'inside',
	            minorTickColor: '#666',

	            tickPixelInterval: 30,
	            tickWidth: 2,
	            tickPosition: 'inside',
	            tickLength: 10,
	            tickColor: '#666',
	            labels: {
	                step: 2,
	                rotation: 'auto'
	            },
	            title: {
	                text: data.unit
	            },
	            plotBands: [{
	                from: data.redFrom,
	                to: data.redTo,
	                color: '#DF5353' // red
	            }, {
	                from: data.yellowFrom,
	                to: data.yellowTo,
	                color: '#DDDF0D' // yellow
	            }, {
	                from: data.greenFrom,
	                to: data.greenTo,
	                color: '#55BF3B' // green
	            }]
	        },
	        gauge : {
	        	dataLables: {
	        		enabled: false,
	        	}
	        },
	        series: [{
	            name: data.seriesName,
	            data: data.valueInArray,
	            tooltip: {
	                valuePrefix: data.toolTipValuePrefix
	            }
	        }]
        });
    });
}

function drawHorizontalBarChart(data, paneID) {
	var dataSum = 0;
	for (var j=0; j<data.yAxisData.length; j++) {
		dataSum += data.yAxisData[j];
	}
	
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            type: 'bar',
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        subtitle: {
	            text: data.topSubTitle
	        },
	        xAxis: {
	            categories: data.xAxisData,
                labels: {
                    step: 1,
                },
	            title: {
	                text: null
	            }
	        },
	        yAxis: {
	            min: 0,
	            title: {
	                text: data.yAxisTitle + data.unit,
	                align: 'high'
	            },
	            labels: {
	                overflow: 'justify',
	                style: {
	                	fontSize: '10px'
	                }
	            }
	        },
            tooltip: {
	            pointFormat: '{point.name}: <b>$M {point.y:.2f}</b>',
                //valueSuffix: data.unit
            },
	        plotOptions: {
	            bar: {
	                dataLabels: {
	                    enabled: true,
	                    //format: '{point.y:.2f}',
	                    formatter:function() {
	                        var pcnt = (this.y / dataSum) * 100;
	                        return Highcharts.numberFormat(pcnt) + '%';
	                    }
	                }
	            },
	        	series: {
	        		dataLabels: {
	                    enabled: true,
	                    allowOverlap: true,
		                style: {
		                	fontSize: '8px'
		                }
	        		}
	        	}
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'right',
	            verticalAlign: 'top',
	            x: -40,
	            y: 80,
	            floating: true,
	            borderWidth: 1,
	            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
	            shadow: true,
	            itemStyle: {
	            	fontSize: '10px'
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	        	color: data.barColor,
	        	shadow: true,
	            name: data.seriesName,
	            data: data.yAxisData
	        }]
	    },
        function (chart) {
	    	var legend = chart.legend;
	    	if (legend.display) {
	    		legend.group.hide();
	    		legend.box.hide();
	    		legend.display = false;
	    	}
        });
	});	
}

function drawVerticalBarChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            type: 'column',
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        subtitle: {
	            text: data.topSubTitle
	        },
	        xAxis: {
	            categories: data.xAxisData,
                labels: {
                    step: 1,
                },
	            title: {
	                text: null
	            }
	        },
	        yAxis: {
	            min: 0,
	            title: {
	                text: data.yAxisTitle + data.unit,
	                align: 'high'
	            },
	            labels: {
	                overflow: 'justify',
	                style: {
	                	fontSize: '8px'
	                }
	            }
	        },
            tooltip: {
	            pointFormat: '{point.name}: <b>$M {point.y:.2f}</b>',
                //valueSuffix: data.unit
            },
	        plotOptions: {
	            bar: {
	                dataLabels: {
	                    enabled: true,
	                }
	            },
	        	series: {
	        		dataLabels: {
	                    enabled: true,
	                    allowOverlap: true,
	                    format: '{point.y:.2f}',
		                style: {
		                	fontSize: '8px'
		                }
	        		}
	        	}
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'right',
	            verticalAlign: 'top',
	            x: -40,
	            y: 80,
	            floating: true,
	            borderWidth: 1,
	            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
	            shadow: true,
	            itemStyle: {
	            	fontSize: '10px'
	            }
	        },
	        credits: {
	            enabled: false
	        },
	        series: [{
	        	color: data.barColor,
	        	shadow: true,
	            name: data.seriesName,
	            data: data.yAxisData
	        }]
	    },
        function (chart) {
	    	var legend = chart.legend;
	    	if (legend.display) {
	    		legend.group.hide();
	    		legend.box.hide();
	    		legend.display = false;
	    	}
        });
	});	
}

function drawDualAxisVerticalChart(data, paneID) {
	$(function () {
	    $(paneID).highcharts({
	        chart: {
	            zoomType: 'xy'
	        },
	        title: {
	            text: data.topTitle,
                style: {
                	fontSize: data.titleFontSize
                }
	        },
	        subtitle: {
	            text: ''
	        },
	        xAxis: [{
	            categories: data.xAxisData,
	            crosshair: true
	        }],
	        yAxis: [{ // Primary yAxis
	            labels: {
	                format: '{value}%',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            },
	            title: {
	                text: 'YoY',
	                style: {
	                    color: Highcharts.getOptions().colors[1]
	                }
	            }
	        }, { // Secondary yAxis
	            title: {
	                text: 'Booking',
	                style: {
	                    color: Highcharts.getOptions().colors[0]
	                }
	            },
	            labels: {
	                format: '$M {value}',
	                style: {
	                    color: Highcharts.getOptions().colors[0]
	                }
	            },
	            opposite: true
	        }],
	        tooltip: {
	            shared: true
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'left',
	            x: 120,
	            verticalAlign: 'top',
	            y: 100,
	            floating: true,
	            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
	        },
	        series: [{
	            name: 'Booking',
	            type: 'column',
	            yAxis: 1,
	            data: data.yAxisPrimaryData,
	            tooltip: {
		            pointFormat: '{point.name}: <b>$M {point.y:.2f}</b>',
	                //valueSuffix: data.unit
	            }

	        }, {
	            name: 'YoY',
	            type: 'spline',
	            data: data.yAxisSecondaryData,
	            tooltip: {
		            pointFormat: '{point.name}: <b>{point.y:.1f}%</b>'
	                //valueSuffix: '%'
	            }
	        }]
	    },
	    function (chart) {
	    	var legend = chart.legend;
	    	if (legend.display) {
	    		legend.group.hide();
	    		legend.box.hide();
	    		legend.display = false;
	    	}
        });
	});
}

function drawSolidGauge(data, paneID) {
	$(function () {

	    var gaugeOptions = {

	        chart: {
	            type: 'solidgauge'
	        },
            exporting: {
                enabled: false
            },
	        title: null,
	        pane: {
	            center: ['50%', '50%'],
	            size: '70%',
	            startAngle: -100,
	            endAngle: 100,
	            background: {
	                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
	                innerRadius: '60%',
	                outerRadius: '100%',
	                shape: 'arc'
	            }
	        },

	        tooltip: {
	            enabled: false
	        },

	        // the value axis
	        yAxis: {
	            //stops: data.stops,
                minColor: '#00FF00',
                maxColor: '#00FF00',
	            lineWidth: 0,
	            minorTickInterval: null,
	            tickPixelInterval: 400,
	            tickWidth: 0,
	            title: {
	                y: -70
	            },
	            labels: {
	                y: 16
	            }
	        },

	        plotOptions: {
	            solidgauge: {
	                dataLabels: {
	                    y: 35,
	                    borderWidth: 0,
	                    useHTML: false
	                }
	            }
	        }
	    };

	    // The speed gauge
	    $(paneID).highcharts(Highcharts.merge(gaugeOptions, {
	        yAxis: {
	            min: -100,
	            max: 100,
	            title: {
	                text: ''
	            },
                style: {
                    fontSize: data.fontSize, 
                },
                labels: {
                    enabled: false
                }
	        },

	        credits: {
	            enabled: false
	        },

	        series: [{
	            name: '',
	            data: data.bookingInArray,
	            dataLabels: {
	                format: '<div style="text-align:center"><span style="font-size:' + data.fontSize + ';color:' +
	                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}' + 
                            data.unit + '</span><br /><span style="font-size:' + data.fontSize + ';text-align:center;">' + data.seriesName + '</span></div>'
	            },
	            tooltip: {
	            }
	        }]

	    }), function(chart) {
                var point = chart.series[0].points[0];
                var pointValue = point.y;
                var color = data.stops.neutral;
                if (pointValue >= -100 && pointValue < 0) {
                    color = data.stops.negative;
                } else if (pointValue > 0) {
                    color = data.stops.positive;
                }
                chart.yAxis[0].stops[0].color.rgba = color;
                chart.yAxis[0].stops[1].color.rgba = color;
                point.update(pointValue);
        });

	});
}



function drawStackedColumn(data, paneID) {
    $(function () {
        $(paneID).highcharts({
            chart: {
                type: 'column'
            },
            exporting: {
                enabled: false
            },
            legend: {
                align: 'right',
                layout: 'vertical',
                verticalAlign: 'middle',
                symbolHeight: 8,
                symbolWidth: 8,
                itemStyle: {
                    fontSize: '8px'
                }
            },
            title: {
                text: '$M',
                style: {
                    fontSize: '8px'
                }
            },
            xAxis: {
                categories: [''],
                lineWidth: 0,
                minorGridLineWidth: 0,
                majorGridLineWidth: 0,
                gridLineWidth: 0,
                lineColor: 'transparent',
                labels: {
                    enabled: false
                },
                title: {
                    enabled: false
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                },
                labels: {
                    enabled: false
                },
                lineWidth: 0,
                minorGridLineWidth: 0,
                majorGridLineWidth: 0,
                gridLineWidth: 0,
                lineColor: 'transparent',
            },
	        credits: {
	            enabled: false
	        },
            tooltip: {
                shared: true
            },
            plotOptions: {
                column: {
                    stacking: 'percent'
                }
            },
            series: [{
                name: 'FY15',
                data: [5],
	            dataLabels: {
	                format: '<div style="text-align:center"><span style="font-size:10px;color:' +
	                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white') + '">{y}</span></div>',
                    allowOverlap: true,
                    overflow: 'justify',
                    enabled: true,
	            },
            }, {
                name: 'FY16',
                data: [2],
	            dataLabels: {
	                format: '<div style="text-align:center"><span style="font-size:10px;color:' +
	                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'white') + '">{y}</span></div>',
                    allowOverlap: true,
                    overflow: 'justify',
                    enabled: true,
	            },
            }]
        });
    }); 
}


function drawDualAxisGauge(data, paneID) {
    $(paneID).highcharts({

        chart: {
            type: 'gauge',
            alignTicks: false,
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        tooltip: {
            enabled: false
        },
        title: {
            text: data.title,
            style: {
                fontSize: data.titleFontSize
            }
        },
        credits: {
            enabled: false
        },
        pane: {
            startAngle: -150,
            endAngle: 150
        },

        yAxis: [{
            min: 0,
            max: data.partnerMax,
            lineColor: '#339',
            tickColor: '#339',
            minorTickColor: '#339',
            offset: -25,
            lineWidth: 2,
            labels: {
                distance: -20,
                rotation: 'auto'
            },
            tickLength: 5,
            minorTickLength: 5,
            endOnTick: false
        }, {
            min: 0,
            max: data.customerMax,
            tickPosition: 'outside',
            lineColor: '#933',
            lineWidth: 2,
            minorTickPosition: 'outside',
            tickColor: '#933',
            minorTickColor: '#933',
            tickLength: 5,
            minorTickLength: 5,
            labels: {
                distance: 12,
                rotation: 'auto'
            },
            offset: -20,
            endOnTick: false
        }],

        series: [{
            name: 'Partners',
            data: data.partnersInArray,
            dataLabels: {
                formatter: function () {
                    var partners = this.y,
                        customers = Math.round(partners / data.ratioCusPar);
                        console.log("Derived customers: " + customers);
                    return '<span style="color:#339">' + partners + ' Partners</span><br/>' +
                        '<span style="color:#933">' + customers + ' Customers</span>';
                },
                backgroundColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, '#DDD'],
                        [1, '#FFF']
                    ]
                },
                y: 100,
                x: 90,
            },
            tooltip: {
                valueSuffix: ' Nos',
            }
        }]

    });
    
}




function drawLineGraph(data, paneID) {
    $(paneID).highcharts({
        title: {
            text: data.topTitle,
            x: -20 //center
        },
        credits: {
            enabled: false
        },
        subtitle: {
            text: '',
            x: -20
        },
        xAxis: {
            categories: data.xAxisData 
        },
        yAxis: {
            title: {
                text: data.yAxisTitle
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '$M',
            pointFormat: '{point.name}: <b>$M {point.y:.1f}</b>'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Booking',
            data: data.yAxisData, 
        }]
    });
    
}




function drawBubbleGraph(data, paneID) {
    //console.log(data);
    $(paneID).highcharts({

        chart: {
            type: 'bubble',
            plotBorderWidth: 1,
            zoomType: 'xy'
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        title: {
            text: data.topTitle,
            style: {
                fontSize: data.titleFontSize
            }
        },
        subtitle: {
            text: '',
        },
        xAxis: {
            gridLineWidth: 1,
            title: {
                text: data.xAxisTitle,
            },
            labels: {
                format: '${value}K'
            },
            plotLines: [{
                color: 'black',
                dashStyle: 'dot',
                width: 2,
                value: 0,
                label: {
                    align: 'middle',
                    rotation: 0,
                    y: 15,
                    style: {
                        fontStyle: 'italic'
                    },
                    text: 'Booking'
                },
                zIndex: 3
            }]
        },

        yAxis: {
            startOnTick: false,
            endOnTick: false,
            title: {
                text: data.yAxisTitle,
                style: {
                    fontSize: data.titleFontSize
                }
            },
            labels: {
                format: '{value}'
            },
            maxPadding: 0.2,
            plotLines: [{
                color: 'black',
                dashStyle: 'dot',
                width: 2,
                value: 0,
                label: {
                    align: 'right',
                    style: {
                        fontStyle: 'italic'
                    },
                    text: 'Accounts',
                    x: -10
                },
                zIndex: 3
            }]
        },

        tooltip: {
            pointFormat: '{point.description}<br />{point.y} accounts <br />${point.x:.1f}K <br />{point.z:.1f}% No. of accounts attach',
        },

        plotOptions: {
            series: {
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },

        series: [{
            data: data.dataArray
        }]

    });
    
}

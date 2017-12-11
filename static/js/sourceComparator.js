// **** Data used for this page is stored in data.js

// Initial values for chart options 
var sourceValue = ""
var xAxisFeature = ""
var yAxisFeature = ""
var bubbleColorFeature = ""
var bubbleSizeFeature = ""
var startDate = ""
var endDate = ""
var selectedSources = []
var sources = []

$(document).ready(function () {
	google.charts.load('current', {'packages':['corechart']});
	// Initially set x, y, bubble color and bubble size options to top features
	setFeatureOptions(topFeatures)

	// Get initial chart data
	$.when(getAllSources(), getDateRange()).done(function(a1, a2) {
		sources = a1[0]["sources"]
		selectedSources = sources.slice()
		// Set source chart option
		setSourceOptions(sources)
		startDate = a2[0]["startDate"]
		endDate = a2[0]["endDate"]

	  	// Initializes date range picker and also gets value of range when changed
		$('input[name="daterange"]').daterangepicker(
	    {
	      locale: {
	        format: 'YYYY-MM-DD'
	      },
	      startDate: startDate,
	      endDate: endDate,
	      minDate: startDate,
	      maxDate: endDate
	    }, 
	    function(start, end, label) {
	      startDate = start.format('YYYY-MM-DD')
	      endDate = start.format('YYYY-MM-DD')
	    })
	    
	    // Get initial chart data
		google.charts.setOnLoadCallback(submitData());

	})
});

// Gets all sources stored in the database
function getAllSources() {
	return $.ajax({
		type: "GET",
		url: "/getAllSources",
		success: function(response) {
			// In the $.when function
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

// Sets up options for x, y, bubble color, and bubble size options so there are no repeats
function setFeatureOptions(features) {
	var xAxisSelector = document.getElementById("xAxisSelector")
	var yAxisSelector = document.getElementById("yAxisSelector")
	var bubbleColorSelector = document.getElementById("bubbleColorSelector")
	var bubbleSizeSelector = document.getElementById("bubbleSizeSelector")
	var selectors = [xAxisSelector, yAxisSelector, bubbleColorSelector, bubbleSizeSelector]
	
	// Clear current options in selectors
	for (i=0; i < selectors.length; i++) {
		selectors[i].innerHTML = ""
	}

	// Add options
	$.each(Object.keys(features), function(i, key) {    
		for (j=0; j < selectors.length; j++) {
			if (i == j) {
				selectors[j].innerHTML += "<option selected='selected'>" + key + "</option>"
			}
			else {
				selectors[j].innerHTML += "<option>" + key + "</option>"
			}
		}
	});
}

function setSourceOptions(allSources) {
	for (i=0; i < allSources.length; i++) {
		var divSources = document.getElementById("sourceSelector")
		divSources.innerHTML += "<option selected='selected' value='" + allSources[i] + "''>" + allSources[i] + "</option>"
	}
	$("#sourceSelector").selectpicker('refresh');
}

function getDateRange() {
	return $.ajax({
		type: "GET",
		url: "/getDateRange",
		success: function(response) {
			// In the $.when function
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function drawBubbleChart() {

	if (data.length == 1) {
		errorPopover("Invalid news source(s) for selected date range.")
		return
	}

	dataTransform = google.visualization.arrayToDataTable(data)

	var options = {
		enableInteractivity: true,
		chartArea: {width: 1100, height: 575},
		hAxis: {title: data[0][1], viewWindowMode: 'pretty', textPosition: "none"},
		vAxis: {title: data[0][2], viewWindowMode: 'pretty', textPosition: "none"},
		colorAxis: {legend: {textStyle: {color: "white"}}},
		bubble: {textStyle: {fontSize: 11}},
		animation: {startup: true, duration: 1000, easing: 'inAndOut'},
		explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 4.0},
		tooltip: {trigger: "none"}
	}

	chart = new google.visualization.BubbleChart(document.getElementById("bubbleChart"));

	function selectHandler() {
		var selectedItem = chart.getSelection()[0];
		if (selectedItem) {
			source = data[selectedItem.row+1][0]
			window.location.href = "/newsSource?source=" + source;
		}
	}

	google.visualization.events.addListener(chart, 'select', selectHandler);    
	chart.draw(dataTransform, options);
	$("#lowLegendLabel p").text("low")
	$("#highLegendLabel p").text("high")
}

function getChartSettings() {
	sourceValue = $("#sourceValueSelector").find(":selected").text();
	xAxisFeature = $("#xAxisSelector").find(":selected").text();
	yAxisFeature = $("#yAxisSelector").find(":selected").text();
	bubbleColorFeature = $("#bubbleColorSelector").find(":selected").text();
	bubbleSizeFeature = $("#bubbleSizeSelector").find(":selected").text();
	selectedSources = []

	$('.selectpicker :selected').each(function(i, selected){ 
		selectedSources.push($(selected).text()); 
	});
}


// Updates selected chart feature settings when one selected (need to test this)
$(function() {
  $('.form-control').on('change', function() {

	var selectedText = $(this).find("option:selected").text()
	var options = ["xAxisSelector", "yAxisSelector", "bubbleColorSelector", "bubbleSizeSelector"]
	var f = $(this).attr('id')
	var index = options.indexOf(f)

	for (var i=0; i < options.length; i++) {
	  if (i != index) {
		var selectedOption = $("#" + options[i]).find("option:selected").text()
		if (selectedOption == selectedText) {
		  var invalid = []
		  for (var j=0; j < options.length; j++) {
			if (i != j) {
			  invalid.push($("#" + options[j]).find("option:selected").text())
			}
		  }
		  $("#" + options[i] + " option").each(function() {
			if (invalid.indexOf($(this).text()) == -1) {
			  $(this).prop("selected", true);
			  return false;
			}
		  });
		}
	  }
	}
  });
});

function submitData() {
	getChartSettings()

	if (selectedSources.length == 0) {
		errorPopover("You must select at least one news source.")
		document.getElementById("submitButton").disabled = true
		return
	}

	// Removes any error popovers if exists
	$('.popover').remove();

	// Disable submit button so that user does not keep clicking
	document.getElementById("submitButton").disabled = true

	$.ajax({
	type: "GET",
	url: "/getBubbleChartData",
	data: {
		sourceValue: sourceValue,
		xAxis: features[xAxisFeature],
		yAxis: features[yAxisFeature],
		bubbleColor: features[bubbleColorFeature],
		bubbleSize: features[bubbleSizeFeature],
		startDate: startDate,
		endDate: endDate,
		sources: JSON.stringify(selectedSources)
	},
	success: function(response) {
		data = []
		data[0] = ['Source', xAxisFeature, yAxisFeature, bubbleColorFeature, bubbleSizeFeature]

		var row = 1
		for (var i in response["values"]) {
			s = response["values"][i]
			data[row] = [s["source"], s["xAxis"], s["yAxis"], s["bubbleColor"], s["bubbleSize"]]
			row += 1
	  } 

	  // Update header statistics
	  document.getElementById("sourceCount").innerHTML = response["numSources"]
	  document.getElementById("articleCount").innerHTML = response["numArticles"]
	  document.getElementById("facebookShares").innerHTML = response["mostFBShares"]
	  document.getElementById("facebookComments").innerHTML = response["mostFBComments"]
	  document.getElementById("facebookReactions").innerHTML = response["mostFBReactions"]
	  drawBubbleChart()
	  
	  // Re-enable submit button after successful request
	document.getElementById("submitButton").disabled = false

	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}

// Makes sure that at least one source is picked by presenting user with error message
$(document).ready(function(){
	$('[data-toggle="popover"]').popover();   
});

function errorPopover(text) {
  $('#sourceSelectContainer').popover({
			placement:'right',
			trigger:'manual',
			html:true,
			content: text
		});
   $('#sourceSelectContainer').popover('show');
}

function sourceSelectClicked() {
  $('.popover').remove();
  document.getElementById("submitButton").disabled = false
}

// Function that toggles features shown
$(document).ready(function() {
	$("#featureCheckbox").change(function() {
	    if (this.checked) {
	        setFeatureOptions(features)
	    }
	    else {
	    	setFeatureOptions(topFeatures)
	    }
	});
});
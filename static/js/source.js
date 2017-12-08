// **** Data used for this page is stored in sourceData.js

var abbrevMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
// Array to hold data for the charts
var articleCountData = [];
var facebookEngagementData = [];

// Name of source accessed
var source = "";

// Read the news source name, which is provided as a parameter in the URL
function getURLParameter(name) {
	return decodeURIComponent((new RegExp("[?|&]" + name + "=" + "([^&;]+?)(&|#|;|$)").exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}

// Update page with source-specific information
$(document).ready(function () {
	source = getURLParameter("source")
	getSourceInfo()
	getSourceValues()
	getFeaturedArticles()
	getSourcePublishDates()
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(getArticleCountChartData());
	google.charts.setOnLoadCallback(getFacebookEngagementChartData());
});

// Get source metadata information panel with data collected about the source
function getSourceInfo() {
	document.getElementById("sourceName").innerHTML = sourceData[source]["name"]
	document.getElementById("sourceImage").src = "/static/newsSourceImages/" + sourceData[source]["imageName"]
	document.getElementById("typeLabel").innerHTML = sourceData[source]["type"]
	document.getElementById("countryLabel").innerHTML = sourceData[source]["country"]
	document.getElementById("foundedLabel").innerHTML = sourceData[source]["founded"]
	document.getElementById("websiteLabel").innerHTML = sourceData[source]["website"]
	document.getElementById("websiteLabel").href = "http://www." + sourceData[source]["website"]
}

// Get credibility/impartiality values or show that it is a satire source
function getSourceValues() {
	$.ajax({
	type: "GET",
	url: "/getSourceMetadata",
	data: {
		source: source
	},
	success: function(response) {
		var perCredible = response["perCredible"]
		var perImpartial = response["perImpartial"]
		var isSatire = response["isSatire"]
		if (isSatire == 1) {
			$("#perCredibleVal").text(" N/A")
			$("#perImpartialVal").text(" N/A")
			var $isSatire = $("<p id='isSatire' style='font-size:smaller; margin-left: 160px'> *Self-identified satire source </p>")
			$("#sourceMetadataVals").append($isSatire)
		}
		else {
			$("#perCredibleVal").text(perCredible + "%")
			$("#perImpartialVal").text(perImpartial + "%")
			$("#isSatire").remove()
		}
			
	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}

function getArticleCountChartData() {
	$.ajax({
	type: "GET",
	url: "/getSourcePublishCounts",
	data: {
		source: source
	},
	success: function(response) {
		// Header for data
		articleCountData[0] = ["Month", "Number of Articles", { role: 'style' }]

		// Colors used in chart for each month in order
		var colors = ["#CACFD6", "#D6E5E3", "#9FD8CB", "#517664", "#70798C", "#93827F", "#2D3319"]

		// Populate data array used for chart
		var row = 1
		var colorIndex = 0
		for (var month in response) {
			var monthCount = response[month] 
			articleCountData[row] = [month, monthCount, colors[colorIndex]]
			row += 1
			colorIndex += 1
			if (colorIndex == 7) {
				colorIndex = 0;
			}
		} 

		google.charts.setOnLoadCallback(articleCountChart);
	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}

// Gets valid source publish dates for top phrase selector
function getSourcePublishDates() {
	$.ajax({
	type: "GET",
	url: "/getSourcePublishDates",
	data: {
		source: source
	},
	success: function(response) {
		var monthPhraseSelector = document.getElementById("monthPhraseSelector")
		for (var i in response["dates"]) {
			// Set initial top phrases
			if (i == 0) {
				var date = response["dates"][i].split(" ")
				var month = abbrevMonths.indexOf(date[0]) + 1
				var year = date[1]
				getTopPhrases(month, year)
			}
			monthPhraseSelector.innerHTML += "<option>" + response["dates"][i] + "</option>"
		}
	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}


function articleCountChart() {
	var transformedData = google.visualization.arrayToDataTable(articleCountData);
	var view = new google.visualization.DataView(transformedData);
	view.setColumns([0, 1,
					   { calc: "stringify",
						 sourceColumn: 1,
						 type: "string",
						 role: "annotation" },
					   2]);

	var options = {
		title: "Number of Articles per Month",
		width: 825,
		height: 300,
		bar: {groupWidth: "95%"},
		legend: { position: "none" },
		animation: {startup: true, duration: 1000, easing: 'inAndOut'}
	};
	var chart = new google.visualization.BarChart(document.getElementById("articleCountChart"));
	chart.draw(view, options);
}

function getFacebookEngagementChartData() {
	$.ajax({
	type: "GET",
	url: "/getSourceFacebookEngagement",
	data: {
		source: source
	},
	success: function(response) {
		// Header for data
		facebookEngagementData[0] = ["Month", "Facebook Shares", "Facebook Comments", "Facebook Reactions"]

		// Populate data array used for chart
		var row = 1
		for (var month in response) {
			var monthData = response[month]
			var shares = monthData["shares"]
			var comments = monthData["comments"]
			var reactions = monthData['reactions']
			facebookEngagementData[row] = [month, shares, comments, reactions]
			row += 1
		} 

		google.charts.setOnLoadCallback(facebookEngagementChart);
	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}

function facebookEngagementChart() {
	var transformedData = google.visualization.arrayToDataTable(facebookEngagementData);
	var options = {
		  title: 'Facebook Engagement',
		  curveType: 'function',
		  legend: { position: 'bottom' },
		  animation: {startup: true, duration: 1000, easing: 'inAndOut'}
	};
	var chart = new google.visualization.LineChart(document.getElementById('facebookEngagementChart'));

	chart.draw(transformedData, options);
}

function getFeaturedArticles() {
	$.ajax({
	type: "GET",
	url: "/getMostSharedArticles",
	data: {
		source: source
	},
	success: function(response) {
		var articles = response["articles"]
		for (var i=0; i < articles.length; i++) {
			url = articles[i]["url"]
			title = articles[i]["title"]
			shares = articles[i]["shares"]
			$("#featuredArticles").append("<tr><td><a style='font-weight:600' href='" + url + "' target='_blank'>" + title + "</a></td><<td>" + shares + "</td></tr>");
		}

	},
	error: function(chr) {
	  console.log("Error!")
	}
  });

}

// Update shown top phrases when user clicks new month
function updateTopPhrases(sel) {
	var date = sel.value.split(" ")
	var month = abbrevMonths.indexOf(date[0]) + 1
	var year = date[1]
	getTopPhrases(month, year)
}

function getTopPhrases(monthInt, year) {
	$.ajax({
	type: "GET",
	url: "/getTopSourcePhrases",
	data: {
		source: source,
		month: monthInt,
		year: year
	},
	success: function(response) {
		$("#topPhrases").html("");
		var phrases = response["orderedPhrases"]
		for (var i=0; i < phrases.length; i++) {
			$("#topPhrases").append("<div class='phrase'><center>" + phrases[i] + "<center></div>");
		}
	},
	error: function(chr) {
	  console.log("Error!")
	}
  });
}
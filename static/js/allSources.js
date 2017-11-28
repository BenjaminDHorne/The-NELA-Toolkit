// Populate two tables with all source
$(document).ready(function () {
	var numSources = sources.length
	for (var i=0; i < numSources; i++) {
		//Split up sources into two tables
		var tableId = "#allSources" + Math.floor(i/(numSources/3))
		var imgHTML = "<img src='/static/newsSourceImages/" + sourceData[sources[i]]["imageName"] + "' style='width:75px' >"
		$(tableId).append("<tr><td>" + imgHTML + "</td><td class='clickableRow' style='vertical-align: middle; font-size: large; font-weight: 700'>" + sources[i] + "</td></tr>")
	}
});

// Take user to source page when row is clicked
jQuery(document).ready(function() {
    $(".clickableRow").click(function() {
    	source = $(this).text();
        window.location.href = "/newsSource?source=" + source;
    });
});
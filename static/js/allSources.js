// Populate two tables with all source
$(document).ready(function () {
	getAllSources()
});


// Gets all sources stored in the database
function getAllSources() {
	$.ajax({
		type: "GET",
		url: "/getAllSources",
		success: function(response) {
			sources = response["sources"]
			addSourcesToView(sources)
		},
		error: function(chr) {
		 	console.log("Error!")
		}
	});
}

function addSourcesToView(sources) {
	var numSources = sources.length

	for (var i=0; i < numSources; i++) {
		//Split up sources into two tables
		var tableId = "#allSources" + Math.floor(i/(numSources/3))
		var imgHTML = "<img src='/static/newsSourceImages/" + sourceData[sources[i]]["imageName"] + "' style='width:75px;' >"
		$(tableId).append("<tr><td style='height:100px'>" + imgHTML + "</td><td class='clickableRow' style='vertical-align: middle; font-size: large; font-weight: 700'>" + sources[i] + "</td></tr>")
	}
	
	$(".clickableRow").click(function() {
    	source = $(this).text();
        window.location.href = "/newssource?source=" + source;
    });

}

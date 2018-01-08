function createPieChart(element, title, data) {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
	/* Data Example:
	 * [
	 * ['Task', 'Hours per Day'],
	 * ['Work',     11],
	 * ['Eat',      2],
	 * ['Commute',  2],
	 * ['Watch TV', 2],
	 * ['Sleep',    7]
	 * ]
	 */

        var dataTable = google.visualization.arrayToDataTable(data);

        var options = {
          title: title
        };

        var chart = new google.visualization.PieChart(document.getElementById(element));

        chart.draw(dataTable, options);
      }
}

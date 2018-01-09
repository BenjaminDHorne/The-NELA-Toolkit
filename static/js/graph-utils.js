function drawChart(type, element, title, data, options) {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(chartCallback);

      function chartCallback() {
        var dataTable = google.visualization.arrayToDataTable(data);

        options["title"] = title;
        options["chartArea"] = {width: '50%'};

        if (type == "Pie") {
          type = google.visualization.PieChart;
        }
        else if (type == "Bar") {
          type = google.visualization.BarChart;
        }

        var chart = new type(document.getElementById(element));

        chart.draw(dataTable, options);
      }
}

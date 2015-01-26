function columnChartDraw(columnChart_datatable, title, divselect){

      var data = google.visualization.arrayToDataTable(columnChart_datatable);
      var options = {
                      title: title,
                      hAxis: {title: 'Lead status'},
                      vAxis: {title: 'No. of Leads'}
                    };

      var chart = new google.visualization.ColumnChart(document.getElementById(divselect));

      chart.draw(data, options);
 
 }

 function pieChartDraw(piechart_datatable,title, divselect){

        var data = google.visualization.arrayToDataTable(piechart_datatable);

        var options = {title: title};

        var chart = new google.visualization.PieChart(document.getElementById(divselect));

        chart.draw(data, options);
 
}

function lineChartDraw(linechart_datatable, title, divselect){

		var data = google.visualization.arrayToDataTable(linechart_datatable)

		var options = {
          title: title,
          curveType: 'function',
          legend: { position: 'bottom' }
        };

    var chart = new google.visualization.LineChart(document.getElementById(divselect));

	chart.draw(data, options);
}
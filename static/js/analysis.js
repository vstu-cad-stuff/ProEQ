google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var jsonData = JSON.parse($.ajax({
    url: "/dashboard/analysis?file=" + filename_url,
    dataType: 'json',
    method: 'post',
    async: false
  }).responseText).data;

  var data = new google.visualization.arrayToDataTable(jsonData);

  var options = {
    title: 'Загруженные данные',
    chartArea: { width: '85%', height: '85%' },
    legend: 'none'
  };

  var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}
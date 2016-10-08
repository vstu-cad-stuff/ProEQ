google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function gId(name) {
  return document.getElementById(name);
}

function drawChart() {
  var jsonData = JSON.parse($.ajax({
    url: '/dashboard/analysis?file=' + filename_url,
    dataType: 'json',
    method: 'post',
    async: false
  }).responseText);

  gId('point_count').innerHTML = jsonData.count;
  gId('point_period').innerHTML = jsonData.period;
  gId('point_range').innerHTML = '[' + jsonData.range[0] + ', ' + jsonData.range[1] + ']';
  var data = new google.visualization.arrayToDataTable(jsonData.data);

  var options = {
    title: 'Загруженные данные',
    chartArea: { width: '85%', height: '85%' },
    legend: 'none'
  };

  var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}

function SendData() {
  send_data = {
    alphabet_len:   parseInt(gId('alphabet_len').value),
    window_len:     parseInt(gId('window_len').value),
    train_range:    [parseInt(gId('train_start').value), parseInt(gId('train_end').value)],
    forecast_range: [parseInt(gId('forecast_start').value), parseInt(gId('forecast_end').value)]
  };
  $.ajax({
    contentType: 'application/json',
    url: '/dashboard/model',
    dataType: 'json',
    type: 'POST',
    data: JSON.stringify(send_data)
  });
}
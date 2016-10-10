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
    chartArea: { width: '85%', height: '75%' },
    legend: 'none'
  };

  var chart = new google.visualization.LineChart(gId('curve_chart'));

  chart.draw(data, options);
}

function SendData() {
  send_data = {
    alphabet_len:   parseInt(gId('alphabet_len').value),
    window_len:     parseInt(gId('window_len').value),
    train_range:    [parseInt(gId('train_start').value), parseInt(gId('train_end').value)],
    forecast_range: [parseInt(gId('forecast_start').value), parseInt(gId('forecast_end').value)],
    // magic for html page
    filename:       filename_url,
  };
  $.ajax({
    contentType: 'application/json',
    url: '/dashboard/model',
    dataType: 'json',
    type: 'POST',
    data: JSON.stringify(send_data),
    success: function (data) {
      gId('mape_error').innerHTML = 'MAPE: ' + data.errors.mape.toFixed(2) + ' %';
      gId('mae_error').innerHTML = 'MAE: ' + data.errors.mae.toFixed(2);
      gId('mse_error').innerHTML = 'MSE: ' + data.errors.mse.toFixed(2);
      gId('rmse_error').innerHTML = 'RMSE: ' + data.errors.rmse.toFixed(2);
      gId('me_error').innerHTML = 'ME: ' + data.errors.me.toFixed(2);
      gId('sd_error').innerHTML = 'SD: ' + data.errors.sd.toFixed(2);
      var rf_data = google.visualization.arrayToDataTable(data.data);
      var options = {
        title: 'Предсказанные данные',
        chartArea: { width: '85%', height: '75%' },
        curveType: 'function',
        legend: { position: 'bottom' }
      };

      var chart = new google.visualization.LineChart(gId('forecast_chart'));

      chart.draw(rf_data, options);
    }
  });
}
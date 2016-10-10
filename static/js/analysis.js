window.onload = function() {
  drawChart();
}

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
  var chart = c3.generate({
    bindto: '#curve_chart',
    size: {
      width: 480,
      height: 300
    },
    data: {
      x: 'x',
      rows: jsonData.data,
      names: {
        // use custom data from js
        y: 'power consumption data'
      }
    },
    point: { show: false },
    axis: {
      x: {
        // use custom data from js
        label: '15 minute intervals',
        tick: {
          count: 48,
          format: function (x) { return Math.round(x); }
        }
      },
      y: {
        // use custom data from js
        label: 'power consumption',
      }
    }
  });
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
      var chart = c3.generate({
        bindto: '#forecast_chart',
        size: {
          width: 480,
          height: 300
        },
        data: {
          x: 'x',
          rows: data.data,
          names: {
            // use custom data from js
            real: 'real power consumption',
            forecast: 'predict power consumption'
          }
        },
        point: { show: false },
        axis: {
          x: {
            // use custom data from js
            label: '15 minute intervals',
            tick: {
              count: 48,
              format: function (x) { return Math.round(x); }
            }
          },
          y: {
            // use custom data from js
            label: 'power consumption',
          }
        }
      });
    }
  });
}
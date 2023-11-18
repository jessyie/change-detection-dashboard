// Function to fetch and update chart data
function updateCharts(selectedYear) {

  fetch(`/update_charts?year=${selectedYear}`)
  .then(response => response.json())
  .then(data => {
    
    // Update chart configuration and data based on the fetched data
    document.querySelector('#map-container1').innerHTML = data.world_map
    document.querySelector('#map-container2').innerHTML = data.world_map2
    document.querySelector('#map-container3').innerHTML = data.world_map3


    chart1.update({
      chart: {
            zoomType: 'x',
            style: {
                fontSize: '15px',
          
        }
        },
        title: {
            text: 'NDVI TIME SERIES',
            align: 'center'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
            align: 'left'
        },
        xAxis: {
            categories: data.graph1AXA
        },
        yAxis: {
            title: {
                text: 'NDVI'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        credits: {
            enabled: false
        },

        series: [{
            type: 'area',
            name: 'NDVI Data',
            data: data.graph1AYA
        }]
   
  });


    chart2.update({
      chart: {
            zoomType: 'x',
            style: {
                fontSize: '15px',
          
        }
        },
        title: {
            text: 'LST TIME SERIES',
            align: 'center'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in',
            align: 'left'
        },
        xAxis: {
            categories: data.graph1AX
        },
        yAxis: {
            title: {
                text: 'LST_Day_1km'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        credits: {
            enabled: false
        },

        series: [{
            type: 'area',
            name: 'LST Data',
            data: data.graph1AY
        }]
   
  })


    
  
})
}


// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function changeChartYear() {
  const yearSelector = document.querySelector("#yearSelection")
  activeYear = yearSelector.value || '2021'
  updateCharts(activeYear);
  
}


const BACKGROUND_COLORS = [
  'rgba(54, 162, 235, 0.7)',
  'rgba(255, 99, 132, 0.7)',
  'rgba(255, 206, 86, 0.7)',
  'rgba(75, 192, 192, 0.7)',
  'rgba(153, 102, 255, 0.7)',
  'rgba(255, 159, 64, 0.7)'
];

const BORDER_COLORS = [
  'rgba(54, 162, 235, 1)',
  'rgba(255, 99, 132, 1)',
  'rgba(255, 206, 86, 1)',
  'rgba(75, 192, 192, 1)',
  'rgba(153, 102, 255, 1)',
  'rgba(255, 159, 64, 1)'
];

console.log(Chart.defaults);

Chart.defaults.scale.grid.borderColor = 'rgba(255,255,255,0.5)';
Chart.defaults.scale.grid.color = 'rgba(255,255,255,0.5)';
Chart.defaults.color = 'rgba(255,255,255,0.5)';
Chart.defaults.plugins.legend.position = 'bottom';

function addCustomerStringingsChart() {
  const ctx = document.getElementById('customer-stringings-chart');

  if (!ctx) {
    return;
  }

  const datasets = [];

  for (let i = 0; i < customerStringingsChartData.data.length; i++) {
    datasets.push({
      label: customerStringingsChartData.labels[i],
      data: [customerStringingsChartData.data[i]],
      backgroundColor: BACKGROUND_COLORS[i % BACKGROUND_COLORS.length],
      borderColor: BORDER_COLORS[i % BACKGROUND_COLORS.length],
      borderWidth: 2,
      borderRadius: 10,
    })
  }

  ctx.getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [''],
      datasets: datasets,
    },
    options: {
      backgroundColor: 'rgba(255,255,255,0.1)',
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      scales: {
        x: {
          pointLabels: {
            display: false,
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      },
    }
  });
}

function addRacquetsByBrandChart() {
  const ctx = document.getElementById('racquets-by-brand-chart');

  if (!ctx) {
    return;
  }

  ctx.getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: racquetsByBrandChart["labels"],
      datasets: [{
        label: '# of racquets of the brand',
        data: racquetsByBrandChart["data"],
        backgroundColor: BACKGROUND_COLORS,
        borderColor: BORDER_COLORS,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
    }
  });
}

function addStringingsChartData() {
  const ctx = document.getElementById('stringings-chart');

  if (!ctx) {
    return;
  }

  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: stringingsChartData.labels,
      datasets: [{
        label: 'Number of stringings per month/year',
        data: stringingsChartData.data,
        backgroundColor: BACKGROUND_COLORS[0],
        borderColor: BORDER_COLORS[0],
        borderWidth: 2,
        borderRadius: 10,
      }]
    },
    options: {
      backgroundColor: 'rgba(255,255,255,0.1)',
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          }
        }
      }
    }
  });
}

addStringingsChartData();
addCustomerStringingsChart();
addRacquetsByBrandChart();

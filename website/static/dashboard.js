const BACKGROUND_COLORS = [
  'rgba(255, 99, 132, 0.7)',
  'rgba(54, 162, 235, 0.7)',
  'rgba(255, 206, 86, 0.7)',
  'rgba(75, 192, 192, 0.2)',
  'rgba(153, 102, 255, 0.2)',
  'rgba(255, 159, 64, 0.2)'
];

const BORDER_COLORS = [
  'rgba(255, 99, 132, 1)',
  'rgba(54, 162, 235, 1)',
  'rgba(255, 206, 86, 1)',
  'rgba(75, 192, 192, 1)',
  'rgba(153, 102, 255, 1)',
  'rgba(255, 159, 64, 1)'
];

console.log(Chart.defaults);

Chart.defaults.scale.grid.borderColor = 'rgba(255,255,255,0.5)';
Chart.defaults.scale.grid.color = 'rgba(255,255,255,0.5)';
Chart.defaults.color = 'rgba(255,255,255,0.5)';

function addCustomerStringingsChart() {
  const ctx = document.getElementById('customer-stringings-chart');

  if (!ctx) {
    return;
  }

  ctx.getContext('2d');
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: customerStringingsChartData["labels"],
      datasets: [{
        label: 'Number of stringings',
        data: customerStringingsChartData["data"],
        backgroundColor: BACKGROUND_COLORS,
        borderColor: BORDER_COLORS,
        borderWidth: 2
      }]
    },
    options: {
      backgroundColor: 'rgba(255,255,255,0.1)',
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            // forces step size to be 50 units
            stepSize: 1
          }
        }
      }
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
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Number of racquets by brand'
        }
      }
    }
  });
}

addCustomerStringingsChart();
addRacquetsByBrandChart();

import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

// Chart.js Komponenten registrieren
ChartJS.register(ArcElement, Tooltip, Legend, Title);

const PieChart = ({ data, title, icon }) => {
  // Daten für Chart.js formatieren
  const chartData = {
    labels: data.map(item => item.label),
    datasets: [
      {
        data: data.map(item => item.value),
        backgroundColor: data.map(item => item.color),
        borderColor: data.map(item => item.borderColor || 'rgba(255, 255, 255, 0.1)'),
        borderWidth: 2,
        hoverBorderWidth: 3,
        hoverBorderColor: 'rgba(255, 255, 255, 0.8)',
      },
    ],
  };

  // Chart-Optionen
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false, // Wir erstellen eine eigene Legende
      },
      tooltip: {
        backgroundColor: 'rgba(26, 26, 26, 0.95)',
        titleColor: '#ffffff',
        bodyColor: '#a0a0a0',
        borderColor: 'rgba(0, 212, 170, 0.5)',
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true,
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${label}: €${value.toLocaleString('de-DE', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })} (${percentage}%)`;
          }
        }
      },
    },    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 800,
      easing: 'easeOutQuart'
    },
    elements: {
      arc: {
        borderAlign: 'inner',
        borderJoinStyle: 'round',
      }
    }
  };

  // Gesamtwert berechnen
  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="chart-container">
      <h3 className="chart-title">
        {icon} {title}
      </h3>
      
      <div className="chart-wrapper">
        <Pie data={chartData} options={options} />
      </div>
      
      {/* Eigene Legende */}
      <div className="chart-legend">
        {data.map((item, index) => (
          <div key={index} className="legend-item">
            <div 
              className="legend-color" 
              style={{ backgroundColor: item.color }}
            ></div>
            <span>{item.label}</span>
          </div>
        ))}
      </div>
      
      {/* Statistiken */}
      <div className="chart-stats">
        <div className="total-value">
          €{totalValue.toLocaleString('de-DE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })}
        </div>
        <div className="asset-count">
          {data.length} {data.length === 1 ? 'Asset' : 'Assets'}
        </div>
      </div>
    </div>
  );
};

export default PieChart;

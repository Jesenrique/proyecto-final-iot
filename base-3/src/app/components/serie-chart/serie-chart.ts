import { CommonModule } from '@angular/common';
import { Component, computed, input } from '@angular/core';
import { Chart, ChartConfiguration, ChartOptions, registerables } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import 'chartjs-adapter-date-fns';
import { es } from 'date-fns/locale';
import { DataHistorial } from '../../interfaces/dataHistorial';

Chart.register(...registerables);

type ChartStatus = 'normal' | 'alerta' | 'critico';

@Component({
  selector: 'app-serie-chart',
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './serie-chart.html',
  styleUrl: './serie-chart.css',
})
export class SerieChart {
  dataHistorial = input.required<DataHistorial[]>();
  status = input<ChartStatus>('normal');

  // Paleta semantica segun estado del panel.
  tone = computed(() => {
    switch (this.status()) {
      case 'critico':
        return {
          line: '#dc2626',
          area: 'rgba(220, 38, 38, 0.14)',
          point: '#991b1b',
        };
      case 'alerta':
        return {
          line: '#d97706',
          area: 'rgba(245, 158, 11, 0.16)',
          point: '#92400e',
        };
      default:
        return {
          line: '#2563eb',
          area: 'rgba(37, 99, 235, 0.14)',
          point: '#1d4ed8',
        };
    }
  });

  lineChartData = computed<ChartConfiguration<'line'>['data']>(() => {
    const datosFormateados = this.dataHistorial().map((item) => ({
      x: item.periodo,
      y: item.promedio,
    }));

    const color = this.tone();

    return {
      datasets: [
        {
          // Cast necesario para compatibilidad de tipos con el eje temporal.
          data: datosFormateados as any[],
          label: 'Presion (PSI)',
          fill: true,
          tension: 0.32,
          borderWidth: 2,
          borderColor: color.line,
          backgroundColor: color.area,
          pointBackgroundColor: color.point,
          pointBorderColor: '#ffffff',
          pointBorderWidth: 1,
          pointRadius: 0,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 2,
        },
      ],
    };
  });

  lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.94)',
        titleColor: '#e2e8f0',
        bodyColor: '#f8fafc',
        borderColor: '#334155',
        borderWidth: 1,
        padding: 10,
        displayColors: false,
        callbacks: {
          label: (context) => {
            const value = context.parsed.y;
            return `Presion: ${value} PSI`;
          },
        },
      },
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'minute',
          displayFormats: {
            minute: 'HH:mm',
          },
          tooltipFormat: 'dd/MM/yyyy HH:mm',
        },
        adapters: {
          date: {
            locale: es,
          },
        },
        ticks: {
          color: '#64748b',
          maxTicksLimit: 8,
          font: {
            size: 11,
          },
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.18)',
        },
        title: {
          display: true,
          text: 'Tiempo',
          color: '#64748b',
          font: {
            size: 11,
            weight: 600,
          },
        },
      },
      y: {
        beginAtZero: false,
        ticks: {
          color: '#64748b',
          maxTicksLimit: 6,
          font: {
            size: 11,
          },
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.16)',
        },
        title: {
          display: true,
          text: 'Presion (PSI)',
          color: '#64748b',
          font: {
            size: 11,
            weight: 600,
          },
        },
      },
    },
  };

  lineChartLegend = false;
}

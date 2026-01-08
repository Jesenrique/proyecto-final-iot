import { Component, computed, input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';

// 1. IMPORTAR FUNCIONALIDADES DE CHART.JS
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';
import { Chart, registerables } from 'chart.js';

// 2. IMPORTAR EL ADAPTADOR DE FECHA Y EL IDIOMA
import 'chartjs-adapter-date-fns';
import { es } from 'date-fns/locale';

import 'chartjs-adapter-date-fns';
import { DataHistorial } from '../../interfaces/dataHistorial';

// 3. Registras todo
Chart.register(...registerables);

// Registrar los componentes
//Chart.register(...registerables);

@Component({
  selector: 'app-serie-chart',
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './serie-chart.html',
  styleUrl: './serie-chart.css',
})
export class SerieChart {

  dataHistorial = input.required<DataHistorial[]>();


  public lineChartData = computed<ChartConfiguration<'line'>['data']>(() => {
    const datosCrudos = this.dataHistorial();
    // Transformamos los datos del backend al formato X/Y de ChartJS
    const datosFormateados = datosCrudos.map(item => ({
      x: item.periodo,
      y: item.promedio
    }));

    // Retornamos la estructura compleja que pide la librería
    return {
      datasets: [
        {
          // se debe castear como any por que typescript pone problema por 
          // tipo de dato para los ejes
          data: datosFormateados as any[],
          label: 'Presión (PSI)',
          fill: true,
          tension: 0.4,
          borderColor: 'blue',
          backgroundColor: 'rgba(0,0,255,0.2)'
        }
      ]
    };
  });

  // --- CONFIGURACIÓN DE OPCIONES (Cómo se ve) ---
  public lineChartOptions: ChartOptions<'line'> = {
    responsive: true,
    scales: {
      // CONFIGURACIÓN DEL EJE X (TIEMPO)
      x: {
        type: 'time', // <--- ESTO ES LO MÁS IMPORTANTE
        time: {
          unit: 'minute', // Queremos ver minutos
          displayFormats: {
            minute: 'HH:mm' // Formato visual: "10:30"
          },
          tooltipFormat: 'dd/MM/yyyy HH:mm' // Al pasar el mouse
        },
        adapters: {
          date: {
            locale: es // Usar español
          }
        },
        title: {
          display: true,
          text: 'Tiempo (Hora)'
        }
      },
      // CONFIGURACIÓN DEL EJE Y (VALOR)
      y: {
        beginAtZero: false, // No forzar que empiece en 0 si la presión es alta
        title: {
          display: true,
          text: 'Presión (PSI)'
        }
      }
    }
  };

  public lineChartLegend = true;
}
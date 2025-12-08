import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';

// 1. IMPORTAR FUNCIONALIDADES DE CHART.JS
import { ChartConfiguration, ChartOptions, ChartType } from 'chart.js';
import { Chart, registerables } from 'chart.js';

// 2. IMPORTAR EL ADAPTADOR DE FECHA Y EL IDIOMA
import 'chartjs-adapter-date-fns';
import { es } from 'date-fns/locale';

import 'chartjs-adapter-date-fns'; 

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
   // --- CONFIGURACIÓN DE DATOS (Lo que se pinta) ---
  public lineChartData: ChartConfiguration<'line'>['data'] = {
    datasets: [
      {
        data: [
          // Fíjate en el formato: X es fecha (String ISO), Y es valor
          { x: '2023-10-27T10:00:00', y: 120 },
          { x: '2023-10-27T10:05:00', y: 125 },
          { x: '2023-10-27T10:10:00', y: 122 },
          { x: '2023-10-27T10:15:00', y: 130 },
          { x: '2023-10-27T10:20:00', y: 145 }, // Pico de presión
          { x: '2023-10-27T10:25:00', y: 135 },
        ] as any[],
        label: 'Presión de Caldera (PSI)',
        fill: true, // Rellenar el área bajo la curva
        tension: 0.4, // Suavizado de la curva (0 es rectas, 1 es muy curvo)
        borderColor: 'blue',
        backgroundColor: 'rgba(0,0,255,0.2)'
      }
    ]
  };

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


import { Component, computed, inject, Signal, signal } from '@angular/core';
import { DbManometros } from '../../services/db-manometros';
import { WSService } from '../../services/ws-service';
import { DataManometro } from '../../interfaces/dataManometro';
import { FrameSeriesGraphic } from '../frame-series-graphic/frame-series-graphic';

@Component({
  selector: 'app-data-chart',
  imports: [FrameSeriesGraphic],
  templateUrl: './data-chart.html',
  styleUrl: './data-chart.css'
})
export class DataChart {

  // manometroLastValue = signal(120);
  // manometroID = signal(1)
  // Asumamos que este componente solo muestra el ID 5
  private manometroId = '1';
  private dbService = inject(DbManometros);

  // Creamos una Signal CALCULADA reactiva
  LastValue = computed(() => {
    // Busca el objeto por ID en el array global
    const manometro = this.dbService.dataManometros().find(m => m.id_manometro == this.manometroId);

    // Devuelve solo el valor de la lectura
    return manometro ? manometro.ultima_lectura : null;
  });

  cargarDatos(rango: string) {
    // Correcto: Solo los valores, en orden
    this.dbService.obtenerHistorico("1", "2024-12-07T10:00:00", "2024-12-07T11:00:00")
      .subscribe(datos => {
        console.log('Datos recibidos:', datos);
        // Aquí asignarías los datos a tu gráfica
      });
  }
  
}
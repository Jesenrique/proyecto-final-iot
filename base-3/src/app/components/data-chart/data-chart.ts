import { Component, computed, inject, Input, Signal, signal } from '@angular/core';
import { DbManometros } from '../../services/db-manometros';
import { WSService } from '../../services/ws-service';
import { DataManometro } from '../../interfaces/dataManometro';
import { FrameSeriesGraphic } from '../frame-series-graphic/frame-series-graphic';
import { DataHistorial } from '../../interfaces/dataHistorial';


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
  private dbService = inject(DbManometros);

  //se crea la señal que me permite pasar los datos al siguiente compoenente
  datosGrafica = signal<DataHistorial[]>([]);
  manometroId = signal<string>('');

  @Input() 
  set id(manometroIdRouter: string) {
    // Apenas el router nos manda el dato, actualizamos la señal
    this.manometroId.set(manometroIdRouter);

    this.cargarDatos('day'); 
  }

  // Creamos una Signal CALCULADA reactiva
  LastValue = computed(() => {
    const currentId = this.manometroId();
    // Busca el objeto por ID en el array global
    const manometro = this.dbService.dataManometros().find(m => m.id_manometro == currentId);

    // Devuelve solo el valor de la lectura
    return manometro ? manometro.ultima_lectura : null;
  });

  cargarDatos(rango: string) {
    const id = this.manometroId();
    // Correcto: Solo los valores, en orden
    console.log(rango)
    this.dbService.obtenerHistorico(id, rango)
      .subscribe(datos => {
        console.log('Datos recibidos:', datos);
        this.datosGrafica.set(datos);
        // Aquí asignarías los datos a tu gráfica
      });
  }
  
}
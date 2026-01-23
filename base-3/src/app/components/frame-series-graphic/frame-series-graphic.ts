import { Component, input, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SerieChart } from '../serie-chart/serie-chart';
import { DataHistorial } from '../../interfaces/dataHistorial';


@Component({
  selector: 'app-frame-series-graphics',
  standalone: true,
  imports: [CommonModule, SerieChart],
  templateUrl: './frame-series-graphic.html',
  styleUrls: ['./frame-series-graphic.css']
})
export class FrameSeriesGraphic {
  
  rangoActivo = signal<string>('1H');
  rangoCambiado = output<string>();

  lastValue = input.required()
  dataGrafica = input.required<DataHistorial[]>();

  public rangoSeleccionado: 'hour' | 'day' | 'week' | 'month' | 'year' = 'hour';

  cambiarRango(rango: string) {
    this.rangoActivo.set(rango);
    // 2. ¡Tocar el timbre!
    this.rangoCambiado.emit(rango);
  }


}

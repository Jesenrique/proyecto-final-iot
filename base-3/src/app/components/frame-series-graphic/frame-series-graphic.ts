import { Component, input, output, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SerieChart } from '../serie-chart/serie-chart';


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
  public rangoSeleccionado: '1H' | '1D' | '1S' | '1M' | '1A' = '1H';

  cambiarRango(rango: string) {
    this.rangoActivo.set(rango);
    // 2. ¡Tocar el timbre!
    this.rangoCambiado.emit(rango);
  }


}

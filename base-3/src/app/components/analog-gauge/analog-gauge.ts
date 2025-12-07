import { Component, input, InputSignal, Signal, ViewEncapsulation } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NgxGaugeModule } from 'ngx-gauge';

export type NgxGaugeType = 'full' | 'arch' | 'semi';

@Component({
  selector: 'app-analog-gauge',
  imports: [NgxGaugeModule,RouterModule],
  templateUrl: './analog-gauge.html',
  encapsulation: ViewEncapsulation.ShadowDom
})
export class AnalogGauge { 
  value=input.required<number>()          // valor actual del manómetro
  min = 0;
  max = 100;
  gaugeType: NgxGaugeType = 'arch';

  // sectores de colores estilo manómetro
  thick = 15;
  size = 250;

  thresholdConfig = {
    '0': { color: '#3498db' },      // azul (normal)
    '60': { color: '#27ae60' },     // verde
    '80': { color: '#f1c40f' },     // amarillo
    '90': { color: '#e74c3c' }      // rojo (peligro)
  };
}

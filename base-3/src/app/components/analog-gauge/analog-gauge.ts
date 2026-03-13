import { Component, ViewEncapsulation, input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { NgxGaugeModule } from 'ngx-gauge';

export type NgxGaugeType = 'full' | 'arch' | 'semi';

@Component({
  selector: 'app-analog-gauge',
  imports: [NgxGaugeModule, RouterModule],
  templateUrl: './analog-gauge.html',
  encapsulation: ViewEncapsulation.ShadowDom,
})
export class AnalogGauge {
  value = input.required<number>();
  size = input<number>(250);

  min = 0;
  max = 100;
  gaugeType: NgxGaugeType = 'arch';

  // Sectores de color del manometro.
  thick = 15;

  thresholdConfig = {
    '0': { color: '#3498db' },
    '60': { color: '#27ae60' },
    '80': { color: '#f1c40f' },
    '90': { color: '#e74c3c' },
  };
}

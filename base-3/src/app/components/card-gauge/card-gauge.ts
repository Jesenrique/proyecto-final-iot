import { Component, computed, input } from '@angular/core';
import { DatePipe, DecimalPipe} from '@angular/common';
import { AnalogGauge } from '../analog-gauge/analog-gauge';

type GaugeStatus = 'normal' | 'alerta' | 'critico';

@Component({
  selector: 'app-card-gauge',
  imports: [AnalogGauge, DatePipe, DecimalPipe],
  templateUrl: './card-gauge.html',
  styleUrl: './card-gauge.css',
})
export class CardGauge {
  siganlID = input.required<string>();
  signalValue = input.required<number>();
  signalUltimaLectura = input.required<number>();
  signalFecha = input.required<Date | string>();

  status = computed<GaugeStatus>(() => {
    const value = this.signalValue();

    if (value >= 90) {
      return 'critico';
    }

    if (value >= 75) {
      return 'alerta';
    }

    return 'normal';
  });

  statusText = computed(() => {
    switch (this.status()) {
      case 'critico':
        return 'Critico';
      case 'alerta':
        return 'Alerta';
      default:
        return 'Normal';
    }
  });

  statusClass = computed(() => {
    switch (this.status()) {
      case 'critico':
        return 'badge-critico';
      case 'alerta':
        return 'badge-alerta';
      default:
        return 'badge-normal';
    }
  });

  relativeTime(): string {
    const rawDate = this.signalFecha();
    const date = new Date(rawDate);

    if (Number.isNaN(date.getTime())) {
      return 'Sin fecha';
    }

    const diffMs = Date.now() - date.getTime();
    const diffMinutes = Math.floor(diffMs / 60000);

    if (diffMinutes < 1) {
      return 'Hace instantes';
    }

    if (diffMinutes < 60) {
      return `Hace ${diffMinutes} min`;
    }

    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) {
      return `Hace ${diffHours} h`;
    }

    const diffDays = Math.floor(diffHours / 24);
    return `Hace ${diffDays} d`;
  }
}

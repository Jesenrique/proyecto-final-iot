import { CommonModule } from '@angular/common';
import { Component, computed, input, output, signal } from '@angular/core';
import { DataHistorial } from '../../interfaces/dataHistorial';
import { SerieChart } from '../serie-chart/serie-chart';

@Component({
  selector: 'app-frame-series-graphics',
  standalone: true,
  imports: [CommonModule, SerieChart],
  templateUrl: './frame-series-graphic.html',
  styleUrls: ['./frame-series-graphic.css'],
})
export class FrameSeriesGraphic {
  rangoActivo = signal<string>('hour');
  rangoCambiado = output<string>();
  retryRequested = output<void>();

  lastValue = input.required<number | null>();
  dataGrafica = input.required<DataHistorial[]>();
  loading = input<boolean>(false);
  error = input<string | null>(null);

  hasData = computed(() => this.dataGrafica().length > 0);

  // Estado semantico basado en umbrales de PSI.
  panelStatus = computed<'normal' | 'alerta' | 'critico'>(() => {
    const value = this.lastValue();
    if (value === null || value === undefined) {
      return 'normal';
    }

    if (value >= 90) {
      return 'critico';
    }

    if (value >= 75) {
      return 'alerta';
    }

    return 'normal';
  });

  statusText = computed(() => {
    switch (this.panelStatus()) {
      case 'critico':
        return 'Critico';
      case 'alerta':
        return 'Alerta';
      default:
        return 'Normal';
    }
  });

  rangoLabel = computed(() => {
    const map: Record<string, string> = {
      hour: 'ultima hora',
      day: 'ultimo dia',
      week: 'ultima semana',
      month: 'ultimo mes',
      year: 'ultimo ano',
    };

    return map[this.rangoActivo()] ?? 'rango actual';
  });

  // KPIs rapidos para contexto del rango seleccionado.
  summary = computed(() => {
    const points = this.dataGrafica();
    if (!points.length) {
      return { avg: null, max: null, min: null };
    }

    const avg = points.reduce((acc, p) => acc + p.promedio, 0) / points.length;
    const max = Math.max(...points.map((p) => p.max_valor));
    const min = Math.min(...points.map((p) => p.min_valor));

    return { avg, max, min };
  });

  cambiarRango(rango: string) {
    this.rangoActivo.set(rango);
    // Avisamos al componente padre para recargar datos del nuevo rango.
    this.rangoCambiado.emit(rango);
  }

  solicitarReintento() {
    this.retryRequested.emit();
  }
}

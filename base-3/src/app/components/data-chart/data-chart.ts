import { Component, Input, computed, inject, signal } from '@angular/core';
import { FrameSeriesGraphic } from '../frame-series-graphic/frame-series-graphic';
import { DataHistorial } from '../../interfaces/dataHistorial';
import { DbManometros } from '../../services/db-manometros';

@Component({
  selector: 'app-data-chart',
  imports: [FrameSeriesGraphic],
  templateUrl: './data-chart.html',
  styleUrl: './data-chart.css',
})
export class DataChart {
  private dbService = inject(DbManometros);

  datosGrafica = signal<DataHistorial[]>([]);
  manometroId = signal<string>('');
  rangoActual = signal<string>('day');

  loading = signal<boolean>(false);
  error = signal<string | null>(null);

  //recibe datos del componente padre
  @Input()
  set id(manometroIdRouter: string) {
    this.manometroId.set(manometroIdRouter);
    this.cargarDatos('day');
  }

  LastValue = computed(() => {
    const currentId = this.manometroId();
    const manometro = this.dbService
      .dataManometros()
      .find((m) => m.id_manometro === currentId);

    return manometro ? manometro.ultima_lectura : null;
  });

  cargarDatos(rango: string) {
    const id = this.manometroId();

    this.rangoActual.set(rango);
    this.loading.set(true);
    this.error.set(null);

    this.dbService.obtenerHistorico(id, rango).subscribe({
      next: (datos) => {
        this.datosGrafica.set(datos);
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error obteniendo historico:', err);
        this.datosGrafica.set([]);
        this.error.set('No se pudo cargar el historico. Intenta nuevamente.');
        this.loading.set(false);
      },
    });
  }

  reintentarCarga() {
    this.cargarDatos(this.rangoActual());
  }
}

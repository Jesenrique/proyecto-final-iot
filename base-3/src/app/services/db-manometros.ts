import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { DataManometro } from '../interfaces/dataManometro';
import { WSService } from './ws-service';
import { FiltroBusqueda } from '../interfaces/filtroBusqueda';
import { DatoGrafica } from '../interfaces/datoGrafica';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DbManometros {

  private apiUrl = 'http://localhost:8000';

  dataManometros = signal<DataManometro[]>([]);

  private http = inject(HttpClient);
  private wsService =inject(WSService)

  constructor() {
    console.log("Servicio creado!");
    this.getNumeroManometros();
  }


  getNumeroManometros() {
    this.http.get<DataManometro[]>(`${this.apiUrl}/plantas`)
      .subscribe({
        next: (resp) => {
          // Guardamos la lista de manómetros
          this.dataManometros.set(resp);

          resp.forEach(mano => {
            this.wsService.deviceValues.update(map => {
              if (!map.has(mano.id_manometro)) {
                map.set(mano.id_manometro, signal(mano.ultima_lectura));
              } else {
                map.get(mano.id_manometro)!.set(mano.ultima_lectura);
              }
              return map;
            });
          });

          console.log('Número de manómetros:', resp);
          this.dataManometros.set(resp);
        },
        error: (err) => {
          console.error('Error obteniendo manómetros:', err);
        }
      });
  }


  getHistorialLecturas(filtro: FiltroBusqueda): Observable<DatoGrafica[]> {

    const params = new HttpParams()
      .set('id_manometro', filtro.id_manometro)
      .set('fecha_inicio', filtro.fecha_inicio.toISOString()) // Ej: 2025-12-15T10:00:00.000Z
      .set('fecha_fin', filtro.fecha_fin.toISOString())
      .set('granularidad', filtro.granularidad);

    
    return this.http.get<DatoGrafica[]>(`${this.apiUrl}/lecturas/agregadas`, { params });

  }



}


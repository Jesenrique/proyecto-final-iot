import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { DataManometro } from '../interfaces/dataManometro';
import { WSService } from './ws-service';
import { FiltroBusqueda } from '../interfaces/filtroBusqueda';
import { Observable } from 'rxjs';
import { DataHistorial } from '../interfaces/dataHistorial';

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

  /**
   * Obtiene el histórico agregado.
   * @param idManometro ID del manómetro (ej: '1')
   * @param fechaInicio String ISO (ej: '2024-12-07T10:00:00')
   * @param fechaFin String ISO (ej: '2024-12-07T11:00:00')
   */
  obtenerHistorico(idManometro: string, fechaInicio: string, fechaFin: string): Observable<DataHistorial[]> {
    
    // 2. Construcción de parámetros
    // Esto genera: ?id_manometro=1&fecha_inicio=...&fecha_fin=...
    let params = new HttpParams()
      .set('id_manometro', idManometro)
      .set('fecha_inicio', fechaInicio)
      .set('fecha_fin', fechaFin);

    // 3. Petición GET pasando las opciones
    return this.http.get<DataHistorial[]>(`${this.apiUrl}/lecturas/agregadas`, { params });
  }

}

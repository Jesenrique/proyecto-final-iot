import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { DataManometro } from '../interfaces/dataManometro';
import { WSService } from './ws-service';

@Injectable({
  providedIn: 'root'
})
export class DbManometros {

  dataManometros = signal<DataManometro[]>([]);

  private http = inject(HttpClient);
  private wsService =inject(WSService)

  constructor() {
    console.log("Servicio creado!");
    this.getNumeroManometros();
  }

  getNumeroManometros() {
    this.http.get<DataManometro[]>('http://localhost:8000/plantas')
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
}


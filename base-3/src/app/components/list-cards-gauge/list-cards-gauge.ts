import { Component, inject, input, signal } from '@angular/core';
import { CardGauge } from '../card-gauge/card-gauge';
import { WSService } from '../../services/ws-service';
import { AnalogGauge } from '../analog-gauge/analog-gauge';
import { DataManometro } from '../../interfaces/dataManometro';
import { RouterLink } from '@angular/router';
import { DbManometros } from '../../services/db-manometros';

@Component({
  selector: 'app-list-cards-gauge',
  imports: [CardGauge, RouterLink],
  templateUrl: './list-cards-gauge.html',
  styleUrl: './list-cards-gauge.css'
})
export class ListCardsGauge {

  //inyecto el servicio para conocer el numero de manometros
  private db=inject(DbManometros)
  dataManometros=this.db.dataManometros
  
  private wsService = inject(WSService);
  devices = this.wsService.deviceValues;


    getSignal(id: string) {
    const map = this.devices();
    
    if (!map.has(id)) {
      map.set(id, signal<number>(0));
    }

    return map.get(id)!; // siempre existe
  }

}

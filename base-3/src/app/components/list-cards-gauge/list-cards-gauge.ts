import { Component, inject, input, signal } from '@angular/core';
import { CardGauge } from '../card-gauge/card-gauge';
import { WSService } from '../../services/ws-service';
import { AnalogGauge } from '../analog-gauge/analog-gauge';
import { DataManometro } from '../../interfaces/dataManometro';

@Component({
  selector: 'app-list-cards-gauge',
  imports: [CardGauge],
  templateUrl: './list-cards-gauge.html',
  styleUrl: './list-cards-gauge.css'
})
export class ListCardsGauge { 
  
  private wsService = inject(WSService);
  devices = this.wsService.deviceValues;

  dataManometros=input.required<DataManometro[]>();

    getSignal(id: string) {
    const map = this.devices();
    
    if (!map.has(id)) {
      map.set(id, signal<number>(0));
    }

    return map.get(id)!; // siempre existe
  }

}

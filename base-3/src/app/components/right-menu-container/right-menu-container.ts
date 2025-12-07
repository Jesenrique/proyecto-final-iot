import {Component, input, Signal } from '@angular/core';
import { CardGauge } from '../card-gauge/card-gauge';
import { ListCardsGauge } from "../list-cards-gauge/list-cards-gauge";
import { DataManometro } from '../../interfaces/dataManometro';

@Component({
  selector: 'app-right-menu-container',
  imports: [ListCardsGauge],
  templateUrl: './right-menu-container.html',
  styleUrl: './right-menu-container.css'
})
export class RightMenuContainer { 
  dataManometros=input.required<DataManometro[]>();
}

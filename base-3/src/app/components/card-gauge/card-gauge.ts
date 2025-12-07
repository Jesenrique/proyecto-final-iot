import { Component, input, Signal, WritableSignal } from '@angular/core';
import { AnalogGauge } from "../analog-gauge/analog-gauge";
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-card-gauge',
  imports: [AnalogGauge, DatePipe ],
  templateUrl: './card-gauge.html',
  styleUrl: './card-gauge.css',
})
export class CardGauge { 
  //value=input.required<number>();
  siganlID=input.required();
  signalValue = input.required<number>();
  signalUltimaLectura=input.required();
  signalFecha=input.required<Date>();
}

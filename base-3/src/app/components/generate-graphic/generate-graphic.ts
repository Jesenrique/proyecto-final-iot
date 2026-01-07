import { Component } from '@angular/core';
import { RightMenuContainer } from '../right-menu-container/right-menu-container';
import { SerieChart } from "../serie-chart/serie-chart";

@Component({
  selector: 'app-generate-graphic',
  imports: [SerieChart],
  templateUrl: './generate-graphic.html',
  styleUrl: './generate-graphic.css'
})
export class GenerateGraphic { }

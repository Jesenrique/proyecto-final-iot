import { Component} from '@angular/core';
import { RightMenuContainer } from "../../components/right-menu-container/right-menu-container";
import { SideMenu } from '../../components/side-menu/side-menu';
import { ListCardsGauge } from "../../components/list-cards-gauge/list-cards-gauge";


@Component({
  selector: 'app-dashboard-page',
  imports: [ListCardsGauge],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.css'
})
export class DashboardPage { 

  constructor() {
  }
  
}

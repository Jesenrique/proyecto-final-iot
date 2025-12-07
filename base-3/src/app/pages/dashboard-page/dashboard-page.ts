import { Component, inject, signal } from '@angular/core';
import { RightMenuContainer } from "../../components/right-menu-container/right-menu-container";
import { SideMenu } from '../../components/side-menu/side-menu';
import { DbManometros } from '../../services/db-manometros';

@Component({
  selector: 'app-dashboard-page',
  imports: [RightMenuContainer,SideMenu],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.css'
})
export class DashboardPage { 

  //inyecto el servicio para conocer el numero de manometros
  private db=inject(DbManometros)

  dataManometros=this.db.dataManometros

}

import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SideMenu } from "./components/side-menu/side-menu";
import { RightMenuContainer } from "./components/right-menu-container/right-menu-container";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SideMenu, RightMenuContainer],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('base-3');
}

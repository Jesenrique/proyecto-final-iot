import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RightMenuContainer } from '../right-menu-container/right-menu-container';

@Component({
  selector: 'app-side-menu',
  imports: [],
  templateUrl: './side-menu.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SideMenu { }

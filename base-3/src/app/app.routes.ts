import { Routes } from '@angular/router';
import { SideMenu } from './components/side-menu/side-menu';
import { DashboardPage } from './pages/dashboard-page/dashboard-page';
import { AnalogGauge } from './components/analog-gauge/analog-gauge';

export const routes: Routes = [
    {
        path:'',
        component:DashboardPage,
    },
        {
        path:'test',
        component:AnalogGauge,
    },
];

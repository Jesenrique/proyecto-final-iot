import { Routes } from '@angular/router';
import { SideMenu } from './components/side-menu/side-menu';
import { DashboardPage } from './pages/dashboard-page/dashboard-page';
import { AnalogGauge } from './components/analog-gauge/analog-gauge';
import { Chart } from 'chart.js';
import { SerieChart } from './components/serie-chart/serie-chart';

export const routes: Routes = [
    {
        path:'',
        component:DashboardPage,
    },
        {
        path:'test',
        component:SerieChart,
    },
];

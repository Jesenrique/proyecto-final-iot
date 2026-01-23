import { Routes } from '@angular/router';
import { FrameSeriesGraphic } from './components/frame-series-graphic/frame-series-graphic';
import { DataChart } from './components/data-chart/data-chart';

export const routes: Routes = [
    // 1. EL DASHBOARD (Con su sidebar y header)
    {
        path: '',
        loadComponent: () => import('./pages/dashboard-page/dashboard-page').then(m => m.DashboardPage),
        
    },
    
    // 2. LA GRÁFICA (Full Screen)
    // Aunque la URL empieza con 'dashboard/', Angular la trata como una página independiente.
    {
        path: 'dashboard/:id', 
        loadComponent: () => import('./components/data-chart/data-chart').then(m => m.DataChart)
    },
    {
       path: 'test', 
        loadComponent: () => import('./components/data-chart/data-chart').then(m => m.DataChart)
    },
];
 
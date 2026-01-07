import { Routes } from '@angular/router';
import { FrameSeriesGraphic } from './components/frame-series-graphic/frame-series-graphic';
import { DataChart } from './components/data-chart/data-chart';

export const routes: Routes = [
    // 1. EL DASHBOARD (Con su sidebar y header)
    {
        path: 'dashboard',
        loadComponent: () => import('./pages/dashboard-page/dashboard-page').then(m => m.DashboardPage),
        // IMPORTANTE: Aquí NO ponemos children que queramos Full Screen
    },
    
    // 2. LA GRÁFICA (Full Screen)
    // Aunque la URL empieza con 'dashboard/', Angular la trata como una página independiente.
    {
        path: 'dashboard/time-line', 
        loadComponent: () => import('./components/generate-graphic/generate-graphic').then(m => m.GenerateGraphic)
    },
    {
       path: 'test', 
        loadComponent: () => import('./components/data-chart/data-chart').then(m => m.DataChart)
    },
];
 
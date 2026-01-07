export type Granularidad = 'minute' | 'hour' | 'day' | 'week' | 'month';

export interface FiltroBusqueda {
  id_manometro: number;
  fecha_inicio: Date;
  fecha_fin: Date;
  granularidad: Granularidad;
}

export interface DatoGrafica {
  periodo: string; // La fecha truncada que devuelve Postgres
  promedio_valor: number;
  max_valor?: number;
  min_valor?: number;
}
import { Injectable, WritableSignal, signal } from '@angular/core';
import { DeviceData } from '../components/interfaces/deviceData';

@Injectable({ providedIn: 'root' })
export class WSService {

  // Un Mapa donde cada dispositivo tiene su propia señal
  // La clave es el ID del dispositivo (string) y el valor es la señal WritableSignal<number>
  deviceValues = signal<Map<string, WritableSignal<number>>>(new Map());

  constructor() {
    console.log("Servicio WSService inicializado.");
    this.connect();
  }

  private connect() {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onmessage = (msg) => {
      console.log("Llegó:", msg.data);
      
      // Asume que el mensaje es un JSON
      let data: DeviceData;
      try {
        data = JSON.parse(msg.data);
      } catch (e) {
        console.error("Error al parsear el JSON:", e);
        return;
      }

      const id = data.id;
      const value = data.value;

      console.log(id, value)

      // 1. Obtener la señal existente
      const existingSignal = this.deviceValues().get(id);

      if (existingSignal) {
        // 2. Si la señal existe, simplemente actualiza su valor.
        // Esto es reactivo porque el Signal interno está cambiando.
        existingSignal.set(value);
      } else {
        // 3. Si la señal NO existe, debes crear una nueva y añadirla al Map.
        // Para que Angular detecte que el Map ha cambiado, debemos usar .update()
        
        // Crea la nueva señal para el dispositivo
        if (value != undefined) {
          console.log("entra")
          const newSignal = signal<number>(value);

          // Usa update para modificar y devolver un NUEVO Map (o clonado)
          this.deviceValues.update(currentMap => {
            // El Map.set() muta el Map, pero si devuelves el MISMO Map, Angular NO lo detecta.
            // Para solucionarlo, haz un clone (spread) y añade el elemento
            const newMap = new Map(currentMap); // Clonamos el mapa
            newMap.set(id, newSignal);         // Añadimos la nueva señal
            return newMap;                      // Devolvemos el mapa clonado (nueva referencia)
          });
        }
      }
    };
    
    // Opcional: Manejadores de conexión
    ws.onopen = () => console.log("Websocket conectado.");
    ws.onerror = (e) => console.error("Websocket error:", e);
    ws.onclose = () => console.warn("Websocket desconectado.");
  }
}
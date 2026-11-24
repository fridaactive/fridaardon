# Coach Seba · sistema vacío

Copia limpia del sistema: sin clientes, rutinas ni sesiones. Es un solo archivo, `index.html`, con todo el HTML, el CSS y el JavaScript adentro. No necesita compilar nada.

## Cómo probarlo

Abrí `index.html` en el navegador. Fuera de Claude arranca en **modo local**: todo se guarda en el `localStorage` del navegador, en la clave `liftcoach-local`. Sirve para probar, pero cada navegador tiene sus propios datos.

## Cómo conectarlo a tu sistema

Todo el guardado pasa por tres funciones del `<script>`. Cambiando solo estas tres, el resto funciona igual:

| Función | Qué hace hoy | Qué tiene que hacer en tu sistema |
| --- | --- | --- |
| `initStore()` | Carga las 5 colecciones en el objeto `data` y llama a `render()` | Pedir los datos a tu API (o Supabase), cargarlos en `data` y llamar a `render()`. Si tenés tiempo real, actualizá `data` y volvé a llamar a `render()` en cada cambio. |
| `put(col, id, obj)` | Guarda un documento completo | `upsert` del documento `id` en la tabla `col` |
| `del(col, id)` | Borra un documento | `delete` del documento `id` en la tabla `col` |

Los nombres de las funciones están en el script. El resto del código solo lee y escribe `data[col][id]`.

## Datos (5 colecciones)

Cada documento es un objeto JSON. Los ids son texto.

- **clients**: `{ name, age, goal, slots: [{ wd: 0-6 (0=domingo), time: "HH:MM" }], partnerId?, pause?: { from, until, reason, note }, createdAt }`
- **routines**: `{ name, clientId (null = plantilla), days: [{ id, name, focus, weekday, blocks: [{ id, name, superset?, rest?, ex: [ejercicio] }] }], changes: [], updatedAt }`
  - **ejercicio**: `{ id, name, how, mode: "reps"|"time", sets, reps, repsList?, maxReps?, sec, side, rest, unit, trackLoad, startLoad?, level?, coachNote?, retired? }`
- **sessions**: `{ clientId, routineId, dayId, dayName, status: "active"|"done", startedAt, endedAt?, durationMs?, activeMs, stepIdx, stepMs, plan (copia del día), logs: { [exId]: { sets: [{ s, sd, reps|sec, load, level, ms }], rpe, conf, pain, note, skipped?, changedTo? } }, blocks, score, note, duo? }`
- **library**: ejercicios guardados para reutilizar (mismo formato que el ejercicio, sin `id`).
- **attendance**: el id es `clienteId_AAAA-MM-DD_HHMM` → `{ cid, date, time, status?: "vino"|"falto"|"cancelado"|"reprogramado"|"sinclase", reason?, note?, extra?, makeup?: { from, wd } }`

Las cargas se guardan siempre en **libras**. La pantalla convierte a kg cuando hace falta.

## Funciones que dependen de Claude (opcionales)

Si no hay Claude, el sistema sigue funcionando sin estas funciones:

- **Variantes al subir de nivel** (`sample`): sin Claude, ofrece progresiones simples (más nivel, reps o series).
- **Descarga de CSV y reporte** (`downloads`): sin Claude, muestra el texto para copiarlo. En tu sistema podés reemplazarlo por una descarga normal (`Blob` + `<a download>`).
- **Permisos de escritura** (`user`): sin Claude, todos pueden editar. Agregá tus propios roles.

## Externo

Solo carga las fuentes Barlow y Barlow Condensed de Google Fonts. Si no cargan, usa las fuentes del sistema.

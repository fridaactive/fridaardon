# Rutinas y videos de ejercicios

- `videos.md`: lista maestra de ejercicios (con video / falta grabar / volver a grabar), por equipo.
- `grabacion-AAAA-MM-DD.md`: lista para cada día de grabación, con tips.
- `clientes/<nombre>.md`: borrador aprobado de la rutina de cada cliente.

Cómo se conectan los videos: el portal busca el ejercicio en el banco
(Firebase `exerciseBank`) por **nombre exacto** (sin importar mayúsculas).
El nombre en la rutina tiene que ser idéntico al del banco para que salga el video.

## Publicar una rutina (automático)
1. Guardar la rutina aprobada como `clientes/<nombre>.json` (formato: ver `clientes/jocelyn.json`).
2. Agregarla en `publicar.json` con `clave` = SHA-256 del nombre del cliente tal como está en el panel
   (sin tildes, minúsculas, espacios simples) y `version` (subirla para reemplazar).
3. Publicar en main. La próxima vez que Frida abra su panel, se carga sola en la cuenta del cliente
   y los ejercicios nuevos se agregan al banco (sin video).
Si Frida edita la rutina en el panel, no se pisa hasta que se suba una versión mayor.
Ojo: reemplazar una rutina cambia los ids de los ejercicios (el historial anterior queda guardado, pero no se liga a la nueva).

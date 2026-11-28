# Imágenes de planes

Fuentes de las imágenes de `/planes`, que aparecen en el portal de administradora (Cotización).

Para actualizar precios:
1. Editar los precios en los `.html` de esta carpeta.
2. Renderizar cada uno a 1080×1350 con deviceScaleFactor 2 (Playwright) y guardar el PNG en `/planes` con el mismo nombre.
3. Subir `PLANES_VERSION` en `admin.html` para que el celular no muestre la imagen vieja.

Precios vigentes (desde enero 2027, y para toda clienta nueva):
- Presencial: $30 sesión · Starter $240 · Active $360. Plan de alimentación con nutricionista +$20.
- Videollamada: $20 sesión · Starter $160 · Active $240. Incluye guía de alimentación.
- Rutina online: $50/mes. Incluye guía de alimentación.

Precio anterior (solo Ángela): presencial $25 · $200 · $300.

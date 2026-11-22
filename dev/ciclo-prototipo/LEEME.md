# Mi ciclo · "Tu energía de hoy" (prototipo de diseño)

Prototipo visual de la tarjeta del ciclo menstrual para la pestaña Inicio del portal.
No se carga en la web: es una referencia para integrarla en `index.html`.

- `ciclo.css`: estilos (pensados para `body.portal-dark`).
- `ciclo.js`: `cicloCardHtml({ dia, largo, sentir })`, `cicloFase()`, `cicloEnergia()`, `cicloBateriaSvg()`.
  La página debe definir `cicloSentir(id)` con id en 'dolor' | 'nauseas' | 'cansada' | 'bien' | 'contodo' (guardar lo que siente hoy y volver a dibujar).
- `demo.html`: las 4 fases lado a lado. `ciclo-demo.png`: captura.

Ideas clave: batería con líquido y olas animadas, burbujas, rayo cuando la energía sube y "zz" en fase
menstrual; color y nombre propio por fase (Modo recarga, Energía en subida, Tu pico de poder, Modo
constante); barra del ciclo con marcador del día; qué entreno es ideal hoy y qué cuidar; ella marca cómo se siente con caritas dibujadas
(con dolor, con náuseas, cansada, bien, ¡con todo!), recibe un consejo para eso y la batería se ajusta (pesa más lo que ella siente que la
fase); explicación científica corta y sin promesas, siempre con "escucha a tu cuerpo".

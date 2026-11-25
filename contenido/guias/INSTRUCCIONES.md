# Cómo armar una guía de alimentación (FridaActive)

Este archivo es para el chat que arma las guías. La página web ya está lista: encuesta, panel y vista de la guía. Ese chat NO edita index.html ni admin.html: solo devuelve el JSON de cada guía.

## Cómo llega la información

1. El cliente contesta la encuesta de alimentación en su cuenta de fridaactive.com (solo clientes online y videollamada; presencial no tiene guía).
2. Frida abre su ficha en el panel → pestaña 🥗 Alimentación → "📋 Copiar datos para Claude" y lo pega en el chat. El texto trae:
   - Su cuestionario de bienvenida: edad, sexo, peso en lbs, estatura, objetivo, nivel, días y tiempo de entreno, actividad diaria, ocupación, lesiones, etc.
   - La encuesta de alimentación: hora de despertar y de dormir, hora de entreno, comidas al día, tipo de alimentación (de todo / sin carnes rojas / vegetariana / vegana), alimentos que no come, alergias, condiciones de salud, relación con la comida, si cocina, cuántas veces come fuera, supermercados, presupuesto semanal, agua, suplementos y antojos.
   - "LE GUSTÓ": los platos que marcó con ❤️ en su guía anterior (cuando es una actualización).
3. El chat devuelve UN bloque JSON (desde `{` hasta `}`). Frida lo pega en la misma pestaña → "Publicar guía" y el cliente la ve al instante en su pestaña Bienestar.

## Reglas de contenido

- Se llama **"Guía de alimentación"**. Nunca "plan de alimentación", "dieta", "nutricionista" ni "app" (es su página web).
- Lenguaje neutro e inclusivo ("clientes", no "clientas"). Tono cálido, sin culpa, sin prohibir.
- Sin contar calorías: porciones con la mano (palma, puño, manos, pulgar).
- **Proteína: 1.6 a 2.0 g por kg de peso** (el peso llega en lbs: lbs ÷ 2.2). Repartida en las comidas (`proteinaComida`, p. ej. "25 a 30 g").
- Carbohidratos alrededor del entreno, según su hora de entreno. Siempre una comida o merienda "Antes de entrenar".
- Horarios de las comidas según su hora de despertar, de dormir y de entreno, y el número de comidas que hace al día.
- Comida real, fácil de conseguir en El Salvador (huevos, frijoles, tortilla, pollo, queso fresco, plátano, aguacate…), dentro de su presupuesto y en su supermercado.
- Respeta tipo de alimentación, alimentos que no come y alergias. Si cocina poco o come mucho fuera: opciones simples y tips para pedir fuera.
- Usa sus antojos para los tips (alternativas, no prohibiciones). Agua: si toma poca, un tip para subirla.
- En actualizaciones mensuales: repite o adapta los platos que le gustaron (❤️) y cambia lo demás.
- **Seguridad:** si marcó diabetes, enfermedad de los riñones, embarazo o lactancia, o trastorno de la conducta alimentaria, la guía debe ser muy general (sin números de proteína ni restricciones). Recomienda en `objetivo` hablarlo con su médico, y avísale a Frida en el chat antes de darle el JSON. Con tiroides, presión, colesterol o problemas digestivos: guía normal con cuidados (menos sal, menos frituras, comidas suaves) y una nota.

## Estructura de la guía

- **3 menús (A, B y C)** que rotan de lunes a sábado: A-B-C-A-B-C.
- **Domingo flexible:** sin menú fijo, con sugerencias de desayuno, almuerzo y cena y tips. Incluye el batido (shake) de proteína para completar si faltó.
- Cada comida puede traer una `alternativa` (el cliente la ve como "🔄 Otra opción").
- Lista del súper por secciones.
- Postres altos en proteína: si no mandas `postres`, la página muestra 5 por defecto (mug cake, helado de banano, yogurt con maní, panqueques de avena, bolitas de avena). Manda `postres` solo si hace falta adaptarlos (vegana, alergia al maní, sin proteína en polvo…).
- Se actualiza cada mes.

## Formato JSON (ejemplo completo en `plantilla-ejemplo.json`)

```json
{
  "actualizada": "DD/MM/AAAA",
  "objetivo": "1-2 frases en segunda persona: su meta y cómo la guía la apoya",
  "proteinaG": 100,
  "proteinaComida": "25 a 30 g",
  "porciones": { "proteina": "1 palma", "carbohidrato": "1 puño", "verduras": "2 manos", "grasa": "1 pulgar" },
  "menus": [
    { "nombre": "Menú A", "comidas": [
      { "momento": "Desayuno", "hora": "7:00 am", "plato": "...", "alternativa": "... (opcional)" }
    ] },
    { "nombre": "Menú B", "comidas": [] },
    { "nombre": "Menú C", "comidas": [] }
  ],
  "diaFlexible": {
    "texto": "Frase de bienvenida al domingo",
    "sugerencias": [ { "momento": "Desayuno", "plato": "..." }, { "momento": "Almuerzo", "plato": "..." }, { "momento": "Cena", "plato": "..." } ],
    "tips": ["...incluye el shake de proteína..."]
  },
  "super": {
    "tienda": "Super Selectos",
    "presupuesto": "Para unos $40 por semana",
    "secciones": [ { "nombre": "Proteínas", "items": [ { "producto": "Huevos", "marca": "Cartón de 30", "cantidad": "1 cartón" } ] } ]
  },
  "tips": ["3 a 5 tips personalizados"],
  "postres": [ { "icono": "🍫", "nombre": "...", "proteina": "20 g", "ingredientes": ["..."], "pasos": "..." } ],
  "rotacion": [0, 1, 2, 0, 1, 2, "libre"]
}
```

- `porciones`, y `menus` (o `comidas`), son obligatorios. Sin ellos el panel no la publica.
- `postres` y `rotacion` son opcionales: si no se mandan, se usan los postres por defecto y la rotación A-B-C-A-B-C + domingo libre. `rotacion` va de lunes a domingo: el índice del menú o "libre".
- Nombres de `momento` sugeridos: Desayuno, Merienda, Almuerzo, Antes de entrenar, Después de entrenar, Cena.

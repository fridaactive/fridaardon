# Cómo armar una guía de alimentación (FridaActive)

Este archivo es para el chat "Guía de alimentación", que arma las guías y también se encarga del diseño de la guía (index.html: pestaña Bienestar; admin.html: pestaña 🥗 Alimentación). Por cada cliente devuelve el JSON de su guía.

## Cómo llega la información

1. El cliente contesta la encuesta de alimentación en su cuenta de fridaactive.com (solo clientes online y videollamada; presencial no tiene guía).
2. Frida abre su ficha en el panel → pestaña 🥗 Alimentación → "📋 Copiar datos para Claude" y lo pega en el chat. El texto trae:
   - Su cuestionario de bienvenida: edad, sexo, peso en lbs, estatura, objetivo, nivel, días y tiempo de entreno, actividad diaria, ocupación, lesiones, etc.
   - La encuesta de alimentación: hora de despertar y de dormir, hora de entreno, comidas al día, tipo de alimentación (de todo / sin carnes rojas / vegetariana / vegana), alimentos que no come, alergias, condiciones de salud, relación con la comida, si cocina, cuántas veces come fuera, supermercados, presupuesto semanal, agua, suplementos y antojos.
   - "LE GUSTÓ": los platos que marcó con ❤️ en su guía anterior (cuando es una actualización).
3. El chat devuelve UN bloque JSON (desde `{` hasta `}`). Frida lo pega en la misma pestaña → "Publicar guía en su cuenta" y el cliente la ve al instante en su pestaña Bienestar.

## Reglas de contenido

- Se llama **"Guía de alimentación"**. Nunca "plan de alimentación", "dieta", "nutricionista" ni "app" (es su página web).
- Lenguaje neutro e inclusivo ("clientes", no "clientas"). Tono cálido, sin culpa, sin prohibir.
- **Calorías (desde nov 2026):** se calculan con Mifflin-St Jeor y se muestran como referencia, nunca como regla.
  - Base: mujer = 10×kg + 6.25×cm − 5×edad − 161; hombre = … + 5. Peso en lbs ÷ 2.2.
  - × actividad: sentada casi todo el día 1.2; + 1-3 entrenos/sem 1.375; + 4-5 entrenos/sem 1.45 a 1.55; trabajo activo + entrenos 1.6 a 1.725.
  - Mantenimiento = base × actividad. Meta: bajar grasa −300 a −500; tonificar/mantener = mantenimiento; ganar músculo +200 a +300.
  - Macros: proteína primero; grasa 25 a 30 % de la meta (÷ 9); carbohidratos el resto (÷ 4).
  - Cada comida lleva `cal`, `prot`, `carb` y `grasa` aproximados; los 3 menús deben sumar cerca de la meta (± 100).
  - En el chat, darle a Frida el detalle (IMC, mantenimiento, meta, macros y cómo se calculó) antes del JSON.
  - El IMC (kg ÷ m²) solo es referencia para Frida; no va en la guía.
- **Proteína: 1.6 a 2.0 g por kg de peso** (el peso llega en lbs: lbs ÷ 2.2). Repartida en las comidas (`proteinaComida`, p. ej. "25 a 30 g").
- Carbohidratos alrededor del entreno, según su hora de entreno. Siempre una comida o merienda "Antes de entrenar".
- Horarios de las comidas según su hora de despertar, de dormir y de entreno, y el número de comidas que hace al día.
- Comida real, fácil de conseguir en El Salvador (huevos, frijoles, tortilla, pollo, queso fresco, plátano, aguacate…), dentro de su presupuesto y en su supermercado.
- Respeta tipo de alimentación, alimentos que no come y alergias. Si cocina poco o come mucho fuera: opciones simples y tips para pedir fuera.
- Usa sus antojos para los tips (alternativas, no prohibiciones). Agua: si toma poca, un tip para subirla.
- En actualizaciones mensuales: repite o adapta los platos que le gustaron (❤️) y cambia lo demás.
- "NO LE GUSTÓ / CAMBIARÍA": lo que el cliente escribió en la caja ✏️ de cada menú. Respétalo siempre en la siguiente guía.
- **Seguridad:** si marcó diabetes, enfermedad de los riñones, embarazo o lactancia, o trastorno de la conducta alimentaria, la guía debe ser muy general: sin `calorias`, `macros`, `proteinaG` ni `cal`/`prot` por comida (la página entonces cuenta comidas en vez de calorías). Con resistencia a la insulina sin medicamento, Frida decide tras preguntarle. Recomienda en `objetivo` hablarlo con su médico, y avísale a Frida en el chat antes de darle el JSON. Con tiroides, presión, colesterol o problemas digestivos: guía normal con cuidados (menos sal, menos frituras, comidas suaves) y una nota.

## Biblioteca de alimentos

- `biblioteca-alimentos.md` guarda alimentos (con calorías y macros) y comidas ya probadas, por momento del día. Úsala para escoger platos y súmale lo nuevo de cada guía.
- Productos de marca (antojos, snacks): buscar su tabla nutricional; si no aparece, calcular y marcar 🧮. Frida puede mandar foto de la etiqueta para dejarlo exacto.
- Antes de publicar, mostrarle a Frida los 3 menús en el chat (tabla por hora) para que los revise; publicar solo cuando los apruebe.

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
  "calorias": { "meta": 2150, "mantenimiento": 1900 },
  "macros": { "proteina": 105, "carbohidratos": 250, "grasa": 70 },
  "proteinaG": 105,
  "proteinaComida": "25 a 30 g",
  "porciones": { "proteina": "1 palma", "carbohidrato": "1 puño", "verduras": "2 manos", "grasa": "1 pulgar" },
  "menus": [
    { "nombre": "Menú A", "comidas": [
      { "momento": "Desayuno", "hora": "7:00 am", "icono": "🍳", "nombre": "Waffles de avena y banano", "plato": "resumen en una línea", "ingredientes": ["½ taza de avena", "..."], "preparacion": ["Paso 1", "Paso 2"], "foto": "fotos/comidas/waffles.jpg (opcional)", "alternativa": "... (opcional)", "cal": 450, "prot": 28, "carb": 45, "grasa": 15 }
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
    "secciones": [ { "nombre": "Proteínas", "items": [ { "producto": "Huevos", "marca": "Cartón de 30", "cantidad": "1 cartón", "icono": "🥚 (opcional)" } ] } ]
  },
  "tips": ["3 a 5 tips personalizados"],
  "postres": [ { "icono": "🍫", "nombre": "...", "proteina": "20 g", "ingredientes": ["..."], "pasos": "..." } ],
  "rotacion": [0, 1, 2, 0, 1, 2, "libre"]
}
```

- `porciones`, y `menus` (o `comidas`), son obligatorios. Sin ellos el panel no la publica.
- Cada comida: la tarjeta muestra solo `nombre` (corto y antojable, 2 a 6 palabras), hora y calorías; al tocarla se abre su página con foto (o dibujito), `ingredientes` con cantidades exactas y marca, `preparacion` en pasos y la `alternativa`. Siempre mandar `nombre`, `ingredientes` y `preparacion`.
- **Marcas entre asteriscos:** en `ingredientes`, `preparacion`, `plato`, `alternativa` y en el súper (`producto`, `marca`), la marca va así: `1 taza de leche *Dos Pinos Doble Proteína*`. La página la resalta.
- `foto`: ruta de una imagen guardada en la página (Frida manda la foto en el chat y se guarda en `fotos/comidas/`). Si no hay, sale el dibujito.
- `calorias`, `macros`, `icono` y `cal`/`prot`/`carb`/`grasa` son opcionales. Sin `calorias`, el anillo de arriba cuenta comidas. Si no hay `icono`, la página pone uno según el momento (🍳 desayuno, 🍎 merienda, 🍗 almuerzo, 🍌 antes de entrenar, 🥗 cena) o el producto del súper.
- Lo que ve el cliente: anillo "Hoy llevas X de [meta] cal" que se llena al marcar ✓ cada comida, barras de proteína/carbohidratos/grasas, su mantenimiento, la semana L-D con su menú, las comidas con dibujito y calorías, la lista de súper con ✓, postres y tips. Las ✓ se guardan solo en su celular.
- `porciones` ya no se muestra en la página, pero el panel lo sigue pidiendo: mándalo siempre.
- `postres` y `rotacion` son opcionales: si no se mandan, se usan los postres por defecto y la rotación A-B-C-A-B-C + domingo libre. `rotacion` va de lunes a domingo: el índice del menú o "libre".
- Nombres de `momento` sugeridos: Desayuno, Merienda, Almuerzo, Antes de entrenar, Después de entrenar, Cena.

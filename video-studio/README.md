# Estudio de video Frida Active

Herramientas y guía de estilo para editar los reels de Frida Active con el mismo diseño en todos los videos.

## Flujo de trabajo

1. Frida graba siguiendo el guion de grabación del calendario de contenido.
2. Sube todos los clips a la carpeta compartida de Google Drive ("Cualquier persona con el enlace").
3. En el chat "Frida Active · Estudio de video", Claude descarga los clips, los analiza, propone la estructura y edita.
4. Frida revisa y pide ajustes. Al publicar, ella agrega la canción en Instagram.

## Guía de estilo (aprobada en noviembre 2026)

**Lo que sí:**

- Historia contada con frases propias de Frida, no frases genéricas. Empezar con algo cotidiano y terminar recomendando de forma natural, como un consejo a una amiga.
- Frases en letra pequeña: Archivo Black, blanca, mayúsculas, con sombra suave. Aparecen con un desvanecido corto, sin sonido.
- Solo la palabra clave de cada frase se marca, con efecto visual y sonido a la vez:
  - Cursiva elegante (Instrument Serif Italic) en crema `#F5ECCB`, con sonido de brillo suave.
  - Mayúsculas Archivo Black en azul `#1C55E5` con borde blanco, con un "pop".
- Whoosh solo en las transiciones entre escenas. Pocos sonidos y bien puestos (unos 15 en 30 segundos).
- Subtítulos pequeños en la parte baja cuando Frida habla.
- Inicio con una toma que atrape en los primeros 2 segundos.
- Duración de 20 a 30 segundos. Cortes de 1 a 2 segundos.
- Colores naturales. Los clips del iPhone en HDR (HLG) se corrigen con `eq=contrast=1.1:saturation=1.15:gamma=0.92`; `zscale` + `tonemap` los dejaba sobresaturados.
- Video sin música: Frida agrega la canción en Instagram, al 20 o 30% cuando hay voz.

**Frases de énfasis (agregado el 9 de noviembre de 2026):** a Frida le encantó la combinación de serifa gruesa + cursiva de pincel (referencia "Make fitness Reels that everyone Copies"). Se usa para frases importantes en videos y fotos: portada, gancho, cierre y la frase clave del video. No reemplaza a las frases cortas del medio, que siguen en Archivo Black.

- Serifa: Fraunces (peso 720, puntas suaves, letras un poco juntas; minúsculas con la primera en mayúscula). Cursiva: **Norican** (la elegida por Frida), solo para las palabras con emoción. Playball queda como alternativa más fina. Mr Dafoe descartada: "parece escrita de carta".
- Líneas apiladas y centradas, alternando serifa y cursiva, con interlineado muy apretado. La cursiva va un poco girada hacia arriba y sus trazos se montan sobre la serifa.
- Colores: todo crema (como la referencia), blanco + amarillo, o crema + azul con borde blanco. Nada de rosado.
- Mejor sobre una zona oscura o lisa de la toma. Sombra suave, sin recuadros.
- Se genera con `scripts/enfasis.py` (imagen fija, sobre foto, o animación con transparencia).

**Lo que no (probado y descartado):**

- Recuadros de color detrás del texto.
- Letras burbuja 3D (se ven de caricatura).
- Textos grandes con frases genéricas ("recargada", "hora de recargar").
- Un sonido por cada palabra: satura.
- Tiempos muertos (manejar, GPS).

## Herramientas

- `scripts/textos.py`: genera la capa de textos animados (frase base + palabra clave marcada) y la lista de momentos para los sonidos.
- `scripts/transcribir.py`: transcribe la voz en español con tiempos por palabra (Vosk), para sincronizar subtítulos.
- `scripts/ejemplo_tumadre.sh`: edición completa del reel de Tu Madre, como plantilla: cortes, transiciones, textos, sonidos y voz.
- `scripts/enfasis.py`: frase de énfasis con serifa + cursiva de pincel, en imagen, sobre foto o animada (`.mov` con transparencia para encimar en el video).
- `fonts/`: Archivo Black, Instrument Serif Italic, Fraunces, Norican, Playball, DM Serif Display y Mr Dafoe (licencia SIL Open Font License, de Google Fonts).
- `inspiraciones.md`: ideas y referencias que Frida quiere llegar a hacer.

## Preparar una sesión nueva

```bash
pip install pillow gdown
```

Vosk necesita el paquete `srt`, que no compila en este entorno. Se instala a mano:

```bash
pip download --no-deps --no-binary :all: --no-build-isolation srt==3.5.3 -d /tmp/pkg && tar xzf /tmp/pkg/srt-3.5.3.tar.gz -C /tmp/pkg && cp /tmp/pkg/srt-3.5.3/srt.py "$(python3 -c 'import site;print(site.getsitepackages()[0])')/" && pip install --no-deps vosk cffi
```

Modelo de voz en español (requiere permitir `alphacephei.com` en la red del entorno):

```bash
curl -L -o /tmp/es.zip https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip && python3 -c "import zipfile;zipfile.ZipFile('/tmp/es.zip').extractall('/tmp')"
```

Descargar clips de Drive: listar con `gdown.download_folder(url, skip_download=True)` y bajar cada archivo desde `https://drive.usercontent.google.com/download?id=ID&export=download&confirm=t` (los hosts `doc-*.googleusercontent.com` están bloqueados).

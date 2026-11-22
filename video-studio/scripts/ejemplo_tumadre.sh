#!/bin/bash
# Final v3: frases pequeñas + palabra clave marcada con efecto visual y sonido (estilo referencia).
# Sonido solo en palabras marcadas y en transiciones.
set -e
S="${WORK:?Define WORK=carpeta de trabajo}"; VS="$(cd "$(dirname "$0")/.." && pwd)"
R=$S/raw
W=$S/salida
mkdir -p $W/sfx && cd $W
rm -rf seg*.mp4 g*.mp4 txt l.txt

TONE="eq=contrast=1.1:saturation=1.15:gamma=0.92"
enc="-c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30"
cut() { # out clip start dur zoom(z|-) pad_seconds
  vf="$TONE,scale=1080:1920"
  [ "$5" = "z" ] && vf="$TONE,scale=1210:2150,crop=1080:1920"
  [ -n "$6" ] && vf="$vf,tpad=stop_mode=clone:stop_duration=$6"
  ffmpeg -nostdin -v error -y -ss "$3" -t "$4" -i "$R/$2" -vf "$vf,fps=30,format=yuv420p" -an $enc "$1"
}
cut seg01.mp4 IMG_7376.MOV 78.0 1.6 -
cut seg02.mp4 IMG_7379.MOV 30.0 1.6 z
cut seg03.mp4 IMG_7377.MOV 25.0 1.6 -
cut seg04.mp4 IMG_7385.MOV 0.9 1.5 -
cut seg05.mp4 IMG_7388.MOV 2.0 1.4 -
cut seg06.mp4 IMG_7399.MOV 1.3 3.0 -
cut seg07.mp4 IMG_7406.MOV 0.0 2.5 -
cut seg07b.mp4 IMG_7406.MOV 4.0 3.0 -
cut seg08.mp4 IMG_7409.MOV 8.2 4.4 -
cut seg09.mp4 IMG_7414.MOV 2.0 2.2 -
cut seg10.mp4 IMG_7421.MOV 1.0 1.3 -
cut seg11.mp4 IMG_7422.MOV 8.0 1.3 z
cut seg12.mp4 IMG_7421.MOV 3.5 1.2 z
cut seg13.mp4 IMG_7422.MOV 18.0 1.3 -
cut seg14.mp4 IMG_7423.MOV 0.0 2.7 - 1.5

group() { out=$1; shift; : > l.txt; for s in "$@"; do echo "file '$s'" >> l.txt; done
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i l.txt -c copy "$out"; }
group g1.mp4 seg01.mp4 seg02.mp4 seg03.mp4
group g2.mp4 seg04.mp4 seg05.mp4
group g3.mp4 seg06.mp4
group g4.mp4 seg07.mp4 seg07b.mp4 seg08.mp4
group g5.mp4 seg09.mp4
group g6.mp4 seg10.mp4 seg11.mp4 seg12.mp4 seg13.mp4
group g7.mp4 seg14.mp4

ffmpeg -nostdin -v error -y -i g1.mp4 -i g2.mp4 -i g3.mp4 -i g4.mp4 -i g5.mp4 -i g6.mp4 -i g7.mp4 -filter_complex \
"[0][1]xfade=transition=smoothleft:duration=0.3:offset=4.5[a];\
[a][2]xfade=transition=zoomin:duration=0.3:offset=7.1[b];\
[b][3]xfade=transition=smoothup:duration=0.3:offset=9.8[c];\
[c][4]xfade=transition=zoomin:duration=0.3:offset=19.4[d];\
[d][5]xfade=transition=smoothleft:duration=0.3:offset=21.3[e];\
[e][6]xfade=transition=fadewhite:duration=0.3:offset=26.1,format=yuv420p[v]" \
-map "[v]" $enc base.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 base.mp4)

cat > spec.json <<EOF
{"fonts": {"base": "$VS/fonts/ArchivoBlack.ttf", "serif": "$VS/fonts/InstrumentSerifItalic.ttf"},
 "duration": $DUR, "blocks": [
 {"start": 0.05, "end": 1.6, "size": 46, "lines": [[["base","DESPUÉS DE UN"]], [["serif","día largo…",0.35]]]},
 {"start": 1.6, "end": 4.45, "size": 42, "lines": [[["base","…A VECES SOLO QUIERO COMER ALGO"]], [["serif","saludable,",0.4]], [["base","PERO QUE DE VERDAD",0.9]], [["bold","ME NUTRA",1.4]]]},
 {"start": 4.8, "end": 7.05, "size": 46, "lines": [[["base","ME QUEDABA DE PASO"]], [["serif","Productos Tu Madre",0.35]]]},
 {"start": 7.4, "end": 9.75, "size": 42, "lines": [[["base","Y PASÉ POR MI ALMUERZO ANTES DE MI"]], [["bold","ÚLTIMA CLASE",0.5]], [["base","DEL DÍA",0.5]]]},
 {"start": 10.25, "end": 12.3, "size": 38, "y": 1240, "lines": [[["base","YO ME PEDÍ EL"]], [["bold","SIVAR BOWL",0.95]]]},
 {"start": 12.35, "end": 15.3, "size": 36, "y": 1240, "lines": [[["base","Y YA LE PUSE UN POQUITO DE ADEREZO,"]], [["base","ASÍ QUE VAMOS A",1.9]], [["serif","probarlo",2.3]]]},
 {"start": 19.7, "end": 21.25, "size": 46, "lines": [[["base","Y PARA ACOMPAÑAR,"]], [["serif","mi shake",0.35]]]},
 {"start": 21.6, "end": 26.05, "size": 46, "lines": [[["base","LISTA PARA MI"]], [["bold","ÚLTIMA CLASE",0.45]]]},
 {"start": 26.4, "end": 99, "size": 42, "lines": [[["base","SI PASAS POR TU MADRE, PIDE EL"]], [["serif","Sivar Bowl",0.45]], [["base","Y DESPUÉS ME CUENTAS",1.2]]]}
]}
EOF
python3 -I $VS/scripts/textos.py spec.json txt events.txt

# Sonidos: pop para palabras en negrita, brillo para palabras en cursiva, whoosh en transiciones
ffmpeg -nostdin -v error -y -f lavfi -i "anoisesrc=color=pink:duration=0.5:amplitude=0.9" \
  -af "highpass=f=400,lowpass=f=5000,afade=t=in:d=0.28:curve=exp,afade=t=out:st=0.28:d=0.22,volume=0.45" -ac 2 sfx/whoosh.wav
ffmpeg -nostdin -v error -y -f lavfi -i "aevalsrc='0.55*sin(2*PI*t*(450+3200*exp(-t*40)))*exp(-t*18)':d=0.25:s=44100" -ac 2 sfx/bold.wav
ffmpeg -nostdin -v error -y -f lavfi -i "aevalsrc='0.16*(sin(2*PI*1318*t)+0.7*sin(2*PI*1975*t)+0.5*sin(2*PI*2637*t))*exp(-t*6)*min(1,t*60)':d=0.7:s=44100" -ac 2 sfx/serif.wav

ffmpeg -nostdin -v error -y -ss 0.0 -i $R/IMG_7406.MOV -t 2.5 -vn -ac 2 -ar 44100 v1.wav
ffmpeg -nostdin -v error -y -ss 4.0 -i $R/IMG_7406.MOV -t 3.0 -vn -ac 2 -ar 44100 v2.wav
ffmpeg -nostdin -v error -y -ss 8.2 -i $R/IMG_7409.MOV -t 4.4 -vn -ac 2 -ar 44100 v3.wav
ffmpeg -nostdin -v error -y -i v1.wav -i v2.wav -i v3.wav -filter_complex "[0][1][2]concat=n=3:v=0:a=1,loudnorm=I=-16:TP=-1.5[a]" -map "[a]" -ar 44100 voice.wav

for t in 4.35 6.95 9.65 19.25 21.15 25.95; do echo "whoosh $t" >> events.txt; done
inputs="-i voice.wav"; filters="[1]adelay=9800|9800[s1];"; n=1
while read -r name t; do
  n=$((n+1)); d=$(python3 -c "print(int($t*1000))")
  inputs="$inputs -i sfx/$name.wav"; filters="$filters[$n]adelay=$d|$d[s$n];"
done < events.txt
mix=""; for i in $(seq 1 $n); do mix="$mix[s$i]"; done
ffmpeg -nostdin -v error -y -f lavfi -t $DUR -i anullsrc=r=44100:cl=stereo $inputs -filter_complex \
  "${filters}[0]${mix}amix=inputs=$((n+1)):normalize=0:duration=first,alimiter=limit=0.9[a]" -map "[a]" sfx/track.wav
echo "sonidos: $(wc -l < events.txt)"

ffmpeg -nostdin -v error -y -i base.mp4 -framerate 30 -i txt/t%04d.png -i sfx/track.wav -filter_complex \
  "[0][1]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map 2:a $enc -c:a aac -b:a 192k -shortest \
  -movflags +faststart frida_tumadre_final_v3.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 frida_tumadre_final_v3.mp4

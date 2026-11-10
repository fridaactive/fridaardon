#!/bin/bash
# Reel "Cardio vs pesas" (martes 10). Cortes, transiciones xfade, voz limpia, textos y sonidos elegidos por Frida.
set -e
S=/tmp/claude-0/-home-user-fridaardon/594e97b7-6785-521b-a31a-141cacec037b/scratchpad/cardio
VS=/home/user/fridaardon/video-studio
SFX=$S/../portal/sfx2
R=$S/raw; W=$S/out; cd $W
TONE="eq=contrast=1.1:saturation=1.15:gamma=0.92"
enc="-c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30"
# cut out clip start dur zoom audio(a|-)
cut() {
  vf="$TONE,scale=1080:1920"
  [ "$5" = "z" ] && vf="$TONE,scale=1188:2112,crop=1080:1920"
  if [ "$6" = "a" ]; then
    ffmpeg -nostdin -v error -y -ss "$3" -t "$4" -i "$R/$2" -vf "$vf,fps=30,format=yuv420p" -af "highpass=f=90,afade=t=in:d=0.04,afade=t=out:st=$(echo "$4-0.05"|bc):d=0.05" -ar 44100 -ac 2 $enc -c:a pcm_s16le "$1.mov"
  else
    ffmpeg -nostdin -v error -y -ss "$3" -t "$4" -i "$R/$2" -f lavfi -t "$4" -i anullsrc=r=44100:cl=stereo -vf "$vf,fps=30,format=yuv420p" -map 0:v -map 1:a $enc -c:a pcm_s16le "$1.mov"
  fi
}
cut s01 IMG_7497.MOV 0.0 1.7 - -
cut s02 IMG_7510.MOV 3.9 1.9 - -
cut s03 IMG_7500.MOV 2.80 4.35 - a
cut s04 IMG_7505.MOV 2.35 4.55 - a
cut s05 IMG_7505.MOV 8.28 1.75 z a
cut s06 IMG_7536.MOV 2.0 2.2 - -
cut s07 IMG_7537.MOV 11.0 2.6 - -
cut s08 IMG_7538.MOV 44.0 2.4 - -
cut s09 IMG_7553.MOV 5.20 8.05 - a
cut s10 IMG_7540.MOV 4.6 3.6 - -
# grupos sin transición (corte directo dentro del grupo)
grp() { o=$1; shift; : > l.txt; for s in "$@"; do echo "file '$W/$s.mov'" >> l.txt; done; ffmpeg -nostdin -v error -y -f concat -safe 0 -i l.txt -c copy $o.mov; }
grp g1 s01 s02
grp g2 s03
grp g3 s04 s05
grp g4 s06 s07 s08
grp g5 s09
grp g6 s10
d() { ffprobe -v error -show_entries format=duration -of csv=p=0 $1.mov; }
X=0.3
o1=$(echo "$(d g1)-$X"|bc); o2=$(echo "$o1+$(d g2)-$X"|bc); o3=$(echo "$o2+$(d g3)-$X"|bc); o4=$(echo "$o3+$(d g4)-$X"|bc); o5=$(echo "$o4+$(d g5)-$X"|bc)
echo "transiciones en: $o1 $o2 $o3 $o4 $o5" | tee trans.txt
ffmpeg -nostdin -v error -y -i g1.mov -i g2.mov -i g3.mov -i g4.mov -i g5.mov -i g6.mov -filter_complex \
"[0:v][1:v]xfade=transition=zoomin:duration=$X:offset=$o1[a];[a][2:v]xfade=transition=slideleft:duration=$X:offset=$o2[b];[b][3:v]xfade=transition=zoomin:duration=$X:offset=$o3[c];[c][4:v]xfade=transition=slideup:duration=$X:offset=$o4[e];[e][5:v]xfade=transition=fade:duration=$X:offset=$o5,format=yuv420p[v];\
[0:a][1:a]acrossfade=d=$X[aa];[aa][2:a]acrossfade=d=$X[ab];[ab][3:a]acrossfade=d=$X[ac];[ac][4:a]acrossfade=d=$X[ad];[ad][5:a]acrossfade=d=$X,loudnorm=I=-16:TP=-1.5[a]" \
-map "[v]" -map "[a]" $enc -c:a pcm_s16le -ar 44100 base.mov
ffprobe -v error -show_entries format=duration -of csv=p=0 base.mov

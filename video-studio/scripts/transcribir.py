"""Transcribe un audio/video en español con tiempos por palabra (Vosk). Imprime JSON."""
import json
import os
import subprocess
import sys
import wave

from vosk import KaldiRecognizer, Model, SetLogLevel

SetLogLevel(-1)
MODEL = os.environ.get("VOSK_MODEL", "/tmp/vosk-model-small-es-0.42")
src, wav = sys.argv[1], sys.argv[2]
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", "-vn", wav], check=True)

wf = wave.open(wav, "rb")
rec = KaldiRecognizer(Model(MODEL), wf.getframerate())
rec.SetWords(True)
words = []
while True:
    data = wf.readframes(4000)
    if not data:
        break
    if rec.AcceptWaveform(data):
        words += json.loads(rec.Result()).get("result", [])
words += json.loads(rec.FinalResult()).get("result", [])
print(json.dumps([{"w": w["word"], "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in words], ensure_ascii=False))

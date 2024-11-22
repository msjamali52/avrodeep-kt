import vosk
import audioop
import base64
import json
import os

model = vosk.Model('model')

CL = '\x1b[0K'
BS = '\x08'

class AudioFunctions:
    def transcribe(self,packet):
        rec = vosk.KaldiRecognizer(model, 16000)
        audio = base64.b64decode(packet['media']['payload'])
        audio = audioop.ulaw2lin(audio, 2)
        audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
        result = ''
        if rec.AcceptWaveform(audio):
            r = json.loads(rec.Result())
            result = r['text']
            print(CL + r['text'] + ' ', end='', flush=True)
        else:
            r = json.loads(rec.PartialResult())
            result = r['partial']
            print(CL + r['partial'] + BS * len(r['partial']), end='', flush=True)
        
        return result
    
    def text2speech(self, text):
        return "Audio"
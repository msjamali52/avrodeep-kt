import audioop
import base64
import json
import os
from fastapi import APIRouter, FastAPI, Request, WebSocket, WebSocketDisconnect
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Start

from app.modules.audio.engine import AudioFunctions
from app.modules.ai.engine import AIFunctions

ACCOUNT_SID = os.getenv('TWILIO_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH')

app = FastAPI()
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

router = APIRouter(
    prefix="/ws",
    tags=["Web Socket"],
    responses={404: {"description": "Not found"}},
)

CL = '\x1b[0K'
BS = '\x08'

@app.post('/call')
async def call(request: Request):
    """Accept a phone call."""
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    return str(response), 200, {'Content-Type': 'text/xml'}


@app.websocket('/stream')
async def websocket_endpoint(ws: WebSocket):
    """Receive and transcribe audio stream."""
    try:
        while True:
            message = ws.receive()
            packet = json.loads(message)
            if packet['event'] == 'start':
                print('Streaming is starting')
            elif packet['event'] == 'stop':
                print('\nStreaming has stopped')
            elif packet['event'] == 'media':
                transcribed_text = AudioFunctions().transcribe(packet=packet)
                processed_reply = AIFunctions().generate(input=transcribed_text)
                audio_reply = AudioFunctions().text2speech(text=processed_reply)

                media_message = {
                    "event": "media",
                    "media": {
                        "payload": audio_reply
                    }
                }
                ws.send(json.dumps(media_message))

    except:
        pass





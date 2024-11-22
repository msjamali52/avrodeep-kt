from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
from app.modules.ai.answer import query

app = FastAPI()
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = query(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")

app.include_router(router)


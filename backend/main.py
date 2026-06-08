from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, kaydet, son_olcum, gecmis
from models import SensorVeri, Olcum, Basarili

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

db = init_db()
websocketler: list[WebSocket] = []

# Bridge buraya POST atar
@app.post("/api/veri", response_model=Basarili)
async def veri_al(veri: SensorVeri):
    kaydet(db, veri.model_dump())
    # Bağlı tüm frontend'lere anlık ilet
    kopanlar = []
    for ws in websocketler:
        try:
            await ws.send_json(veri.model_dump())
        except:
            kopanlar.append(ws)
    for ws in kopanlar:
        websocketler.remove(ws)
    return {"success": True}

# Frontend: son ölçüm (sayfa ilk açıldığında)
@app.get("/api/son-olcum", response_model=Olcum | None)
def get_son_olcum():
    olcum = son_olcum(db)
    if not olcum:
        return None
    return olcum

# Frontend: grafik için geçmiş
@app.get("/api/gecmis", response_model=list[Olcum])
def get_gecmis(limit: int = 200):
    return gecmis(db, limit)

# Frontend: gerçek zamanlı bağlantı
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocketler.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # bağlantıyı canlı tut
    except WebSocketDisconnect:
        websocketler.remove(websocket)
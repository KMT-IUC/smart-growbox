from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, kaydet, son_olcum, gecmis

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

db = init_db()
websocketler: list[WebSocket] = []

# Bridge buraya POST atar
@app.post("/api/veri")
async def veri_al(veri: dict):
    kaydet(db, veri)
    # Bağlı tüm frontend'lere anlık ilet
    kopanlar = []
    for ws in websocketler:
        try:
            await ws.send_json(veri)
        except:
            kopanlar.append(ws)
    for ws in kopanlar:
        websocketler.remove(ws)
    return {"ok": True}

# Frontend: son ölçüm (sayfa ilk açıldığında)
@app.get("/api/son-olcum")
def get_son_olcum():
    return son_olcum(db)

# Frontend: grafik için geçmiş
@app.get("/api/gecmis")
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
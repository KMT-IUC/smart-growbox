# Smart Growbox

Bu proje, bir akıllı bitki yetiştirme kabininin backend ve köprü (bridge) yazılımlarını içerir.

## Kurulum

Projeyi yerel makinenizde çalıştırmadan önce gerekli kütüphaneleri yüklemeniz gerekmektedir.

### Backend Kurulumu

`backend` klasörüne gidin ve `requirements.txt` dosyasındaki paketleri yükleyin:

```bash
cd backend
pip install -r requirements.txt
```

### Bridge Kurulumu

`bridge` klasörüne gidin ve `requirements.txt` dosyasındaki paketleri yükleyin:

```bash
cd bridge
pip install -r requirements.txt
```

## Çalıştırma

### Backend Sunucusu

Backend sunucusunu (FastAPI) başlatmak için `backend` klasöründeyken aşağıdaki komutu çalıştırın:

```bash
uvicorn main:app --reload
```

Sunucu `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

#### Ağ Üzerinden Erişim (İsteğe Bağlı)

Eğer başka bir bilgisayarın (örneğin, EE'nin PC'si) backend sunucusuna erişmesi gerekiyorsa, sunucuyu `0.0.0.0` host adresi ile başlatmalısınız.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Bu durumda, Mac'inizin yerel ağdaki IP adresini bulmanız gerekir:

```bash
# WiFi için
ipconfig getifaddr en0

# Ethernet kablosu için
ipconfig getifaddr en1
```

### Bridge Yazılımı

Bridge yazılımı, STM32'den gelen verileri okuyup backend'e gönderir. `bridge` klasöründeyken aşağıdaki komutu çalıştırın:

```bash
python bridge.py
```

## Mimari

```
STM32
│ (USB CDC JSON)
▼
EE'nin Windows PC'si → bridge.py → POST /api/veri
                                     │
                                     ▼
Backend Sunucusu (Senin Mac'in) ← kaydet(db) & ws.send_json()
                                     │
                                     ▼
Frontend (Tarayıcı)
```

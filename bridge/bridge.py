import serial, json, requests, time

# EE'nin PC'sinde çalışır, başka bir şey yapmaz

PORT = "COM3"          # Device Manager'dan bakılacak
BAUD = 115200
BACKEND = "http://192.168.1.45:8000/api/veri"  # Mac'in lokal IP'si
# ipconfig getifaddr en0   # WiFi ise


ser = serial.Serial(PORT, BAUD, timeout=2)
print("Bridge başladı...")

while True:
    try:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            continue
        veri = json.loads(line)
        print(veri)
        requests.post(BACKEND, json=veri, timeout=3)

    except json.JSONDecodeError:
        print(f"Bozuk frame, atlandı: {line}")
    except requests.ConnectionError:
        print("Backend'e ulaşılamıyor, 3sn bekleniyor...")
        time.sleep(3)
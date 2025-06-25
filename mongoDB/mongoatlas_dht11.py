import serial
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import pytz
import json

# Zona horaria
timezone = pytz.timezone('America/Bogota')

# 🔌 Puerto serial COM4 (ajusta si es necesario)
puerto_serial = serial.Serial('COM8', 9600, timeout=1)
print("🟢 Esperando datos desde el Arduino (COM8)...")

# 🛡️ MongoDB Atlas URI
usuario = quote_plus("omarpk148")
clave = quote_plus("Solopk148")
cluster = "cluster0.i7yfuyi.mongodb.net"
base_datos = "sensordht11"

uri = f"mongodb+srv://{usuario}:{clave}@{cluster}/?retryWrites=true&w=majority&tls=true"

# Conexión MongoDB
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client[base_datos]
coleccion = db["datos"]

try:
    client.server_info()
    print("✅ Conexión establecida con MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar con MongoDB:", e)
    exit()

# 📥 Leer e insertar en bucle
while True:
    try:
        linea = puerto_serial.readline().decode('utf-8').strip()
        if linea:
            data = json.loads(linea)
            temperatura = float(data['temperatura'])
            humedad = float(data['humedad'])

            dato = {
                "sensor": "DHT11",
                "temperatura": temperatura,
                "humedad": humedad,
                "fecha_hora": datetime.now(timezone),
                "ubicacion": "Taller"
            }

            coleccion.insert_one(dato)
            print(f"📤 Subido -> Temp: {temperatura} °C | Humedad: {humedad} %")

    except Exception as error:
        print("⚠️ Error:", error)

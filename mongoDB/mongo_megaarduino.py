# pip install pyserial pymongo pytz

import serial
import time
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import pytz

# Zona horaria
timezone = pytz.timezone('America/Bogota')

# Puerto del Arduino Mega
puerto_arduino = "/dev/cu.usbmodem112401"
baud_rate = 9600

# Conexión a MongoDB Atlas
usuario = quote_plus("lauraarteaga1005")
clave = quote_plus("5quqO6Fq36krMM7l")
cluster = "cluster0.ifst0oe.mongodb.net"
base_datos = "mi_base"
uri = f"mongodb+srv://{usuario}:{clave}@{cluster}/{base_datos}?retryWrites=true&w=majority"

# Conectar a MongoDB
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[base_datos]
    coleccion = db["mi_coleccion"]
    print("✅ Conectado a MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar con MongoDB Atlas:", e)
    exit()

# Conectar al Arduino
try:
    arduino = serial.Serial(puerto_arduino, baud_rate, timeout=1)
    time.sleep(2)
    print(f"✅ Conectado al Arduino Mega en {puerto_arduino}")
except Exception as e:
    print("❌ Error al conectar con el puerto serial:", e)
    exit()

# Lectura e inserción
print("🟢 Iniciando lectura del DHT11...")
while True:
    try:
        linea = arduino.readline().decode(errors='ignore').strip()

        if "," in linea:
            try:
                t_str, h_str = linea.split(",")
                t = float(t_str)
                h = float(h_str)

                doc = {
                    "sensor": "DHT11",
                    "temperatura": t,
                    "humedad": h,
                    "timestamp": datetime.now(timezone)
                }

                resultado = coleccion.insert_one(doc)
                print(f"📤 Insertado en MongoDB con _id: {resultado.inserted_id}")
            except ValueError:
                print("⚠️ Formato no numérico:", linea)
        elif linea != "":
            print("⚠️ Lectura ignorada:", linea)

    except KeyboardInterrupt:
        print("⛔ Lectura finalizada por el usuario.")
        break
    except Exception as e:
        print("❌ Error en la lectura/envío:", e)

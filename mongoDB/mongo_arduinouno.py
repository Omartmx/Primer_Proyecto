# pip install pyserial pymongo pytz

import serial
import time
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import pytz

# Zona horaria de Colombia
timezone = pytz.timezone('America/Bogota')

# Puerto serial del Arduino (ajusta si cambia)

puerto_arduino = "COM8" 
baud_rate = 9600

# Credenciales y URI de MongoDB Atlas
usuario = quote_plus("omarpk148")
clave = quote_plus("Solopk148")
cluster = "cluster0.i7yfuyi.mongodb.net"
base_datos = "sensordht11"

uri = f"mongodb+srv://{usuario}:{clave}@{cluster}/?retryWrites=true&w=majority&tls=true"

# Conexión a MongoDB Atlas
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[base_datos]
    coleccion = db["datos"]
    print("✅ Conectado a MongoDB Atlas")
except Exception as e:
    print("❌ Error al conectar con MongoDB Atlas:", e)
    exit()



# Conexión con Arduino
try:
    arduino = serial.Serial(puerto_arduino, baud_rate, timeout=1)
    time.sleep(2)  # Esperar estabilización
    print(f"✅ Conectado al Arduino en {puerto_arduino}")
except Exception as e:
    print("❌ Error al conectar con el puerto serial:", e)
    exit()

# Inicia la lectura continua
print("🟢 Iniciando lectura del DHT11...")

while True:
    try:
        linea = arduino.readline().decode(errors='ignore').strip()

        if "," in linea:
            # Formato esperado: 24.90,40.00
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
                print("⚠️ Error al convertir datos:", linea)

        elif linea != "":
            print("⚠️ Lectura ignorada:", linea)

    except KeyboardInterrupt:
        print("⛔ Lectura finalizada por el usuario.")
        break
    except Exception as e:
        print("❌ Error en la lectura/envío:", e)

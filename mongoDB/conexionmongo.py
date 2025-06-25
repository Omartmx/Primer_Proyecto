
from pymongo import MongoClient
from urllib.parse import quote_plus


usuario = quote_plus("omarpk148")
clave = quote_plus("Solopk148")
cluster = "cluster0.i7yfuyi.mongodb.net"

uri = f"mongodb+srv://{usuario}:{clave}@{cluster}/?retryWrites=true&w=majority&tls=true"

client = MongoClient(uri)
db = client["mi_base"]
coleccion = db["temperatura"]

"""""

# Insertar un documento de prueba
coleccion.insert_many ([ 

    {"sensor": "DHT11", "tipo": "temperatura", "valor": 30, "unidad": "°C" },
    {"sensor": "DHT11", "tipo": "temperatura", "valor": 49, "unidad": "°C" },
    {"sensor": "DHT11", "tipo": "temperatura", "valor": 35, "unidad": "°C" }

])

#2.	Consulta todas las lecturas con valor mayor a 40 °C.

for lectura in coleccion.find({ "valor": { "$gt": 40 } }):
    print(lectura)

#3.	Actualiza cualquier registro con valor 49 °C para que quede en 48 °C. 

coleccion.update_one({ "valor": 49 },{ "$set": { "valor": 48 } }
)

#4.	Elimina las lecturas inferiores a 32 °C.

coleccion.delete_many({ "valor": { "$lt": 32 } })




coleccion.insert_many ([ 

    { "sensor": "DHT11", "tipo": "humedad", "valor": 50, "unidad": "%" },
    { "sensor": "DHT11", "tipo": "humedad", "valor": 100, "unidad": "%" },
    { "sensor": "DHT11", "tipo": "humedad", "valor": 70, "unidad": "%" }
    ])

#2.	Consulta las lecturas con valor mayor o igual a 70 %.
for lectura in coleccion.find({"valor":{"$gte":70}}):
    print(lectura)

#3.	Agrega el campo estado: "alto" a las lecturas de 100 % de humedad.

coleccion.update_many({ "tipo": "humedad", "valor": 100 },{ "$set": { "estado": "alto" } })


#4.	Cuenta cuántas lecturas presentan humedad menor a 60 %.

for lectura in coleccion.find({"valor":{"$lt":60}}):
    print(lectura)




#1.	Inserta dos registros: (30 m, 40 m) y (60 m, 50 m).

coleccion.insert_many ([ 
    { "vehiculo": "drone", "distancia": 30, "altura": 40, "unidad": "metros" },
    { "vehiculo": "drone", "distancia": 60, "altura": 50, "unidad": "metros" },
     ])

#2.	Consulta los recorridos donde la altura supere los 45 m.

for lectura in coleccion.find({"altura":{"$gt":45}}):
    print(lectura)

#3.	Ordena los resultados por distancia descendente.

for lectura in coleccion.find().sort("distancia", -1):  
    print(lectura)


#4.	Elimina cualquier registro cuya distancia sea menor a 35 m.

coleccion.delete_many({"distancia":{"$lt":35}})


""""""""

coleccion.insert_many ([
    { "pixel_x": 100, "pixel_y": 200, "valor": 128, "unidad": "nivel gris" },
    { "pixel_x": 110, "pixel_y": 210, "valor": 200, "unidad": "nivel gris" },

    ])


# 2. Consulta valores de nivel de gris superiores a 150

for lectura in coleccion.find({ "valor": { "$gt": 150 } }):
    print(lectura)

# 3. Agrega campo clasificacion: "brillante" a los píxeles > 180

coleccion.update_many({ "valor": { "$gt": 180 } }, { "$set": { "clasificacion": "brillante" } })
    

# 4. Muestra pixel_x, pixel_y y valor sin _id

for lectura in coleccion.find({}, { "pixel_x": 1, "pixel_y": 1, "valor": 1, "_id": 0 }):
    print(lectura)


""""""

coleccion.insert_many ([

    { "tipo": "produccion", "valor": 45 },
    { "tipo": "produccion", "valor": 70 },
    { "tipo": "produccion", "valor": 55 },
    ])


# 2. Calcula promedio, max y min
for lectura in coleccion.aggregate([{ "$group": {"_id": "$tipo","promedio": { "$avg": "$valor" },"maximo": { "$max": "$valor" },"minimo": 
                                                 { "$min": "$valor" }
    }}
]):
    print(lectura)

# 3. Actualiza valor 45 a 48
coleccion.update_one({ "valor": 45 }, { "$set": { "valor": 48 } })
   

# 4. Borra registros con valor menor a 50
coleccion.delete_many({ "valor": { "$lt": 50 } })




coleccion.insert_many ([
    { "vehiculo": "robot", "velocidad": 12.5, "unidad": "km/h" },
    { "vehiculo": "robot", "velocidad": 18.2, "unidad": "km/h" }
    ])

# 2. Consulta velocidades > 15
for lectura in coleccion.find({ "velocidad": { "$gt": 15 } }):
    print(lectura)

# 3. Añade campo riesgo: true si velocidad > 17
coleccion.update_many({ "velocidad": { "$gt": 17 } }, { "$set": { "riesgo": True } })

# 4. Limita salida a 1 documento, ordenado por velocidad desc
for lectura in coleccion.find().sort("velocidad", -1).limit(1):
    print(lectura)


    


coleccion.insert_many ([
    { "sensor": "MQ135", "valor": 450, "unidad": "ppm" },
    { "sensor": "MQ135", "valor": 620, "unidad": "ppm" },
    ])

# 2. Consulta entre 400 y 600 ppm
for lectura in coleccion.find({ "valor": { "$gte": 400, "$lte": 600 } }):
    print(lectura)

# 3. Actualiza unidad a "ppm_CO2"
coleccion.update_many({}, { "$set": { "unidad": "ppm_CO2" } })

# 4. Cuenta lecturas fuera de 400-600
coleccion.count_documents({ "$or": [ { "valor": { "$lt": 400 } }, { "valor": { "$gt": 600 } } ] })


"""""""

coleccion.insert_many ([
    { "sensor": "LDR", "valor": 300, "unidad": "lux" },
    { "sensor": "LDR", "valor": 800, "unidad": "lux" },
    ])

# 2. Consulta lecturas con valor > 500 lux
for lectura in coleccion.find({ "valor": { "$gt": 500 } }):
    print(lectura)

# 3. Duplica la lectura de 800 lux con fuente: "prueba"
original = coleccion.find_one({ "valor": 800 })
if original:
    original["fuente"] = "prueba"
    del original["_id"]
    coleccion.insert_one(original)

# 4. Elimina las lecturas de 300 lux
coleccion.delete_many({ "valor": 300 })



""""""

coleccion.insert_many ([
    { "dispositivo": "aire acondicionado", "consumo": 1200, "unidad": "W" },
    { "dispositivo": "computadora", "consumo": 300, "unidad": "W" },
    ])

# 2. Consulta orden ascendente por consumo
for lectura in coleccion.find().sort("consumo", 1):
    print(lectura)

# 3. Cambia consumo de computadora a 280 W
coleccion.update_one({ "dispositivo": "computadora" }, { "$set": { "consumo": 280 } })

# 4. Elimina aire acondicionado
coleccion.delete_one({ "dispositivo": "aire acondicionado" })


""

coleccion.insert_many ([
    { "sensor": "pH", "valor": 6.5, "unidad": "pH" },
    { "sensor": "pH", "valor": 7.1, "unidad": "pH" },
    ])

# 2. Registros con pH entre 6.5 y 7.0 inclusive
coleccion.find({ "valor": { "$gte": 6.5, "$lte": 7.0 } })

# 3. Añade categoria: "ligeramente_acido" a pH < 7
coleccion.update_many({ "valor": { "$lt": 7 } }, { "$set": { "categoria": "ligeramente_acido" } })

# 4. Cuántos registros son neutros (7 ≤ pH < 7.5)
coleccion.count_documents({ "valor": { "$gte": 7, "$lt": 7.5 } })
    


"""""""

coleccion.insert_many ([
    { "sensor": "DHT22", "valor": 22.5, "unidad": "°C", "nivel": "suelo" },
    ])

# 2. Confirma unidad "°C", si no actualiza
coleccion.update_many({ "unidad": { "$ne": "°C" } }, { "$set": { "unidad": "°C" } })

# 3. Agrega zona: "invernadero"
coleccion.update_many({}, { "$set": { "zona": "invernadero" } })

# 4. Elimina si temperatura < 15 °C
coleccion.delete_many({ "valor": { "$lt": 15 } })


""

coleccion.insert_many ([

    { "usuario": "Laura", "pasos": 3500 },
    { "usuario": "Pedro", "pasos": 7800 }
    ])

# 2. Ordenar por pasos descendente
for lectura in coleccion.find().sort("pasos", -1):
    print(lectura)

# 3. Aumenta 500 pasos a Laura
coleccion.update_one({ "usuario": "Laura" }, { "$inc": { "pasos": 500 } })

# 4. Mostrar usuario con más pasos
for lectuira in coleccion.find().sort("pasos", -1).limit(1):
    print(lectura)


""

coleccion.insert_many ([
    { "sensor": "BMP180", "presion": 1013.25, "unidad": "hPa" },
    ])

# 2. Verifica existencia del campo presion
coleccion.find_one({ "presion": { "$exists": True } })
    

# 3. Añade ubicacion: "Bogota"
coleccion.update_many({}, { "$set": { "ubicacion": "Bogota" } })

# 4. Elimina si presión > 1050
coleccion.delete_many({ "presion": { "$gt": 1050 } })

"""""""

coleccion.insert_many ([
    { "sensor": "ultrasonico", "nivel": 75, "unidad": "%" },
    ])

# 2. Consulta si nivel ≥ 75 %
for lectura in coleccion.find({ "nivel": { "$gte": 75 } }):
    print(lectura)

# 3. Actualiza estado a “lleno” si nivel ≥ 90 %
coleccion.update_many({ "nivel": { "$gte": 90 } }, { "$set": { "estado": "lleno" } })

# 4. Cuenta registros con nivel < 25 %
coleccion.count_documents({ "nivel": { "$lt": 25 } })
   


""

coleccion.insert_many ([
    { "sensor": "pulso", "bpm": 72 },
    { "sensor": "pulso", "bpm": 88 }
    ])

# 2. Consulta registros con bpm > 80
for lectura in coleccion.find({ "bpm": { "$gt": 80 } }):
    print (lectura)

# 3. Añade alerta: true a bpm > 100
coleccion.update_many({ "bpm": { "$gt": 100 } }, { "$set": { "alerta": True } })

# 4. Elimina bpm < 60
coleccion.delete_many({ "bpm": { "$lt": 60 } })

""


coleccion.insert_many ([
    { "sensor": "termistor", "valor": 37.8, "unidad": "°C" },
    ])

# 2. Consulta si temperatura > 37.5 °C
for lectura in coleccion.find({ "valor": { "$gt": 37.5 } }):
    print(lectura)

# 3. Añade estado: "fiebre"
coleccion.update_many({ "valor": { "$gt": 37.5 } }, { "$set": { "estado": "fiebre" } })

# 4. Elimina si valor ≤ 36
coleccion.delete_many({ "valor": { "$lte": 36 } })



"""""""

coleccion.insert_many ([
    { "sensor": "acelerometro", "eje_x": 0.3, "eje_y": 0.1, "eje_z": 9.8 },
    ])

# 2. Consulta eje_z > 9.5
for lectura in coleccion.find({ "eje_z": { "$gt": 9.5 } }):
    print(lectura)

# 3. Agrega caida: false
coleccion.update_many({ "eje_z": { "$gt": 9.5 } }, { "$set": { "caida": False } })

# 4. Elimina documentos con eje_z < 1.0
coleccion.delete_many({ "eje_z": { "$lt": 1.0 } })


""

coleccion.insert_many ([
    { "sensor": "microfono", "nivel": 65, "unidad": "dB" },
    ])

# 2. Consulta si nivel > 60 dB
for lectura in coleccion.find({ "nivel": { "$gt": 60 } }):
    print(lectura)

# 3. Clasificación: "alto" si nivel ≥ 70
coleccion.update_many({ "nivel": { "$gte": 70 } }, { "$set": { "clasificacion": "alto" } })

# 4. Media de niveles de ruido
for lectura in coleccion.aggregate([{ "$group": { "_id": None, "promedio": { "$avg": "$nivel" } } }]):
    print(lectura)

""

coleccion.insert_many ([
    { "cpu": "core 1", "uso": 75, "unidad": "%" },
    { "cpu": "core 2", "uso": 83, "unidad": "%" }
    ])

# 2. Núcleo con mayor uso
for lectura in coleccion.find().sort("uso", -1).limit(1):
    print(lectura)

# 3. Reduce uso de core 2 en 5 %
coleccion.update_one({ "cpu": "core 2" }, { "$inc": { "uso": -5 } })

# 4. Elimina donde uso > 95 %
coleccion.delete_many({ "uso": { "$gt": 95 } })


"""""


coleccion.insert_many ([
    { "sensor": "camara", "objetos_detectados": 3 }
    ])

# 2. Actualiza a 6 si se detectan más objetos
coleccion.update_one({ "objetos_detectados": { "$lt": 6 } }, { "$set": { "objetos_detectados": 6 } })

# 3. Añade alerta: "exceso" si objetos_detectados ≥ 5
coleccion.update_many({ "objetos_detectados": { "$gte": 5 } }, { "$set": { "alerta": "exceso" } })

# 4. Elimina si objetos_detectados = 0
coleccion.delete_many({ "objetos_detectados": 0 })


print("✅ Insertado correctamente")
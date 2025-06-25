from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import math

                                # Parcial Omar peña y ivan camilo garcia

#¿Cuál sentencia imprime 'Aprobado' si la nota es mayor o igual a 3.0?


nota = 4.5

if nota >= 3.0:
    print('Aprobado')  


#Un sensor mide la temperatura. Si es mayor a 30 se imprime 'Alerta de calor', si no, 'Temperatura normal'.


temp = 32
print('Alerta de calor' if temp > 30 else 'Temperatura normal')  




a = 1
b = 6
c = -2
discriminante = b**2 - 4*a*c

if discriminante < 0:
    resultado = complex(-b, math.sqrt(-discriminante)) / (2*a)
    resultado += 4  
    print("Raíces imaginarias. Resultado ajustado:", resultado)



#¿Cuál sentencia imprime los números del 1 al 5?


for i in range(1, 6):
    print(i)  



#¿Qué ciclo for recorre las raíces y multiplica por 365 si son enteras?


raices = [1.0, -2.0]  # ejemplo de raíces

for r in raices:
    if r.is_integer():
        print(r * 365)  




#¿Cuál es la sintaxis correcta para insertar un dato con sensor DHT11, temperatura, humedad y timestamp?




coleccion.insert_one({
    'sensor': 'dht11',
    'temperatura': temperatura,
    'humedad': humedad,
    'tiempo': datetime.now()
}) 


#¿Cuál sería una consulta correcta para encontrar temperaturas entre 30 °C y 50 °C?


coleccion.find({'temperatura': {'$gte': 30, '$lte': 50}})  



#¿Cuál comando permite encontrar el último dato insertado en una colección?


coleccion.find().sort('_id', -1).limit(1) 


coleccion.find().sort({'tiempo': -1}).limit(1)


#¿Cuál es el método correcto para agregar un nuevo dato a una colección?


coleccion.insert_one({...}) 




#¿Qué opciones son válidas para actualizar un campo de un documento en MongoDB?


coleccion.update_one({'sensor': 'dht11'}, {'$set': {'humedad': 60}}) 

coleccion.update({'sensor': 'dht11'}, {'$set': {'humedad': 60}})  

coleccion.update_many({}, {'$set': {'humedad': 60}}) 

#¿Qué comando elimina un documento por condición en MongoDB?


coleccion.delete_one({'sensor': 'dht11'})  
coleccion.delete_many({'sensor': 'dht11'})  

#¿Qué comandos permiten insertar varios documentos al mismo tiempo?


coleccion.insert_many([  
    {'sensor': 'dht11', 'valor': 25},
    {'sensor': 'mq135', 'valor': 70}
])


#¿Qué sentencia es válida para buscar todos los sensores DHT11?


coleccion.find({'sensor': 'dht11'})  

#¿Qué comandos ordenan los documentos de forma descendente por temperatura?


coleccion.find().sort('temperatura', -1) 
db.find().sort({'temperatura': -1})      


#¿Cuál es la sintaxis correcta de un documento BSON?


{"sensor": "dht11", "valor": 32}  



# ¿Qué comando permite contar el número de documentos en una colección?
coleccion.count_documents({})



#¿Qué comando permite eliminar todos los documentos de una colección?
coleccion.delete_many({})


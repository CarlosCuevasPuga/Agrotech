import paho.mqtt.client as mqtt
import logging

MAIOTA_DATA = []
client_id = "Equipo 1"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al Sensor MAIoTA con éxito. Los Payloads recibidos son: ")
        client.subscribe("Awi7LJfyyn6LPjg/15046220")
    else:
        print("Fallo al conectarse, código de resultado: " + str(rc))


def on_message(client, userdata, msg):
    Payload = str(msg.payload.decode("utf-8"))
    print("Mensaje recibido -> " + Payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect("broker.emqx.io", 1883, 60)
except Exception as e:
    logging.exception(f"Error al conectar al Sensor MAIoTA: {e}")
    exit()
if __name__ == "__main__":
    client.loop_forever()
"""
-------------------------------------------------------------------------------------------------------------------------
La descripción del Payload es la siguiente (veamosla con un ejemplo):
Payload=CIoTA-D1=2603&D2=5411&D3=2542&D4=43&D5=580&D6=103&D7=1&
                 |       |       |       |     |      |      |_  data NOx. No se opera. Valor = Index 1  
                 |       |       |       |     |      |_  data COV. No se opera. Valor = Index 103           
                 |       |       |       |     |_  data CO2. No se opera. Valor = 580 ppm     
                 |       |       |       |_  data Iluminacion. Se divide entre 10. Valor =43/10 = 4.3 Lux    
                 |       |       |_  data Humedad Suelo. Se divide entre 100. Valor =2542/100 = 25.42 %      
                 |       |_  data Humedad Ambiente. Se divide entre 100. Valor =5411/100 = 54.11 %       
                 |_  data Temperatura Ambiente. Se divide entre 100. Valor =2603/100 = 26.03 ºC
Notas sobre los campos:
*CIoTA- es el identificador de trama. En reto Agrotech siempre será lo mismo.
*Cada dato viene identificado con Dx= (donde x toma valores de 1 a 7)
*Cada dato termina con un &, ya que el contenido es variable. Optimiza longitud Payload.
*El valor mínimo de data Humedad Suelo es 24.65. Cuando la humedad es inferior a este valor aparece una flecha ↓24.65 %.
-------------------------------------------------------------------------------------------------------------------------
 """
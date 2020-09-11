import json
import cognitive_face as CF
import sys
from PIL import Image, ImageDraw, ImageFont
import time
#import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
#from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

SUBSCRIPTION_KEY = os.environ['COGNITIVE_SERVICE_KEY']
BASE_URL = os.environ['FACE_ENDPOINT']
PERSON_GROUP_ID = 'modelo-famosos'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

def detectar_emociones(foto):
    data = open(foto, 'rb')
    print("DATA",data)
    t0 = time.time()
    #headers = {'Ocp-Apim-Subscription-Key': KEY} Se puede usar este header cuando usa un url de internet y en lugar de data usa json{url: url(entre comillas)}
    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY} #Funciona porque tiene el content  type
    params = {
        'returnFaceAttributes': 'emotion',
    }
    face_api_url = BASE_URL+'detect'
    response = requests.post(face_api_url, params=params,
                            headers=headers, data=data)
    json_detected = response.json()
    print("Duracion", str(time.time()-t0))
    imagen = Image.open(foto)
    dibujar = ImageDraw.Draw(imagen)
    face_num = 1
    for resp in json_detected:        
        faceRectangle = resp['faceRectangle']
        width = faceRectangle['width']
        top = faceRectangle['top']
        height = faceRectangle['height']
        left = faceRectangle['left']
        emociones = resp['faceAttributes']['emotion']
        print(width,top,height,left)
        print("EMOCIONES",emociones)
    
        dibujar.rectangle((left,top,left + width,top+height), outline='red')
        #emociones = detectar_emociones(foto)
        y = 20
        font = ImageFont.truetype('Roboto-Regular.ttf', 15)
        dibujar.text((top-50, y - 20), "Face number "+str(face_num), font=font, fill="black")
        for e in emociones:
            if emociones[e] > 0.0:
                #emocion = traducir_sentimiento(e)
                #dibujar.text((top-50, y), e,  fill="black")
                dibujar.text((top-50, y), str( e + " " +str(round(emociones[e]*100,2)))+"%", font=font, fill="black")
                y += 20
    imagen.show()
detectar_emociones('imagenes/mujer.jpg')


import os, io
from google.cloud import vision
from google.cloud.vision import types
import time
from PIL import Image, ImageDraw, ImageFont

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'api_vision_key.json'
client=vision.ImageAnnotatorClient()

nombre = "mujer.jpg"
path = f'./imagenes/{nombre}'

def detectar_rostros():
    with io.open(path,'rb') as imagen_f:
        contenido = imagen_f.read()
    t0 = time.time()
    image = vision.types.Image(content=contenido) # pylint: disable=no-member
    response = client.face_detection(image= image) # pylint: disable=no-member
    response_json = response.face_annotations
    print("Duracion", str(time.time()-t0))
    imagen = Image.open(path)
    dibujar = ImageDraw.Draw(imagen)
    lista_probabilidad = ('unknown', 'very_unlikely', 'unlikely', 'possible', 'likely', 'very_likely')
    
    for face in response_json:
        expresiones=dict(joy_likelihood=lista_probabilidad[face.joy_likelihood],
                        sorrow_likelihood=lista_probabilidad[face.sorrow_likelihood],
                        anger_likelihood=lista_probabilidad[face.anger_likelihood],
                        surprise_likelihood=lista_probabilidad[face.surprise_likelihood],
                        under_likelihood=lista_probabilidad[face.under_exposed_likelihood],
                        blurred_likelihood=lista_probabilidad[face.blurred_likelihood],
                        headwear_likelihood=lista_probabilidad[face.headwear_likelihood])
        
        
        #polígono de marco de cara
        vertices=[]
        for vertex in face.bounding_poly.vertices:
            vertices.append (dict (x=vertex.x, y=vertex.y))
        dibujar.rectangle((vertices[0]["x"],vertices[1]["y"],vertices[2]["x"],vertices[3]["y"]),outline='red')
        y = 20
        for e in expresiones:
            #emocion = traducir_sentimiento(e)
            #dibujar.text((top-50, y), e,  fill="black")
            font = ImageFont.truetype('Roboto-Regular.ttf', 15)
            dibujar.text((50, y), str( e + ": " +str(expresiones[e])), font=font, fill="black")
            y += 20
    imagen.show()

detectar_rostros()
print("**********                                        Vision API     vs     Cognitive services**********")
print("Permite  entrenar un modelo con una persona:            No                       Si")
print("Permite entrenar un modelo con grupos                   No                       Si")
print("Permite reconocer un rostro                             No                       Si")
print("Permite detectar un rostro                              Si                       Si")
print("Permite detectar las emociones de un rostro             Si                       Si")
print("Muestra aparición de emociones en poncentajes           No                       Si")
print("Muestra aparición de las emociones en texto             Si                       No")
print("Muestra las coordenadas de los rostros                  Si                       Si")
print("Permite detectar enojo                                  Si                       Si")
print("Permite detectar desprecio                              No                       Si")
print("Permite detectar asco                                   No                       Si")
print("Permite detectar miedo                                  No                       Si")
print("Permite detectar felicidad                              Si                       Si")
print("Permite detectar neutralidad                            No                       Si")
print("Permite detectar tristeza                               Si                       Si")
print("Permite detectar sorpresa                               Si                       Si")
print("Permite detectar accesorio en la cabeza                 Si                       Si")
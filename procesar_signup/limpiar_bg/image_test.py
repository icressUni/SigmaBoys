from flask import Flask, request, jsonify, send_file
#from flask_cors import CORS
import face_recognition
import cv2
import numpy as np
import os
import pickle
import base64
from io import BytesIO
import tempfile
import uuid


imagen = face_recognition.load_image_file("Felipe/captured_image_down.jpg")
    # Convertir a RGB
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    
    # Encontrar rostros en la imagen
print("aaaa")
ubicaciones_rostros = face_recognition.face_locations(imagen)
codificaciones_rostros = face_recognition.face_encodings(imagen, ubicaciones_rostros)

resultados = []

for (top, right, bottom, left), codificacion_rostro in zip(ubicaciones_rostros, codificaciones_rostros):
    # Comparar con rostros conocidos
    coincidencias = face_recognition.compare_faces(rostros_conocidos, codificacion_rostro, tolerance=0.4)
    nombre = "Desconocido"
    
    # Encontrar la mejor coincidencia
    distancias_faciales = face_recognition.face_distance(rostros_conocidos, codificacion_rostro)
    mejor_coincidencia = np.argmin(distancias_faciales) if len(distancias_faciales) > 0 else -1
    
    if mejor_coincidencia >= 0 and coincidencias[mejor_coincidencia]:
        nombre = nombres_conocidos[mejor_coincidencia]
        confianza = float(1 - distancias_faciales[mejor_coincidencia])
    else:
        confianza = 0.0
    
    # Dibujar un rectángulo
    cv2.rectangle(imagen_rgb, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.rectangle(imagen_rgb, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(imagen_rgb, nombre, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
import jinja2
import tkinter as tk
import pdfkit
import openpyxl
import http.client
import ssl
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk

import http.client
import ssl
from conexion import crear_conexion, ejecutar_consulta

def leer_clientes():
    consulta = "SELECT nombrecliente, direccion, celular FROM Clientes WHERE celular IS NOT NULL;"
    return ejecutar_consulta(crear_conexion(), consulta)


import http.client
import ssl
from conexion import leer_clientes  # Asegúrate de que este import está correcto

def enviarpdfs():
    clientes = leer_clientes()  # Obtiene los clientes directamente de la base de datos

    # Configuración de la conexión HTTP
    conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())
    headers = {'content-type': "application/x-www-form-urlencoded"}
    token = "r2dwow6y1u7juzzt"  # Reemplaza con tu token real

    for cliente in clientes:
        # Asumiendo que cliente[0] es el nombre del cliente y cliente[1] es el número de celular
        filename = cliente[1].replace(" ", "_")  # Reemplaza espacios con guiones bajos para nombres de archivo
        to_number = cliente[2]  # Asegúrate de que cliente[3] es el número de celular

        payload = f"token={token}&to=+51{to_number}&filename=recibo_{filename}.pdf&document=http://200.60.11.181/recibos/recibo_{filename}.pdf&caption=RECIBO"
        payload = payload.encode('utf8').decode('iso-8859-1')

        conn.request("POST", "/instance76590/messages/document", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    conn.close()

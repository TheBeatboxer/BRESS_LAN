import jinja2
import tkinter as tk
import pdfkit
import openpyxl
import http.client
import ssl
from cargar_datos import cargar_datos_postgres, crear_conexion
from tabulate import tabulate
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
from psycopg2 import Error

#OBTIENE TODOS LOS DATOS DE LA TABLA DE CLIENTES DE EXCEL
datos = cargar_datos_postgres()

def general_deuda():
    try:
        conexion = crear_conexion()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor()

        # Actualiza la deuda de todos los clientes sumando 1 a la columna de deuda
        cursor.execute("UPDATE Clientes SET deuda = COALESCE(deuda, 0) + 1")

        conexion.commit()
        messagebox.showinfo("Éxito", "Deuda generada exitosamente.")
    except Error as e:
        messagebox.showerror("Error", f"Error al generar deuda: {e}")
    finally:
        if conexion:
            cursor.close()
            conexion.close()

import tkinter as tk
from tkinter import simpledialog, messagebox
import http.client
import ssl
import os
from conexion import crear_conexion

# Función que obtiene las zonas de la base de datos
def obtener_zonas():
    conexion = crear_conexion()
    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()
        consulta = "SELECT idzona, nombrezona FROM Zona"
        cursor.execute(consulta)
        zonas = cursor.fetchall()
        return zonas
    except Exception as e:
        print(f"Error al obtener zonas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Función que obtiene los clientes por zona
def obtener_clientes_por_zona(zona):
    conexion = crear_conexion()
    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()
        consulta = "SELECT nombrecliente, numerocliente FROM Clientes WHERE idzona = %s"
        cursor.execute(consulta, (zona,))
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Función para enviar mensajes personalizados a los clientes
def enviar_mensajes(clientes, mensaje_base):
    try:
        conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl.create_default_context())
        headers = {'content-type': "application/x-www-form-urlencoded"}
        token = os.getenv("API_TOKEN")

        if not token:
            print("API token no encontrado en las variables de entorno.")
            return

        for nombrecliente, numerocliente in clientes:
            mensaje = mensaje_base.replace("{nombrecliente}", nombrecliente)
            payload = f"token={token}&to=+51{numerocliente}&body={mensaje}"
            conn.request("POST", "/instance76590/messages/chat", payload, headers)
            response = conn.getresponse().read().decode("utf-8")
            print(response)

        conn.close()
    except Exception as e:
        print(f"Error al enviar mensajes: {e}")

# Interfaz gráfica para enviar mensajes
def mostrar_ventana_enviar_mensajes(cuerpo_principal):
    # Limpiar el contenido previo del cuerpo principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    tk.Label(cuerpo_principal, text="Seleccione la zona:").pack(pady=5)
    zonas = obtener_zonas()
    opciones_zonas = {nombrezona: idzona for idzona, nombrezona in zonas}

    if not zonas:
        messagebox.showwarning("Error", "No se pudieron cargar las zonas.")
        return

    variable_zona = tk.StringVar(cuerpo_principal)
    variable_zona.set(list(opciones_zonas.keys())[0])  # Selecciona el primer elemento por defecto
    menu_zonas = tk.OptionMenu(cuerpo_principal, variable_zona, *opciones_zonas.keys())
    menu_zonas.pack(pady=5)

    tk.Label(cuerpo_principal, text="Ingrese el mensaje a enviar (use {nombrecliente} para el nombre del cliente):").pack(pady=5)
    entrada_mensaje = tk.Entry(cuerpo_principal, width=50)
    entrada_mensaje.pack(pady=5)

    def enviar():
        nombre_zona = variable_zona.get()
        zona = opciones_zonas[nombre_zona]
        mensaje = entrada_mensaje.get()
        if not mensaje:
            messagebox.showwarning("Campos Vacíos", "Por favor ingrese el mensaje.")
            return

        clientes = obtener_clientes_por_zona(zona)
        if clientes:
            enviar_mensajes(clientes, mensaje)
            messagebox.showinfo("Éxito", "Mensajes enviados correctamente.")
        else:
            messagebox.showwarning("Sin Clientes", "No se encontraron clientes en la zona especificada.")

    boton_enviar = tk.Button(cuerpo_principal, text="Enviar Mensajes", command=enviar)
    boton_enviar.pack(pady=10)

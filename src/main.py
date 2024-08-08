import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, font
from PIL import ImageTk
from Util.util_ventana import centrar_ventana
from Util.util_imagen import resize_image
from Util.config_color import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from datetime import datetime
#from editar_cliente import abrir_ventana_edicion
from conexion import leer_clientes
from general_pdf import ingresar_nombre
from generar_deuda import general_deuda
from general_pdf_masivo import iniciar_generacion_masiva
from registro_cliente import abrir_ventana_registro
from cortar_cliente import cortar_cliente
from mostrar_datos import mostrar_datos
from mensaje_masivo import mostrar_ventana_enviar_mensajes
from enviar_pdf import enviarpdfs

# Función para redimensionar y actualizar la imagen de fondo
def actualizar_imagen(event):
    nuevo_ancho = event.width
    nuevo_alto = event.height
    imagen_fondo_redimensionada = resize_image("C:/Users/gilbe/Documents/06/BRESS-LAN/src/estilos/imagen/bl.png", nuevo_ancho, nuevo_alto)
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo_redimensionada)
    label_fondo.config(image=imagen_fondo_tk)
    label_fondo.image = imagen_fondo_tk

def mostrar_lista_clientes(cuerpo_principal, clientes):
    # Limpiar el cuerpo principal antes de agregar nuevos widgets
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Configuración de la tabla
    tabla = ttk.Treeview(cuerpo_principal, columns=("Nombre", "Dirección", "Celular"), show='headings')
    tabla.heading('Nombre', text='Nombre')
    tabla.heading('Dirección', text='Dirección')
    tabla.heading('Celular', text='Celular')

    # Configurar el ancho de las columnas
    tabla.column('Nombre', anchor='center', width=180)
    tabla.column('Dirección', anchor='center', width=180)
    tabla.column('Celular', anchor='center', width=180)

    # Insertar datos en la tabla
    for cliente in clientes:
        tabla.insert('', 'end', values=(cliente[1], cliente[3], cliente[4]))

    # Configuración del scroll vertical
    scroll = ttk.Scrollbar(cuerpo_principal, orient="vertical", command=tabla.yview)
    scroll.pack(side='right', fill='y')
    tabla.configure(yscrollcommand=scroll.set)

    # Empaquetar la tabla en el cuerpo principal
    tabla.pack(expand=True, fill='both')
# Configuración de la ventana principal
ventana_general = tk.Tk()
ventana_general.title("BRESS-LAN")
ventana_general.iconbitmap("C:/Users/gilbe/Documents/06/BRESS-LAN/src/estilos/imagen/bl2.ico")

aplicacion_ancho = 800
aplicacion_largo = 600
centrar_ventana(ventana_general, aplicacion_ancho, aplicacion_largo)

# Establecer color y una barra superior
barra_superior = tk.Frame(ventana_general, bg=COLOR_BARRA_SUPERIOR, height=50, bd=1, relief=tk.SUNKEN)
barra_superior.pack(side=tk.TOP, fill='both')

barra_lateral = tk.Frame(ventana_general, bg=COLOR_MENU_LATERAL, width=300)
barra_lateral.pack(side=tk.LEFT, fill='both', expand=False)

# Establecer color al cuerpo de la ventana
cuerpo_principal = tk.Frame(ventana_general, bg=COLOR_CUERPO_PRINCIPAL)
cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

# Redimensionar la imagen de fondo inicial al tamaño del cuerpo principal
imagen_fondo_redimensionada = resize_image("C:/Users/gilbe/Documents/06/BRESS-LAN/src/estilos/imagen/bg.png", aplicacion_ancho, aplicacion_largo)
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo_redimensionada)

# Crear un widget Label para mostrar la imagen de fondo en el centro del cuerpo principal
label_fondo = tk.Label(cuerpo_principal, image=imagen_fondo_tk)
label_fondo.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Vincular el evento de cambio de tamaño del cuerpo principal a la función de actualización de imagen
cuerpo_principal.bind("<Configure>", actualizar_imagen)

# Título del sistema
labelTitulo = tk.Label(barra_superior, text="BRESS-LAN", font=("Roboto", 17), fg="white",
                       bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
labelTitulo.pack(side=tk.LEFT)

# Funciones para cambiar el color de los botones al pasar el ratón por encima y al salir
def on_enter(event, button):
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

def on_leave(event, button):
    button.config(bg=COLOR_MENU_LATERAL, fg='White')

# Configuración de los botones del menú lateral
def configurar_boton(button, text, command):
    button.config(
        text=f"{text}",
        font=font.Font(family='FontAwesome', size=10, weight='bold'),
        bg=COLOR_MENU_LATERAL,
        fg='White',
        activebackground='#303031',
        command=command
    )
    button.pack(fill='both', expand=True)
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))


# Botones de la interfaz
boton_ingresar_cliente = tk.Button(barra_lateral)
configurar_boton(boton_ingresar_cliente, "INGRESAR CLIENTE", lambda: abrir_ventana_registro(cuerpo_principal))

boton_general_pdf = tk.Button(barra_lateral)
configurar_boton(boton_general_pdf, "GENERAR UN RECIBO", lambda: ingresar_nombre(cuerpo_principal))

# Configurar botones en la barra lateral
boton_generar_pdfs_masivos = tk.Button(barra_lateral)
configurar_boton(boton_generar_pdfs_masivos, "GENERAR TODOS LOS RECIBOS", iniciar_generacion_masiva)

boton_enviar_pdfs_masivos = tk.Button(barra_lateral)
configurar_boton(boton_enviar_pdfs_masivos, "ENVIAR PDFS", enviarpdfs)

boton_general_deuda = tk.Button(barra_lateral)
configurar_boton(boton_general_deuda, "GENERAR DEUDA", general_deuda)

boton_cortar_cliente = tk.Button(barra_lateral)
configurar_boton(boton_cortar_cliente, "CORTAR SERVICIO", lambda: cortar_cliente(cuerpo_principal))

boton_mostrar_deudores = tk.Button(barra_lateral)
configurar_boton(boton_mostrar_deudores, "MOSTRAR DEUDORES", lambda: mostrar_datos(cuerpo_principal))

boton_enviar_mensajes = tk.Button(barra_lateral)
configurar_boton(boton_enviar_mensajes, "ENVIAR MENSAJES MASIVOS", lambda: mostrar_ventana_enviar_mensajes(cuerpo_principal))

# Agregar el botón para editar clientes en la barra lateral
# Agregar el botón para editar clientes en la barra lateral
boton_editar_cliente = tk.Button(barra_lateral)
configurar_boton(boton_editar_cliente, "EDITAR CLIENTE", lambda: mostrar_lista_clientes(cuerpo_principal))



# Ejecutar el frame
ventana_general.mainloop()

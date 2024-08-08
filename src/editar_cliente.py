import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from conexion import leer_clientes

# Conexión a la base de datos
def conectar_a_db():
    try:
        conexion = psycopg2.connect(
            user="postgres",  # Reemplaza esto con el usuario real
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN"
        )
        return conexion
    except psycopg2.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None

# Obtener clientes desde la base de datos
def obtener_clientes():
    conexion = conectar_a_db()
    if conexion is not None:
        cursor = conexion.cursor()
        cursor.execute("SELECT idcliente, nombrecliente, direccion, celular FROM Clientes;")
        clientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return clientes
    else:
        return []

# Actualizar la información del cliente en la base de datos
def actualizar_cliente(cliente_id, nombre, direccion, celular):
    conexion = conectar_a_db()
    if conexion is not None:
        cursor = conexion.cursor()
        cursor.execute("UPDATE Clientes SET nombrecliente=%s, direccion=%s, celular=%s WHERE idcliente=%s", (nombre, direccion, celular, cliente_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")

# Mostrar clientes en una tabla con opción para editar
def mostrar_lista_clientes(cuerpo_principal):
    clientes = leer_clientes()  # Esta función debe devolver una lista de clientes desde la base de datos

    # Limpia el área donde se mostrarán los clientes
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Crea la tabla para mostrar los clientes
    tabla = ttk.Treeview(cuerpo_principal, columns=("Nombre", "Dirección", "Celular"), show='headings')
    tabla.heading('Nombre', text='Nombre')
    tabla.heading('Dirección', text='Dirección')
    tabla.heading('Celular', text='Celular')

    tabla.column('Nombre', anchor='center', width=180)
    tabla.column('Dirección', anchor='center', width=180)
    tabla.column('Celular', anchor='center', width=180)

    for cliente in clientes:
        tabla.insert('', 'end', values=(cliente[1], cliente[2], cliente[3]))

    # Agrega scrollbar a la tabla
    scroll = ttk.Scrollbar(cuerpo_principal, orient="vertical", command=tabla.yview)
    scroll.pack(side='right', fill='y')
    tabla.configure(yscrollcommand=scroll.set)
    tabla.pack(expand=True, fill='both')


# Editar el cliente seleccionado
def editar_cliente_seleccionado(tabla):
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showinfo("Error", "Por favor, seleccione un cliente")
        return

    cliente = tabla.item(seleccionado, 'values')
    mostrar_formulario_edicion(cliente)

# Mostrar formulario de edición para el cliente
def mostrar_formulario_edicion(cliente):
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Cliente")

    tk.Label(ventana_edicion, text="Nombre").grid(row=0, column=0)
    nombre = tk.Entry(ventana_edicion)
    nombre.insert(0, cliente[1])
    nombre.grid(row=0, column=1)

    tk.Label(ventana_edicion, text="Dirección").grid(row=1, column=0)
    direccion = tk.Entry(ventana_edicion)
    direccion.insert(0, cliente[2])
    direccion.grid(row=1, column=1)

    tk.Label(ventana_edicion, text="Celular").grid(row=2, column=0)
    celular = tk.Entry(ventana_edicion)
    celular.insert(0, cliente[3])
    celular.grid(row=2, column=1)

    btn_guardar = tk.Button(ventana_edicion, text="Guardar Cambios", command=lambda: actualizar_cliente(cliente[0], nombre.get(), direccion.get(), celular.get()))
    btn_guardar.grid(row=3, column=0, columnspan=2)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import Error
from fpdf import FPDF

def cargar_datos_postgres():
    conexion = None
    cursor = None
    try:
        conexion = psycopg2.connect(
            user="postgres",
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN",
            options='-c client_encoding=UTF8'
        )
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT 
            Clientes.nombrecliente AS cliente_nombre,
            Planes.titulo AS plan_titulo,
            Planes.precio AS plan_precio,
            Clientes.deuda AS deuda,
            Clientes.deuda * Planes.precio AS deuda_total
        FROM 
            Clientes
        JOIN 
            Planes ON Clientes.idplan = Planes.idplan
        WHERE 
            Clientes.deuda > 0;
        """)
        datos = cursor.fetchall()
        print(datos)  # Imprimir los datos para verificar su estructura
        return datos
    except Error as e:
        print("Error al leer datos de PostgreSQL:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def cargar_datos_postgres_filtrados(nombre_cliente):
    conexion = None
    cursor = None
    try:
        conexion = psycopg2.connect(
            user="postgres",
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN",
            options='-c client_encoding=UTF8'
        )
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT 
            Clientes.nombrecliente AS cliente_nombre,
            Planes.titulo AS plan_titulo,
            Planes.precio AS plan_precio,
            Clientes.deuda AS deuda,
            Clientes.deuda * Planes.precio AS deuda_total
        FROM 
            Clientes
        JOIN 
            Planes ON Clientes.idplan = Planes.idplan
        WHERE 
            Clientes.nombrecliente ILIKE %s AND Clientes.deuda > 0;
        """, (f"%{nombre_cliente}%",))
        datos = cursor.fetchall()
        return datos
    except psycopg2.Error as e:
        print("Error al leer datos de PostgreSQL:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def exportar_a_pdf(datos):
    """Función para exportar datos a un archivo PDF"""
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Definir el ancho de las columnas
    col_widths = [60, 60, 40, 40, 60]
    headers = ["Nombre", "Plan", "Precio", "Deuda", "Deuda Total"]

    # Encabezados de la tabla
    pdf.set_fill_color(200, 220, 255)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
    pdf.ln()

    # Datos de la tabla
    pdf.set_fill_color(255, 255, 255)
    for row in datos:
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 10, str(item), border=1, align='C', fill=True)
        pdf.ln()

    pdf.output("datos_filtrados_mejorado.pdf")
    messagebox.showinfo("Exportar a PDF", "Los datos se han exportado exitosamente a datos_filtrados_mejorado.pdf")

def mostrar_datos(cuerpo_principal):
    datos = cargar_datos_postgres()
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    cols = ("Nombre", "Plan", "Precio", "Deuda", "Deuda Total")
    tabla = ttk.Treeview(cuerpo_principal, columns=cols, show='headings')
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, width=100, anchor="center")

    for dato in datos:
        tabla.insert("", "end", values=dato)

    tabla.pack(expand=True, fill='both')
    setup_busqueda(cuerpo_principal, tabla)
    setup_quitar_deuda(cuerpo_principal, tabla)
    btn_exportar_pdf = tk.Button(cuerpo_principal, text="Exportar a PDF", command=lambda: exportar_a_pdf(datos))
    btn_exportar_pdf.pack(pady=10)

def setup_busqueda(cuerpo_principal, tabla):
    entrada_nombre = tk.Entry(cuerpo_principal, font=('Arial', 12))
    entrada_nombre.pack(pady=20, padx=20, side=tk.LEFT)

    boton_buscar = tk.Button(cuerpo_principal, text="Buscar Cliente", command=lambda: buscar_cliente(entrada_nombre.get(), tabla))
    boton_buscar.pack(side=tk.LEFT)

def buscar_cliente(nombre, tabla):
    datos = cargar_datos_postgres_filtrados(nombre)
    if not datos:
        messagebox.showinfo("Resultado", "Este cliente no debe.")
    else:
        for i in tabla.get_children():
            tabla.delete(i)  # Limpiar la tabla antes de agregar nuevos datos
        for dato in datos:
            tabla.insert("", "end", values=dato)

def setup_quitar_deuda(cuerpo_principal, tabla):
    entrada_quitar = tk.Entry(cuerpo_principal, font=('Arial', 12))
    entrada_quitar.pack(pady=20, padx=20, side=tk.LEFT)

    boton_quitar = tk.Button(cuerpo_principal, text="Quitar Deuda", command=lambda: quitar_deuda(entrada_quitar.get(), tabla))
    boton_quitar.pack(side=tk.LEFT)

def quitar_deuda(cantidad, tabla):
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showinfo("Error", "Por favor, seleccione un cliente de la tabla")
        return

    valores = tabla.item(seleccionado, 'values')
    nombre_cliente = valores[0]
    deuda_actual = int(valores[3])

    nueva_deuda = deuda_actual - int(cantidad)

    if nueva_deuda < 0:
        messagebox.showinfo("Error", "La cantidad a quitar es mayor que la deuda actual")
        return

    actualizar_deuda_cliente(nombre_cliente, nueva_deuda)
    tabla.item(seleccionado, values=(valores[0], valores[1], valores[2], nueva_deuda, int(valores[2]) * nueva_deuda))

def actualizar_deuda_cliente(nombre_cliente, nueva_deuda):
    try:
        conexion = psycopg2.connect(
            user="postgres",
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN",
            options='-c client_encoding=UTF8'
        )
        cursor = conexion.cursor()
        cursor.execute("UPDATE Clientes SET deuda = %s WHERE nombrecliente = %s", (nueva_deuda, nombre_cliente))
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Éxito", "Deuda actualizada correctamente")
    except Exception as e:
        messagebox.showinfo("Error", f"Error al actualizar la deuda: {e}")

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from psycopg2 import Error
from conexion import crear_conexion  # Asegúrate de importar crear_conexion desde el archivo correcto

# Diccionario para mapear nombres de zonas a sus IDs en la base de datos
zonas_ids = {
    "Santa Cruz": 1,
    "Progreso": 2,
    "Río Uchiza": 3,
    "Porongo": 4,
    "Santa Lucia": 5,
    "Mareategui": 6,
    "Buenos Aires": 7,
    "Tocache": 8,
    "Las Flores": 9,
    "Pizana": 10,
    "Santa Rosa de Mishollo": 11,
    "Miraflores": 12
}

def insertar_cliente(nombre, ids, direccion, celular, plan, zona, estado):
    """Función para insertar un cliente en la base de datos PostgreSQL"""
    conexion = crear_conexion()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        consulta = '''
            INSERT INTO Clientes (nombrecliente, numerocliente, direccion, celular, deuda, idestado, idplan, idzona)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        parametros = (nombre.upper(), ids, direccion.upper(), celular, 0, estado, plan, zona)  # Convertir a mayúsculas
        cursor.execute(consulta, parametros)
        conexion.commit()
        messagebox.showinfo("Éxito", "El cliente se ha registrado con éxito.")
    except Error as e:
        messagebox.showerror("Error", f"Error al insertar cliente: {e}")
    finally:
        if conexion:
            cursor.close()
            conexion.close()

def insertar_plan_personalizado(titulo, descripcion, precio):
    """Función para insertar un plan personalizado en la base de datos PostgreSQL y devolver su ID"""
    conexion = crear_conexion()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return None

    try:
        cursor = conexion.cursor()
        consulta = '''
            INSERT INTO Planes (titulo, descripcion, precio)
            VALUES (%s, %s, %s) RETURNING idplan;
        '''
        cursor.execute(consulta, (titulo.upper(), descripcion.upper(), precio))  # Convertir a mayúsculas
        plan_id = cursor.fetchone()[0]
        conexion.commit()
        return plan_id
    except Error as e:
        print("Error al insertar plan personalizado:", e)  # Mensaje de depuración
        messagebox.showerror("Error", f"Error al insertar plan personalizado: {e}")
        return None
    finally:
        if conexion:
            cursor.close()
            conexion.close()

def abrir_ventana_registro(cuerpo_principal):
    limpiar_cuerpo_principal(cuerpo_principal)

    def insertar_datos():
        nombre = entry_nombre.get()
        ids = entry_id.get()
        direccion = entry_direccion.get()
        celular = entry_celular.get()
        plan = variable_plan.get()
        zona = zonas_ids[variable_zona.get()]
        estado = 1  # Asegúrate de que este valor es correcto y corresponde a tu base de datos

        if not nombre or not ids or not direccion or not celular or not plan or not zona:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Validar que los campos numéricos sean efectivamente numéricos
        try:
            ids = int(ids)
            celular = int(celular)
        except ValueError:
            messagebox.showwarning("Advertencia", "ID y Celular deben ser numéricos.")
            return

        if plan == "plan personalizado":
            abrir_ventana_plan_personalizado(nombre, ids, direccion, celular, estado, zona, cuerpo_principal)
        else:
            plan_numerico = valores_planes[plan]
            insertar_cliente(nombre, ids, direccion, celular, plan_numerico, zona, estado)  # Agregamos el argumento estado aquí
            

        entry_nombre.delete(0, tk.END)
        entry_id.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_celular.delete(0, tk.END)

    etiqueta_nombre = tk.Label(cuerpo_principal, text="Nombre:")
    entry_nombre = tk.Entry(cuerpo_principal)

    etiqueta_id = tk.Label(cuerpo_principal, text="ID:")
    entry_id = tk.Entry(cuerpo_principal)

    etiqueta_direccion = tk.Label(cuerpo_principal, text="Dirección:")
    entry_direccion = tk.Entry(cuerpo_principal)

    etiqueta_celular = tk.Label(cuerpo_principal, text="Celular:")
    entry_celular = tk.Entry(cuerpo_principal)

    etiqueta_plan = tk.Label(cuerpo_principal, text="Plan:")
    planes = ["plan hogar 15Mb", "plan hogar 25Mb", "plan hogar 35Mb", "duo 15Mb + TV", "duo 25Mb + TV", "duo 35Mb + TV", "TV cable", "cable + anexo1", "cable + anexo2", "plan personalizado"]
    valores_planes = {
        "plan hogar 15Mb": 1,
        "plan hogar 25Mb": 2,
        "plan hogar 35Mb": 3,
        "duo 15Mb + TV": 4,
        "duo 25Mb + TV": 5,
        "duo 35Mb + TV": 6,
        "TV cable": 7,
        "cable + anexo1": 8,
        "cable + anexo2": 9
    }

    variable_plan = tk.StringVar(cuerpo_principal)
    variable_plan.set(planes[0])
    entry_plan = tk.OptionMenu(cuerpo_principal, variable_plan, *planes)

    etiqueta_zona = tk.Label(cuerpo_principal, text="Zona:")
    zonas = list(zonas_ids.keys())
    variable_zona = tk.StringVar(cuerpo_principal)
    variable_zona.set(zonas[0])
    entry_zona = ttk.Combobox(cuerpo_principal, textvariable=variable_zona)
    entry_zona['values'] = zonas

    boton_obtener = tk.Button(cuerpo_principal, text="Ingresar cliente", command=insertar_datos)

    etiqueta_nombre.pack(pady=5)
    entry_nombre.pack(pady=5)

    etiqueta_id.pack(pady=5)
    entry_id.pack(pady=5)

    etiqueta_direccion.pack(pady=5)
    entry_direccion.pack(pady=5)

    etiqueta_celular.pack(pady=5)
    entry_celular.pack(pady=5)

    etiqueta_plan.pack(pady=5)
    entry_plan.pack(pady=5)

    etiqueta_zona.pack(pady=5)
    entry_zona.pack(pady=5)

    boton_obtener.pack(pady=10)

def abrir_ventana_plan_personalizado(nombre, ids, direccion, celular, estado, zona, cuerpo_principal):
    limpiar_cuerpo_principal(cuerpo_principal)

    def guardar_plan_personalizado():
        titulo = entry_titulo.get()
        descripcion = entry_descripcion.get()
        precio = entry_precio.get()

        if not titulo or not descripcion or not precio:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Advertencia", "El precio debe ser numérico.")
            return

        plan_id = insertar_plan_personalizado(titulo, descripcion, precio)
        if plan_id:
            insertar_cliente(nombre, ids, direccion, celular, plan_id, zona, estado)
            limpiar_cuerpo_principal(cuerpo_principal)
            abrir_ventana_registro(cuerpo_principal)

    etiqueta_titulo = tk.Label(cuerpo_principal, text="Título:")
    entry_titulo = tk.Entry(cuerpo_principal)

    etiqueta_descripcion = tk.Label(cuerpo_principal, text="Descripción:")
    entry_descripcion = tk.Entry(cuerpo_principal)

    etiqueta_precio = tk.Label(cuerpo_principal, text="Precio:")
    entry_precio = tk.Entry(cuerpo_principal)

    boton_guardar = tk.Button(cuerpo_principal, text="Guardar Plan Personalizado", command=guardar_plan_personalizado)

    etiqueta_titulo.pack(pady=5)
    entry_titulo.pack(pady=5)

    etiqueta_descripcion.pack(pady=5)
    entry_descripcion.pack(pady=5)

    etiqueta_precio.pack(pady=5)
    entry_precio.pack(pady=5)

    boton_guardar.pack(pady=10)

def limpiar_cuerpo_principal(cuerpo_principal):
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

# Aquí se debería iniciar la aplicación Tkinter, pero asegúrate de que este archivo no se ejecute
# automáticamente si se importa como módulo en otros archivos.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Registro de Clientes")
    cuerpo_principal = ttk.Frame(root, padding="10 10 10 10")
    cuerpo_principal.pack(fill=tk.BOTH, expand=True)

    abrir_ventana_registro(cuerpo_principal)

    root.mainloop()

import tkinter as tk
from tkinter import messagebox
from cargar_datos import cargar_datos_postgres
from conexion import crear_conexion, ejecutar_consulta  # Asegúrate de importar correctamente tus funciones de conexión

def cortar_cliente(cuerpo_principal):
    def funcion_cortar():
        nombre_cliente = entry_nombre.get()  # Obtén el nombre del cliente desde la entrada
        try:
            # Crear la conexión a la base de datos
            conexion = crear_conexion()
            if not conexion:
                label_resultado.config(text="Error al conectar con la base de datos.")
                return

            # Consulta para actualizar el estado del cliente
            consulta = '''
                UPDATE Clientes
                SET idestado = 2
                WHERE nombrecliente = %s;
            '''
            parametros = (nombre_cliente,)

            # Ejecutar la consulta
            ejecutar_consulta(conexion, consulta, parametros)
            label_resultado.config(text="Estado actualizado con éxito.")
        except Exception as e:
            label_resultado.config(text=f"Error al actualizar estado: {e}")
        finally:
            if conexion:
                conexion.close()

    # Limpiar el contenido previo del cuerpo principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Crear y colocar los widgets en el cuerpo principal
    label_instruccion = tk.Label(cuerpo_principal, text="Ingrese el nombre del cliente a actualizar:")
    label_instruccion.pack(pady=5)

    entry_nombre = tk.Entry(cuerpo_principal)
    entry_nombre.pack(pady=5)

    boton_actualizar = tk.Button(cuerpo_principal, text="Actualizar Estado", command=funcion_cortar)
    boton_actualizar.pack(pady=10)

    label_resultado = tk.Label(cuerpo_principal, text="")
    label_resultado.pack(pady=5)
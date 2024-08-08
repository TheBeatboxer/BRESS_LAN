import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import Error
import psycopg2
from psycopg2 import OperationalError

def crear_conexion():
    """Función para conectar a la base de datos PostgreSQL"""
    try:
        conexion = psycopg2.connect(
            user="postgres",  # Reemplaza esto con el usuario real
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN"
        )
        print("Conexión exitosa")
        return conexion
    except OperationalError as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

def ejecutar_consulta(conexion, consulta, parametros=None):
    """Función para ejecutar consultas SQL"""
    try:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, parametros)
            if consulta.strip().lower().startswith('select'):
                return cursor.fetchall()
            else:
                conexion.commit()
                print("Operación ejecutada con éxito")
    except Error as e:
        print("Error al ejecutar la consulta SQL:", e)


def insertar_cliente(nombre, direccion, celular, plan, precio, estado):
    consulta = '''
        INSERT INTO Clientes (NombreClien, Direccion, Celular, Plan, Precio, Estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    parametros = (nombre, direccion, celular, plan, precio, estado)
    ejecutar_consulta(crear_conexion(), consulta, parametros)


def leer_clientes():
    conexion = psycopg2.connect(
            user="postgres",  # Reemplaza esto con el usuario real
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT idcliente, nombrecliente, direccion, celular FROM Clientes;")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes


def actualizar_cliente(id_cliente, nombre, direccion, celular, plan, precio, estado):
    consulta = '''
        UPDATE Clientes
        SET NombreClien = %s, Direccion = %s, Celular = %s, Plan = %s, Precio = %s, Estado = %s
        WHERE IdCliente = %s;
    '''
    parametros = (nombre, direccion, celular, plan, precio, estado, id_cliente)
    ejecutar_consulta(crear_conexion(), consulta, parametros)


def eliminar_cliente(id_cliente):
    consulta = "DELETE FROM Clientes WHERE IdCliente = %s;"
    parametros = (id_cliente,)
    ejecutar_consulta(crear_conexion(), consulta, parametros)

def leer_clientes_por_nombre(nombre):
    """Función para buscar clientes por nombre"""
    try:
        conexion = crear_conexion()
        cursor = conexion.cursor()
        select_query = "SELECT * FROM Clientes WHERE NombreClien ILIKE %s;"
        cursor.execute(select_query, ('%' + nombre + '%',))
        clientes = cursor.fetchall()
        if clientes:
            for cliente in clientes:
                print(cliente)
        else:
            print("No se encontraron clientes con el nombre", nombre)
    except (Exception, psycopg2.Error) as error:
        print("Error al buscar clientes por nombre:", error)
    finally:
        if conexion:
            cursor.close()
            conexion.close()


# Conexión a la base de datos
def conectar_a_db():
    return psycopg2.connect(
            user="postgres",  # Reemplaza esto con el usuario real
            password="RUFFNER25",
            host="localhost",
            port="5432",
            database="BRESS-LAN"
    )

# Obtener clientes desde la base de datos
def obtener_clientes():
    conexion = conectar_a_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT idcliente, nombrecliente, direccion, celular FROM Clientes;")
    clientes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return clientes

# Actualizar la información del cliente en la base de datos
def actualizar_cliente(cliente_id, nombre, direccion, celular):
    conexion = conectar_a_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Clientes SET nombrecliente=%s, direccion=%s, celular=%s WHERE idcliente=%s",
                   (nombre, direccion, celular, cliente_id))
    conexion.commit()
    cursor.close()
    conexion.close()
    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")

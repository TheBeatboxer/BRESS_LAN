import jinja2
import tkinter as tk
import pdfkit
import os
from cargar_datos import cargar_datos_postgres
from tkinter import messagebox

# Cargar datos desde PostgreSQL
datos = cargar_datos_postgres()

# Función para generar PDFs masivos
def general_pdf_masivos():
    print("Iniciando generación masiva de PDFs...")

    def crea_pdf(ruta_template, info, nombre_pdf, rutacss=""):
        try:
            print(f"Creando PDF para {nombre_pdf} con plantilla en {ruta_template}")
            nombre_template = os.path.basename(ruta_template)
            ruta_template_dir = os.path.dirname(ruta_template)
            print(f"Ruta del directorio de la plantilla: {ruta_template_dir}")

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template_dir))
            template = env.get_template(nombre_template)
            html = template.render(info)
            print(f"HTML renderizado para {nombre_pdf}")

            options = {
                'page-size': 'A4',
                'margin-top': '0.05in',
                'margin-right': '0.05in',
                'margin-bottom': '0.05in',
                'margin-left': '0.05in',
                'encoding': 'UTF-8',
                'disable-smart-shrinking': '',
                'no-stop-slow-scripts': '',
                'debug-javascript': '',
            }

            # Configurar la salida del PDF
            path_to_wkhtmltopdf = r'C:\\Users\\Dr.Pc.Solutions\\Documents\\BRESS-LAN\\librerias\\wkhtmltopdf.exe'  # Ruta al ejecutable wkhtmltopdf
            print(f"Ruta del ejecutable wkhtmltopdf: {path_to_wkhtmltopdf}")
            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

            # Asegurarse de que el directorio de salida existe
            output_dir = r'C:\\Users\\Dr.Pc.Solutions\\Documents\\BRESS-LAN\\recibos'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            ruta_salida = os.path.join(output_dir, f'recibo_{nombre_pdf}.pdf')
            pdfkit.from_string(html, ruta_salida, options=options, configuration=config)
            print(f"PDF generado: {ruta_salida}")
        except IOError as e:
            print(f"IOError generando PDF para {nombre_pdf}: {e}")
        except OSError as e:
            print(f"OSError generando PDF para {nombre_pdf}: {e}")
        except Exception as e:
            print(f"Error generando PDF para {nombre_pdf}: {e}")

    for dato in datos:
        try:
            print(f"Generando PDF para: {dato[1]}")
            ruta_template = r'C:\\Users\\Dr.Pc.Solutions\\Documents\\BRESS-LAN\\recursos\\template.html'
            if not os.path.exists(ruta_template):
                print(f"Error: La plantilla {ruta_template} no existe.")
                continue

            info = {
                "nombre": dato[1],
                "id": dato[2],
                "direccion": dato[3],
                "celular": dato[4],
                "plan": dato[10],
                "descripcion": dato[11],
                "precio": dato[12]
            }
            nombre_pdf = dato[1]
            print(f"Información: {info}")
            crea_pdf(ruta_template, info, nombre_pdf)
        except Exception as e:
            print(f"Error en la generación de PDF para {dato[1]}: {e}")

# Función para iniciar la generación de PDFs desde la interfaz Tkinter
def iniciar_generacion_masiva():
    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro que desea generar todos los PDFs?")
    if respuesta:
        general_pdf_masivos()
        messagebox.showinfo("Completado", "La generación de PDFs ha finalizado.")
    else:
        print("Generación masiva de PDFs cancelada.")

# Código de ejemplo para iniciar la interfaz Tkinter (opcional)
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Esconder la ventana principal de Tkinter
    iniciar_generacion_masiva()

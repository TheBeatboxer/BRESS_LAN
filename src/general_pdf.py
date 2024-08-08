import os
import pdfkit
import jinja2
import tkinter as tk
from tkinter import messagebox, ttk
from cargar_datos import cargar_datos_postgres

# Cargar datos desde PostgreSQL
datos = cargar_datos_postgres()

def ingresar_nombre(cuerpo_principal):
    limpiar_cuerpo_principal(cuerpo_principal)

    def buscar_clientes():
        nombre_busqueda = entry_nombre_generapdf.get().strip().lower()
        resultados = [cliente for cliente in datos if nombre_busqueda in cliente[1].strip().lower()]
        mostrar_resultados(resultados)

    etiqueta_nombre_generapdf = tk.Label(cuerpo_principal, text="Ingrese el nombre del cliente:")
    etiqueta_nombre_generapdf.pack(pady=5)

    entry_nombre_generapdf = tk.Entry(cuerpo_principal)
    entry_nombre_generapdf.pack(pady=5)

    boton_buscar_cliente = tk.Button(cuerpo_principal, text="Buscar", command=buscar_clientes)
    boton_buscar_cliente.pack(pady=10)

    treeview_resultados = ttk.Treeview(cuerpo_principal, columns=("ID", "Nombre", "Dirección", "Celular"), show="headings")
    treeview_resultados.heading("ID", text="ID")
    treeview_resultados.heading("Nombre", text="Nombre")
    treeview_resultados.heading("Dirección", text="Dirección")
    treeview_resultados.heading("Celular", text="Celular")
    treeview_resultados.pack(pady=10)

    def mostrar_resultados(resultados):
        for item in treeview_resultados.get_children():
            treeview_resultados.delete(item)
        for cliente in resultados:
            treeview_resultados.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3]))

    def seleccionar_cliente():
        seleccion = treeview_resultados.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un cliente.")
            return
        cliente_seleccionado = treeview_resultados.item(seleccion)["values"]
        crear_un_pdf(cliente_seleccionado[1])

    boton_seleccionar_cliente = tk.Button(cuerpo_principal, text="Generar PDF", command=seleccionar_cliente)
    boton_seleccionar_cliente.pack(pady=10)


def crear_un_pdf(nombre_cliente):
    global datos
    CLIENTE_BUSCADO = None

    for cliente in datos:
        nombre_cliente_bd = str(cliente[1]) if cliente[1] is not None else ""
        if nombre_cliente_bd.strip().lower() == nombre_cliente.strip().lower():
            CLIENTE_BUSCADO = cliente
            break
    else:
        print(f"{nombre_cliente} no se encontró en la base de datos.")
        return

    if CLIENTE_BUSCADO:
        try:
            info = {
                "nombre": CLIENTE_BUSCADO[1],
                "numeroCliente": str(CLIENTE_BUSCADO[2]),
                "direccion": CLIENTE_BUSCADO[3],
                "celular": CLIENTE_BUSCADO[4],
                "plan": CLIENTE_BUSCADO[7],
                "precioPlan": int(CLIENTE_BUSCADO[12]),
                "tituloPlan": CLIENTE_BUSCADO[10],
                "DescripcionPlan": CLIENTE_BUSCADO[11]
            }
            print(f"Información del cliente: {info}")

            ruta_template = r'C:/Users/ppier/OneDrive/Documentos/Proyects/06/BRESS-LAN/recursos/template.html'
            nombre_pdf = CLIENTE_BUSCADO[1]

            nombre_template = os.path.basename(ruta_template)
            ruta_template_dir = os.path.dirname(ruta_template)
            print(f"Ruta del directorio de la plantilla: {ruta_template_dir}")
            print(f"Nombre del archivo de la plantilla: {nombre_template}")

            env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template_dir))
            template = env.get_template(nombre_template)
            html = template.render(info)

            options = {
                'page-size': 'Letter',
                'margin-top': '0in',
                'margin-right': '0in',
                'margin-bottom': '0in',
                'margin-left': '0in',
                'encoding': 'UTF-8',
                'no-outline': None,
                'disable-smart-shrinking': None,
                'quiet': ''
            }

            path_to_wkhtmltopdf = r'C:/Users/ppier/OneDrive/Documentos/Proyects/06/BRESS-LAN/librerias/wkhtmltopdf.exe'
            if not os.path.exists(path_to_wkhtmltopdf):
                print(f"wkhtmltopdf executable not found at: {path_to_wkhtmltopdf}")
                return

            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            ruta_salida = f'C:/Users/ppier/OneDrive/Documentos/Proyects/06/BRESS-LAN/cliente/recibo_{nombre_pdf}.pdf'
            pdfkit.from_string(html, ruta_salida, options=options, configuration=config)
            print(f"PDF generado correctamente en: {ruta_salida}")

        except jinja2.TemplateNotFound as e:
            print(f"Error de plantilla: {e}. Asegúrate de que el archivo template.html existe y está en la ruta especificada.")
        except IndexError as e:
            print(f"Error de índice: {e}. Asegúrate de que el cliente tiene suficientes datos.")
        except TypeError as e:
            print(f"Error de tipo: {e}. Asegúrate de que el cliente es una lista o una tupla.")
        except Exception as e:
            print(f"Otro error: {e}")
            print(e.output)  # Para obtener más detalles del error
    else:
        print("CLIENTE_BUSCADO es None. No se puede generar el PDF.")


def limpiar_cuerpo_principal(cuerpo_principal):
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generación de PDFs de Clientes")
    cuerpo_principal = tk.Frame(root, padding="10 10 10 10")
    cuerpo_principal.pack(fill=tk.BOTH, expand=True)

    ingresar_nombre(cuerpo_principal)

    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import pyperclip
from tkcalendar import Calendar
from datetime import datetime, timedelta
import sys
from PIL import Image, ImageTk

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # Ruta temporal de PyInstaller
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

mainarchivo_env = os.path.join(BASE_DIR, "resources", "credenciales.env")
mainimagen_aceptar = os.path.join(BASE_DIR, "resources", "BotonRojoCosSolidAceptar.png")
mainimagen_canta = os.path.join(BASE_DIR, "resources", "BotonRojoCosSolidCanta.png")
mainimagen_reforma = os.path.join(BASE_DIR, "resources", "BotonRojoCosSolidReforma.png")

load_dotenv(mainarchivo_env)
#load_dotenv('credenciales.env')

# Datos de conexión a la base de datos desde el archivo .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#print(DB_NAME,DB_HOST,DB_PASSWORD,DB_USER)

# Cadena de conexión usando SQLAlchemy y pymssql
db_connection_string = f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crear el motor de SQLAlchemy
engine = create_engine(db_connection_string)

# Función para probar la conexión
def conectar_bd():
    try:
        # Intenta abrir una conexión
        connection = engine.connect()  # No usar 'with' si la conexión será usada fuera del contexto
        print("Conexión exitosa")
        return connection
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None  # Si la conexión falla, retornamos None


# Filtros predeterminados
companias = ['MUEVETE2', 'MUEVETE3', 'MUEVETE4', 'WELCOME', 'WPRO', 'EFECTIVA','TELCELR3']
tipos_llamada = ['VENTA', 'NO VENTA']
duraciones = ['00:01:00', '00:02:00', '00:03:00', '00:04:00', '00:05:00', '00:06:00', '00:07:00', '00:08:00', '00:09:00', '00:10:00']
saliEntrante = ['PREDICTIVO', 'SALIENTE']

campañasR = ['AGENTDIRECT',	'Blas_Desborde_Infini',	'Blas_Prepago_Forzoso',	'BLS_TAF',	'BLSDNS',	'CPBES',	'EST_MER',	'INFFOL',	'INFTM',	'INFTM2',	'INTEGRAL',	'MUEPOS',	'OVERSINE',	'PREFOES2',	'PREFORES',	'PREFORFO',	'PREFORLO',	'PRELIBES',	'PRELIBFR',	'PRELIBLO',	'RENM1',	'RENM2',	'RENROA',	'RENRS',	'RENRS2',	'RENSIN',	'RENTELUP',	'RETCHURN',	'ROAPRE',	'SALTOU',	'SEG_MUEP',	'SEGSINE2',	'SEGSINER',	'SUPCAL',	'TELLUP',	'TELUP2',	'TELUP3',	'TELUP4',	'TNDALN']
tipoR_llamadas = ['PREDICTIVO',	'SALIENTE',	'OTRO']
duracionesR = ['00:01:00', '00:02:00', '00:03:00', '00:04:00', '00:05:00', '00:06:00', '00:07:00', '00:08:00', '00:09:00', '00:10:00']
finaliza = ['NONE',	'CALLER',	'AGENT',	'ABANDON',	'QUEUETIMEOUT']


def copiar_al_portapapeles(tree):
    try:
        item = tree.selection()[0]  # Obtener la fila seleccionada
        values = tree.item(item, 'values')  # Obtener los valores de la fila
        # Convertir los valores a una cadena de texto separada por tabuladores
        text = '\t'.join(str(v) for v in values)
        pyperclip.copy(text)  # Copiar al portapapeles
        messagebox.showinfo("Copiado", "Datos copiados al portapapeles.")
    except IndexError:
        messagebox.showwarning("Advertencia", "Seleccione una fila para copiar.")

# Función para mostrar los resultados en un Treeview
def mostrar_resultados(resultados, ventana_filtros):
    # Crear un nuevo Toplevel para mostrar los resultados
    ventana_resultados = tk.Toplevel(ventana_filtros)
    ventana_resultados.title("Resultados de la Consulta")
    ventana_resultados.geometry("1000x150")

    # Crear el Treeview para mostrar los resultados
    tree = ttk.Treeview(ventana_resultados, columns=("fecha", "interactionid", "horainicio", "duracion", "tipo", "companytexto", "projecttexto", "Tipificacion", "usuario", "PROMOCION", "COMPAÑIA"), show="headings")

    # Definir las columnas del TreeView
    tree.heading("fecha", text="Fecha")
    tree.heading("interactionid", text="InteractionID")
    #tree.heading("numero", text="Número")
    tree.heading("horainicio", text="Hora Inicio")
    tree.heading("duracion", text="Duración")
    tree.heading("tipo", text="Tipo")
    tree.heading("companytexto", text="Compañía")
    tree.heading("projecttexto", text="Proyecto")
    tree.heading("Tipificacion", text="Tipificación")
    tree.heading("usuario", text="Usuario")
    tree.heading("PROMOCION", text="Promoción")
    tree.heading("COMPAÑIA", text="Compañía")

    # Función para convertir datetime a string (formato dd-mm-yyyy)
    def format_fecha(fecha):
        if isinstance(fecha, datetime):
            return fecha.strftime("%d-%m-%Y")  # Formato dd-mm-yyyy
        return fecha

    def format_hora(hora):
        if isinstance(hora, datetime):
            return hora.strftime("%d-%m-%Y %H:%M:%S")  # Formato dd-mm-yyyy HH:MM:SS
        elif isinstance(hora, timedelta):
            return str(hora)  # Si es una duración (timedelta)
        return hora

    # Agregar las filas al Treeview con formato adecuado
    for fila in resultados:
        fila_formateada = [
            format_fecha(fila[0]),  # Formato de la fecha
            fila[1],  # InteractionID
            fila[2],  
            format_hora(fila[3]),  # Hora Inicio formateada
            fila[4],  # Duración
            fila[5],  # Tipo
            fila[6],  # Compañía
            fila[7],  # Proyecto
            fila[8],  # Tipificación
            fila[9],  # Usuario
            fila[10] # Promoción
           # fila[11]  # Compañía
        ]
        tree.insert("", "end", values=fila_formateada)

    # Crear un menú contextual para el Treeview
    def mostrar_menu(event):
        menu = tk.Menu(ventana_resultados, tearoff=0)
        menu.add_command(label="Copiar fila", command=lambda: copiar_al_portapapeles(tree))
        menu.post(event.x_root, event.y_root)

    # Asociar el menú contextual al Treeview
    tree.bind("<Button-3>", mostrar_menu)

    # Mostrar el Treeview
    tree.pack(expand=True, fill="both")

# Función para mostrar los resultados en un Treeview
def mostrar_resultadosR(resultados, ventana_filtros):
    # Crear un nuevo Toplevel para mostrar los resultados
    ventana_resultados = tk.Toplevel(ventana_filtros)
    ventana_resultados.title("Resultados de la Consulta")
    ventana_resultados.geometry("1000x150")

    # Crear el Treeview para mostrar los resultados
    tree = ttk.Treeview(ventana_resultados, columns=("fecha", "interactionid", "horainicio", "duracion", "tipo", "companytexto", "projecttexto", "Tipificacion", "usuario"), show="headings")

    # Definir las columnas del TreeView
    tree.heading("fecha", text="Fecha")
    tree.heading("interactionid", text="InteractionID")
    #tree.heading("numero", text="Número")
    tree.heading("horainicio", text="Hora Inicio")
    tree.heading("duracion", text="Duración")
    tree.heading("tipo", text="Tipo")
    tree.heading("companytexto", text="Compañía")
    tree.heading("projecttexto", text="Proyecto")
    tree.heading("Tipificacion", text="Tipificación")
    tree.heading("usuario", text="Usuario")
    #tree.heading("PROMOCION", text="Promoción")
    #tree.heading("COMPAÑIA", text="Compañía")

    # Función para convertir datetime a string (formato dd-mm-yyyy)
    def format_fecha(fecha):
        if isinstance(fecha, datetime):
            return fecha.strftime("%d-%m-%Y")  # Formato dd-mm-yyyy
        return fecha

    def format_hora(hora):
        if isinstance(hora, datetime):
            return hora.strftime("%d-%m-%Y %H:%M:%S")  # Formato dd-mm-yyyy HH:MM:SS
        elif isinstance(hora, timedelta):
            return str(hora)  # Si es una duración (timedelta)
        return hora

    # Agregar las filas al Treeview con formato adecuado
    for fila in resultados:
        fila_formateada = [
            format_fecha(fila[0]),  # Formato de la fecha
            fila[1],  # InteractionID
            fila[2],  
            format_hora(fila[3]),  # Hora Inicio formateada
            fila[4],  # Duración
            fila[5],  # Tipo
            fila[6],  # Compañía
            fila[7],  # Proyecto
            fila[8],  # Tipificación
            #fila[9],  # Usuario
            #fila[10] # Promoción
           # fila[11]  # Compañía
        ]
        tree.insert("", "end", values=fila_formateada)

    # Crear un menú contextual para el Treeview
    def mostrar_menu(event):
        menu = tk.Menu(ventana_resultados, tearoff=0)
        menu.add_command(label="Copiar fila", command=lambda: copiar_al_portapapeles(tree))
        menu.post(event.x_root, event.y_root)

    # Asociar el menú contextual al Treeview
    tree.bind("<Button-3>", mostrar_menu)

    # Mostrar el Treeview
    tree.pack(expand=True, fill="both")

# Función para ejecutar la consulta
def ejecutar_queryC(ventana_filtros):
    # Recoger los valores de los filtros
    fecha_inicio = cal_inicio.get_date()
    fecha_fin = cal_fin.get_date()
    project = combo_compania.get()
    duracion = combo_duracion.get()
    tipo_llamada = combo_tipo_llamada.get()
    salienteEntrante = combo_saliEntrante.get()
    usuario = entry_usuario.get()
    agente = entry_agente.get()
    interactionid = entry_interactionid.get()

    # Si no se seleccionan fechas, establecer la fecha actual menos 30 días
    if not fecha_inicio or not fecha_fin:
        fecha_fin = datetime.today().date()
        fecha_inicio = fecha_fin - timedelta(days=15)

    # Validación para asegurar que la fecha de inicio no es posterior a la de fin
    if fecha_inicio > fecha_fin:
        messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin.")
        return

      # Construir la consulta dinámica
    query = """
    SELECT  TOP 1 TR.FECHA, TR.INTERACTIONID, TR.HORAINICIO, TR.DURACION, TR.TIPO, TR.COMPANYTEXTO, TR.PROJECTTEXTO, TR.TIPIFICACION, TR.USUARIO, 
        CASE WHEN VC.PROMOCION IS NULL THEN 'NO VENTA' ELSE VC.PROMOCION END AS PROMOCION, 
        CASE WHEN VC.COMPAÑIA IS NULL THEN 'NO VENTA' ELSE VC.COMPAÑIA END AS COMPAÑIA
    FROM Bases..TransferenciasBuscador TR
    LEFT JOIN Prepago..Ventas_Completo VC 
        ON VC.CELULAR = TR.NUMERO AND VC.NUMEROEMPLEADO = TR.USUARIO
    WHERE TR.FECHA >= :fecha_inicio AND TR.FECHA <= :fecha_fin
    """

   # Diccionario para almacenar los parámetros
    params = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }

    # Añadir filtros adicionales a la consulta
    if project:
        query += " AND TR.COMPANYTEXTO = :project"
        params['project'] = project

    if duracion:
        query += " AND TR.DURACION >= :duracion"
        params['duracion'] = duracion

    if tipo_llamada == "VENTA":
        query += " AND VC.PROMOCION IS NOT NULL AND VC.COMPAÑIA IS NOT NULL"
    elif tipo_llamada == "NO VENTA":
        query += " AND (VC.PROMOCION IS NULL OR VC.COMPAÑIA IS NULL)"

    if usuario:
        query += " AND TR.USUARIO = :usuario"
        params['usuario'] = usuario

    if salienteEntrante:
        query += " AND TR.TIPO = :salienteEntrante"
        params['salienteEntrante'] = salienteEntrante

    if agente:
        query += " AND TR.AGENTE = :agente"
        params['agente'] = agente

    if interactionid:
        query += " AND TR.INTERACTIONID = :interactionid"
        params['interactionid'] = interactionid

    # Ordenar aleatoriamente
    query += " ORDER BY NEWID();"

    # Conectar y ejecutar la consulta con SQLAlchemy
    conexion = create_engine(db_connection_string)

    try:
        with engine.connect() as connection:
        # Ejecutar la consulta con los parámetros usando SQLAlchemy
            result_set = connection.execute(text(query), params)
            resultados = result_set.fetchall()  # Obtener todos los resultados
            mostrar_resultados(resultados, ventana_filtros)  # Mostrar los resultados
            messagebox.showinfo("Resultado", "Consulta ejecutada con éxito.")
    except Exception as e:
        messagebox.showerror("Error de ejecución", f"Error al ejecutar la consulta: {e}")

# Función para ejecutar la consulta
def ejecutar_queryR(ventana_filtros):
    # Recoger los valores de los filtros
    fecha_inicio = cal_inicio.get_date()
    fecha_fin = cal_fin.get_date()
    campanasRcCombo = combo_project.get()
    duracion = combo_duracionR.get()
    tipoR_llamadasCombo = combo_tipo_llamadaR.get()
    #finalizaCombo = combo_saliEntrante.get()
    usuario = entry_usuario.get()
    interactionid = entry_interactionid.get()

    # Si no se seleccionan fechas, establecer la fecha actual menos 30 días
    if not fecha_inicio or not fecha_fin:
        fecha_fin = datetime.today().date()
        fecha_inicio = fecha_fin - timedelta(days=15)

    # Validación para asegurar que la fecha de inicio no es posterior a la de fin
    if fecha_inicio > fecha_fin:
        messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin.")
        return

      # Construir la consulta dinámica
    query = """
    SELECT  TOP 1 TR.FECHA, TR.INTERACTIONID, TR.HORAINICIO, TR.DURACION, TR.TIPO, TR.COMPANYTEXTO, TR.PROJECTTEXTO, TR.TIPIFICACION, TR.USUARIO
    FROM Bases..TransferenciasBuscador TR
    WHERE TR.FECHA >= :fecha_inicio AND TR.FECHA <= :fecha_fin
    """

   # Diccionario para almacenar los parámetros
    params = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }

    # Añadir filtros adicionales a la consulta
    if campanasRcCombo:
        query += " AND TR.PROJECTTEXTO = :campanasRcCombo"
        params['campanasRcCombo'] = campanasRcCombo

    if duracion:
        query += " AND TR.DURACION >= :duracion"
        params['duracion'] = duracion

    if usuario:
        query += " AND TR.USUARIO = :usuario"
        params['usuario'] = usuario

    if interactionid:
        query += " AND TR.INTERACTIONID = :interactionid"
        params['interactionid'] = interactionid

    if tipoR_llamadasCombo:
        query += " AND TR.tipo = :tipoR_llamadasCombo"
        params['tipoR_llamadasCombo'] = tipoR_llamadasCombo 

    # Ordenar aleatoriamente
    query += " ORDER BY NEWID();"

    # Conectar y ejecutar la consulta con SQLAlchemy
    conexion = create_engine(db_connection_string)

    try:
        with engine.connect() as connection:
        # Ejecutar la consulta con los parámetros usando SQLAlchemy
            result_set = connection.execute(text(query), params)
            resultados = result_set.fetchall()  # Obtener todos los resultados
            mostrar_resultadosR(resultados, ventana_filtros)  # Mostrar los resultados
            messagebox.showinfo("Resultado", "Consulta ejecutada con éxito.")
    except Exception as e:
        messagebox.showerror("Error de ejecución", f"Error al ejecutar la consulta: {e}")
    
   # print(query,params)


# Función para mostrar la ventana de filtros
def mostrar_filtrosCantarranas():
    # Crear la ventana para los filtros
    ventana_filtros = tk.Toplevel()
    ventana_filtros.title("Búsqueda de números Cantarranas")
    ventana_filtros.geometry("600x600")
    ventana_filtros.attributes('-alpha', 0.998)  # Fondo translúcido

    canvas = tk.Canvas(ventana_filtros, width=580, height=580, highlightthickness=0)
    canvas.place(x=10, y=10)  # Posición del recuadro en la ventana
    r=20
    # Dibujar un rectángulo con bordes redondeados
    canvas.create_arc((0, 0, r * 2, r * 2), start=90, extent=90, fill="white", outline="white")                   # Esquina superior izquierda
    canvas.create_arc((580 - r * 2, 0, 580, r * 2), start=0, extent=90, fill="white", outline="white")            # Esquina superior derecha
    canvas.create_arc((0, 580 - r * 2, r * 2, 580), start=180, extent=90, fill="white", outline="white")          # Esquina inferior izquierda
    canvas.create_arc((580 - r * 2, 580 - r * 2, 580, 580), start=270, extent=90, fill="white", outline="white")  # Esquina inferior derecha

    # Dibujar las áreas rectangulares entre las esquinas
    canvas.create_rectangle(r, 0, 580 - r, 580, fill="white", outline="white")   # Área horizontal entre las esquinas
    canvas.create_rectangle(0, r, 580, 580 - r, fill="white", outline="white")

    # Posicionar cada widget usando place() para ajuste manual
    tk.Label(ventana_filtros, text="Seleccione las fechas de inicio y fin:",bg='white').place(x=35, y=20)
    
    # Calendario de inicio
    global cal_inicio
    cal_inicio = Calendar(ventana_filtros, selectmode="day", bg= 'white',date_pattern="yyyy-mm-dd")
    cal_inicio.place(x=35, y=50)

    # Calendario de fin
    global cal_fin
    cal_fin = Calendar(ventana_filtros, selectmode="day", bg= 'white', date_pattern="yyyy-mm-dd")
    cal_fin.place(x=320, y=50)

    # Combo de compañía
    tk.Label(ventana_filtros, text="Seleccione la compañía:",bg= 'white').place(x=75, y=250) #Izquierda
    global combo_compania
    combo_compania = ttk.Combobox(ventana_filtros, values=companias)
    combo_compania.place(x=70, y=280)

    # Combo de duración
    tk.Label(ventana_filtros, text="Duración (minutos):",bg= 'white').place(x=380, y=250) #Derecha
    global combo_duracion
    combo_duracion = ttk.Combobox(ventana_filtros, values=duraciones,)
    combo_duracion.place(x=370, y=280)

    # Combo de tipo de llamada
    tk.Label(ventana_filtros, text="Tipo de llamada:", bg= 'white').place(x=75, y=320) #Izquierda
    global combo_tipo_llamada
    combo_tipo_llamada = ttk.Combobox(ventana_filtros, values=tipos_llamada,)
    combo_tipo_llamada.place(x=70, y=350)

    # Combo de tipo de llamada entrante o saliente
    tk.Label(ventana_filtros, text="Entrante o Saliente:",bg= 'white').place(x=390, y=320) #Derecha
    global combo_saliEntrante
    combo_saliEntrante = ttk.Combobox(ventana_filtros, values=saliEntrante)
    combo_saliEntrante.place(x=370, y=350)

    # Entradas de usuario, agente e interactionid
    tk.Label(ventana_filtros, text="Usuario:", bg= 'white').place(x=115, y=390)
    global entry_usuario
    entry_usuario = ttk.Entry(ventana_filtros)
    entry_usuario.place(x=80, y=420)

    tk.Label(ventana_filtros, text="Agente:", bg= 'white').place(x=420, y=390)
    global entry_agente
    entry_agente = ttk.Entry(ventana_filtros)
    entry_agente.place(x=380, y=420)

    tk.Label(ventana_filtros, text="Interaction ID:", bg= 'white').place(x=100, y=460)
    global entry_interactionid
    entry_interactionid = ttk.Entry(ventana_filtros)
    entry_interactionid.place(x=80, y=490)

    # Botón de ejecutar consulta
    #btn_ejecutar = tk.Button(ventana_filtros, text="Ejecutar consulta", command=lambda: ejecutar_query(ventana_filtros))
    #btn_ejecutar.place(x=250, y=500)

    global imagen_originalAceptar
    imagen_originalAceptar = Image.open(mainimagen_aceptar)  
    global imagen_redimensionadaAceptar
    imagen_redimensionadaAceptar = imagen_originalAceptar.resize((120, 40))
    global imagen_Aceptar
    imagen_Aceptar = ImageTk.PhotoImage(imagen_redimensionadaAceptar)

    btn_filtrosAceptar = tk.Button(
        ventana_filtros,
        image=imagen_Aceptar,             # Asigna la imagen PNG
        command=lambda:ejecutar_queryC(ventana_filtros),              
        bg="white",                       # Fondo del botón que iguale el borde si no es transparente
        relief="flat",                        # Tipo de borde para minimizar el marco
        compound="center"                     # Centra la imagen en el botón
    )
    btn_filtrosAceptar.place(x=380, y=470) 


def mostrar_filtrosReforma():
    # Crear la ventana para los filtros
    ventana_filtros = tk.Toplevel()
    ventana_filtros.title("Búsqueda de números Reforma")
    ventana_filtros.geometry("600x600")
    ventana_filtros.attributes('-alpha', 0.998)  # Fondo translúcido

    canvas = tk.Canvas(ventana_filtros, width=580, height=580, highlightthickness=0)
    canvas.place(x=10, y=10)  # Posición del recuadro en la ventana
    r=20
    # Dibujar un rectángulo con bordes redondeados
    canvas.create_arc((0, 0, r * 2, r * 2), start=90, extent=90, fill="white", outline="white")                   # Esquina superior izquierda
    canvas.create_arc((580 - r * 2, 0, 580, r * 2), start=0, extent=90, fill="white", outline="white")            # Esquina superior derecha
    canvas.create_arc((0, 580 - r * 2, r * 2, 580), start=180, extent=90, fill="white", outline="white")          # Esquina inferior izquierda
    canvas.create_arc((580 - r * 2, 580 - r * 2, 580, 580), start=270, extent=90, fill="white", outline="white")  # Esquina inferior derecha

    # Dibujar las áreas rectangulares entre las esquinas
    canvas.create_rectangle(r, 0, 580 - r, 580, fill="white", outline="white")   # Área horizontal entre las esquinas
    canvas.create_rectangle(0, r, 580, 580 - r, fill="white", outline="white")

    # Posicionar cada widget usando place() para ajuste manual
    tk.Label(ventana_filtros, text="Seleccione las fechas de inicio y fin:",bg='white').place(x=35, y=20)
    
    # Calendario de inicio
    global cal_inicio
    cal_inicio = Calendar(ventana_filtros, selectmode="day", bg= 'white',date_pattern="yyyy-mm-dd")
    cal_inicio.place(x=35, y=50)

    # Calendario de fin
    global cal_fin
    cal_fin = Calendar(ventana_filtros, selectmode="day", bg= 'white', date_pattern="yyyy-mm-dd")
    cal_fin.place(x=320, y=50)

    # Combo de project
    tk.Label(ventana_filtros, text="Seleccione la campaña:",bg= 'white').place(x=75, y=250) #Izquierda
    global combo_project
    combo_project = ttk.Combobox(ventana_filtros, values=campañasR)
    combo_project.place(x=70, y=280)

    # Combo de duración
    tk.Label(ventana_filtros, text="Duración (minutos):",bg= 'white').place(x=380, y=250) #Derecha
    global combo_duracionR
    combo_duracionR = ttk.Combobox(ventana_filtros, values=duracionesR,)
    combo_duracionR.place(x=370, y=280)

    # Combo de tipo de llamada
    tk.Label(ventana_filtros, text="Tipo de llamada:", bg= 'white').place(x=85, y=320) #Izquierda
    global combo_tipo_llamadaR
    combo_tipo_llamadaR = ttk.Combobox(ventana_filtros, values=tipoR_llamadas,)
    combo_tipo_llamadaR.place(x=70, y=350)

    # Entradas de usuario, agente e interactionid
    tk.Label(ventana_filtros, text="Numero de Empleado:", bg= 'white').place(x=85, y=390)
    global entry_usuario
    entry_usuario = ttk.Entry(ventana_filtros)
    entry_usuario.place(x=80, y=420)

    #k.Label(ventana_filtros, text="Nombre Colaborador:", bg= 'white').place(x=380, y=390)
    #global entry_agente
    #entry_agente = ttk.Entry(ventana_filtros)
    #entry_agente.place(x=380, y=420)

    tk.Label(ventana_filtros, text="Interaction ID:", bg= 'white').place(x=100, y=460)
    global entry_interactionid
    entry_interactionid = ttk.Entry(ventana_filtros)
    entry_interactionid.place(x=80, y=490)
    
    global imagen_originalAceptar
    imagen_originalAceptar = Image.open(mainimagen_aceptar)  
    global imagen_redimensionadaAceptar
    imagen_redimensionadaAceptar = imagen_originalAceptar.resize((120, 40))
    global imagen_Aceptar
    imagen_Aceptar = ImageTk.PhotoImage(imagen_redimensionadaAceptar)

    btn_filtrosAceptar = tk.Button(
        ventana_filtros,
        image=imagen_Aceptar,             # Asigna la imagen PNG
        command=lambda:ejecutar_queryR(ventana_filtros),              
        bg="white",                       # Fondo del botón que iguale el borde si no es transparente
        relief="flat",                        # Tipo de borde para minimizar el marco
        compound="center"                     # Centra la imagen en el botón
    )
    btn_filtrosAceptar.place(x=380, y=470) 

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Selección de site")
ventana_principal.geometry("300x200")
ventana_principal.attributes('-alpha', 0.998) 
#ventana_principal.configure(bg='gray')

canvas = tk.Canvas(ventana_principal, width=280, height=180, highlightthickness=0)
canvas.place(x=10, y=10)  # Posición del recuadro en la ventana

r=20
# Dibujar un rectángulo con bordes redondeados
canvas.create_arc((0, 0, r * 2, r * 2), start=90, extent=90, fill="white", outline="white")                   # Esquina superior izquierda
canvas.create_arc((280 - r * 2, 0, 280, r * 2), start=0, extent=90, fill="white", outline="white")            # Esquina superior derecha
canvas.create_arc((0, 180 - r * 2, r * 2, 180), start=180, extent=90, fill="white", outline="white")          # Esquina inferior izquierda
canvas.create_arc((280 - r * 2, 180 - r * 2, 280, 180), start=270, extent=90, fill="white", outline="white")  # Esquina inferior derecha

# Dibujar las áreas rectangulares entre las esquinas
canvas.create_rectangle(r, 0, 280 - r, 180, fill="white", outline="white")   # Área horizontal entre las esquinas
canvas.create_rectangle(0, r, 280, 180 - r, fill="white", outline="white")

imagen_originalCanta = Image.open(mainimagen_canta)
imagen_redimensionadaCanta = imagen_originalCanta.resize((120, 40))
imagen_cantarranas = ImageTk.PhotoImage(imagen_redimensionadaCanta)

imagen_originalReforma = Image.open(mainimagen_reforma)
imagen_redimensionadaReforma = imagen_originalReforma.resize((120, 40))
imagen_Reforma = ImageTk.PhotoImage(imagen_redimensionadaReforma)

btn_filtrosCanta = tk.Button(
    ventana_principal,
    image=imagen_cantarranas,             # Asigna la imagen PNG
    command=mostrar_filtrosCantarranas,              
    bg="white",                       # Fondo del botón que iguale el borde si no es transparente
    relief="flat",                        # Tipo de borde para minimizar el marco
    compound="center"                     # Centra la imagen en el botón
)
btn_filtrosCanta.place(x=90, y=50) 


btn_filtrosReforma = tk.Button(
    ventana_principal,
    image=imagen_Reforma,             # Asigna la imagen PNG
    command=mostrar_filtrosReforma,              
    bg="white",                       # Fondo del botón que iguale el borde si no es transparente
    relief="flat",                        # Tipo de borde para minimizar el marco
    compound="center"                     # Centra la imagen en el botón
)
btn_filtrosReforma.place(x=90, y=105) 

ventana_principal.mainloop()

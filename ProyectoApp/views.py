from django.shortcuts import render, HttpResponse
from datetime import datetime, timedelta
from getpass import getuser
from ProyectoApp.models import static_panel, dinamic_panel
from ProyectoApp.data import data
from decouple import config
import psycopg2
import os
import pandas as pd
import matplotlib.pyplot as plt
from django.core.paginator import Paginator
import random
import time

# Vista de pagina resumen
def home(request):

    # Obtencion de promedios, desviaciones y generacion de grafica de ultimas 24h
    media_intensidad, media_medicion, media_corriente, std_intensidad, std_medicion, std_corriente = data()
    generate_image()
    imagen = 'static/ProyectoApp/plots/mi_grafico.png'
    media_voltajelive = comprobar_en_vivo()

    # Obtencion de ultimos datos
    entradas = static_panel.objects.all()
    ultima_entrada=[]
    if len(entradas)>1:
        for i in range(len(entradas)-1, len(entradas)):
            ultima_entrada.append(entradas[i])

    ultimo_elemento = ultima_entrada[0]
    ultima_hora = ultimo_elemento.date

    ################################################    
    # datos()
    #################################################

    # Obtencion de datos de usuario y generacion de mensaje
    username = getuser()
    hora = datetime.now()
    fecha = datetime.today()

    if(0<=hora.hour<12):
        mensaje_hora = "Buenos días"
    elif (12<=hora.hour<18):
        mensaje_hora = "Buenas tardes"
    elif (18<=hora.hour<24):
        mensaje_hora = "Buenas noches"


    return render(request, "ProyectoApp/template/index.html",{
        "mensaje_hora": mensaje_hora,
        "username": username,
        "fecha": fecha,
        "imagen": imagen,
        "ultima_lectura":ultimo_elemento.measurement,
        "ultima_hora": ultima_hora,
        "media_intensidad":media_intensidad,
        "media_medicion":media_medicion,
        "media_corriente": media_corriente,
        "std_intensidad": std_intensidad,
        "std_medicion": std_medicion,
        "std_corriente": std_corriente,
        "media_voltajelive": media_voltajelive,
    })

# Vista de pagina stream
def graph_live(request):

    # Obtencion de promedios, desviaciones y generacion de grafica de ultimas 24h
    media_voltaje, media_intensidad, media_corriente = generate_image4()
    imagen = 'static/ProyectoApp/plots/mi_grafico_live.png'
    media_voltajelive = comprobar_en_vivo()

    # Obtencion de datos de usuario y generacion de mensaje
    username = getuser()
    hora = datetime.now()
    fecha = datetime.today()

    if(0<=hora.hour<12):
        mensaje_hora = "Buenos días"
    elif (12<=hora.hour<18):
        mensaje_hora = "Buenas tardes"
    elif (18<=hora.hour<24):
        mensaje_hora = "Buenas noches"

    return render(request, "ProyectoApp/template/live.html",{
        "mensaje_hora": mensaje_hora,
        "username": username,
        "fecha": fecha,
        "imagen": imagen,
        "media_voltaje": media_voltaje,
        "media_intensidad": media_intensidad,
        "media_corriente": media_corriente,
        "media_voltajelive":media_voltajelive,
    })

# Vista de pagina estadisticas estatico
def graph_history(request):

    media_voltaje, media_intensidad, media_corriente = generate_image2()
    imagen = 'static/ProyectoApp/plots/mi_grafico2.png'

    # obtener todos los registros de la tabla StaticPanel
    static_panel_data = static_panel.objects.all().values('id', 'date', 'measurement', 'intensity', 'current')
    # crear un dataframe de pandas con los datos obtenidos
    df = pd.DataFrame.from_records(static_panel_data)
    # formatear la columna 'date' en formato día/mes/año hora:minutos
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%d/%m/%Y %H:%M')
    # crear un objeto Paginator con los datos del dataframe
    paginator = Paginator(df.values.tolist(), 10)
    # obtener la página solicitada por el usuario
    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
    except:
        page_data = paginator.page(1)


    username = getuser()
    hora = datetime.now()
    fecha = datetime.today()

    if(0<=hora.hour<12):
        mensaje_hora = "Buenos días"
    elif (12<=hora.hour<18):
        mensaje_hora = "Buenas tardes"
    elif (18<=hora.hour<24):
        mensaje_hora = "Buenas noches"

    return render(request, "ProyectoApp/template/history.html", {
        "mensaje_hora": mensaje_hora,
        "username": username,
        "fecha": fecha,
        "page_data": page_data,
        "imagen": imagen,
        "media_voltaje": media_voltaje,
        "media_intensidad": media_intensidad,
        "media_corriente": media_corriente,
        })

# Vista de pagina estadisticas dinamico
def graph_history2(request):

    media_voltaje, media_corriente = generate_image3()
    imagen = 'static/ProyectoApp/plots/mi_grafico3.png'

    static_panel_data = dinamic_panel.objects.all().values('id', 'date', 'measurement', 'intensity1', 'intensity2', 'intensity3', 'intensity4', 'intensity5', 'intensity6', 'intensity7', 'intensity8', 'intensity9', 'current')
    # crear un dataframe de pandas con los datos obtenidos
    df = pd.DataFrame.from_records(static_panel_data)
    # crear un objeto Paginator con los datos del dataframe
    paginator = Paginator(df.values.tolist(), 10)
    # obtener la página solicitada por el usuario
    page = request.GET.get('page')
    try:
        page_data = paginator.page(page)
    except:
        page_data = paginator.page(1)

    
    username = getuser()
    hora = datetime.now()
    fecha = datetime.today()

    if(0<=hora.hour<12):
        mensaje_hora = "Buenos días"
    elif (12<=hora.hour<18):
        mensaje_hora = "Buenas tardes"
    elif (18<=hora.hour<24):
        mensaje_hora = "Buenas noches"
    return render(request, "ProyectoApp/template/history2.html",{
        "mensaje_hora": mensaje_hora,
        "username": username,
        "fecha": fecha,
        "page_data": page_data,
        "imagen": imagen,
        "media_voltaje": media_voltaje,
        "media_corriente": media_corriente,
        })

# Vista de pagina de informacion
def info(request):
    
    return render(request, "ProyectoApp/template/info.html",{})

# Generacion de datos aleatorios
def Voltaje():

    Voltaje = random.randint(1,5)

    return Voltaje

def Intensidad():

    Intensidad = random.randint(1,15)

    return Intensidad

def generador_datos(Volt, Inten, Cu):

     nuevo_registro = static_panel(measurement=Volt, intensity=Inten, current=Cu)
     nuevo_registro.save()     

def generador_datos2(Volt, Inten1, Inten2, Inten3, Inten4, Inten5, Inten6, Inten7, Inten8, Inten9, current):

     nuevo_registro = dinamic_panel(measurement=Volt, intensity1=Inten1, intensity2=Inten2, intensity3=Inten3, intensity4=Inten4, intensity5=Inten5, intensity6=Inten6, intensity7=Inten7, intensity8=Inten8, intensity9=Inten9, current=current )
     nuevo_registro.save()        

def datos():
    for i in range(5):
            Volt = Voltaje()
            Inten = Intensidad()
            Cu = Voltaje()
            generador_datos(Volt, Inten, Cu)
            time.sleep(10)

def datos2():
    for i in range(5):
            Volt = Voltaje()
            Inten1 = Intensidad()
            Inten2 = Intensidad()
            Inten3 = Intensidad()
            Inten4 = Intensidad()
            Inten5 = Intensidad()
            Inten6 = Intensidad()
            Inten7 = Intensidad()
            Inten8 = Intensidad()
            Inten9 = Intensidad()
            Cu = Voltaje()
            generador_datos2(Volt, Inten1, Inten2, Inten3, Inten4, Inten5, Inten6, Inten7, Inten8, Inten9, Cu)
            time.sleep(10)

# Generacion de imagen de resumen (ultimas 24h)
def generate_image():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Consulta SQL para obtener los datos
    consulta = 'SELECT date, measurement, intensity, current FROM "ProyectoApp_static_panel" WHERE CAST(date AS DATE) = CURRENT_DATE;'

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    # Convertir la columna 'date' a formato de fecha
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.strftime('%H:%M:%S')

    # Obtener los puntos máximos de cada curva
    max_measurement_idx = df.groupby('intensity')['measurement'].idxmax()
    max_measurement = df.loc[max_measurement_idx, ['date', 'measurement', 'intensity']]
    max_intensity_idx = df.groupby('measurement')['intensity'].idxmax()
    max_intensity = df.loc[max_intensity_idx, ['date', 'measurement', 'intensity']]

    # Graficar los datos
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['measurement'], label='Voltaje')
    plt.plot(df['time'], df['intensity'], label='Intensidad')
    plt.plot(df['time'], df['current'], label='Corriente')
    plt.xlabel('Fecha')
    plt.ylabel('Voltaje/Intensidad/Corriente')
    plt.title('Registro de Medición e Intensidad de hoy')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    ruta_archivo = 'C:/Users/asana/Desktop/Proyecto_E6/ProyectoApp/static/ProyectoApp/plots/mi_grafico.png'

    # Verificar si el archivo ya existe
    if os.path.isfile(ruta_archivo):
        # Si el archivo existe, eliminarlo
        os.remove(ruta_archivo)

    # Guardar el gráfico en un archivo
    plt.savefig(ruta_archivo)

# Generacion de imagen de estadisticas estaticas (1h)
def generate_image2():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Obtener la hora actual
    now = datetime.now()

    # Restar una hora a la hora actual para obtener la hora hace una hora
    one_hour_ago = now - timedelta(hours=1)

    # Formatear las fechas para usarlas en la consulta SQL
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago_formatted = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Consulta SQL para obtener los datos de la última hora
    consulta = f'SELECT date, measurement, intensity, current FROM "ProyectoApp_static_panel" WHERE date BETWEEN \'{one_hour_ago_formatted}\' AND \'{now_formatted}\';'

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    media_voltaje = df["measurement"].mean()
    media_intensidad = df["intensity"].mean()
    media_corriente = df["current"].mean()

    # Convertir la columna 'date' a formato de fecha
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.strftime('%H:%M:%S')
    
    # Graficar los datos
    plt.figure(figsize=(7, 7))
    plt.plot(df['time'], df['measurement'], label='Voltaje')
    plt.plot(df['time'], df['intensity'], label='Intensidad')
    plt.plot(df['time'], df['current'], label='Corriente')
    plt.ylabel('Voltaje/Intensidad/Corriente')
    plt.title('Registro de Medición e Intensidad')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    ruta_archivo = 'C:/Users/asana/Desktop/Proyecto_E6/ProyectoApp/static/ProyectoApp/plots/mi_grafico2.png'

    # Verificar si el archivo ya existe
    if os.path.isfile(ruta_archivo):
        # Si el archivo existe, eliminarlo
        os.remove(ruta_archivo)

    # Guardar el gráfico en un archivo
    plt.savefig(ruta_archivo)

    return (media_voltaje, media_intensidad, media_corriente)
    
# Generacion de imagen de estadisticas dinamica (1h)
def generate_image3():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Obtener la hora actual
    now = datetime.now()

    # Restar una hora a la hora actual para obtener la hora hace una hora
    one_hour_ago = now - timedelta(hours=1)

    # Formatear las fechas para usarlas en la consulta SQL
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago_formatted = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Consulta SQL para obtener los datos de la última hora
    consulta = f'SELECT measurement, intensity1, intensity2, intensity3, intensity4, intensity5, intensity6, intensity7, intensity8, intensity9, current FROM "ProyectoApp_dinamic_panel" WHERE date BETWEEN \'{one_hour_ago_formatted}\' AND \'{now_formatted}\';'
    # print(consulta)

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    media_voltaje = df["measurement"].mean()
    media_intensidad1 = df["intensity1"].mean()
    media_intensidad2 = df["intensity2"].mean()
    media_intensidad3 = df["intensity3"].mean()
    media_intensidad4 = df["intensity4"].mean()
    media_intensidad5 = df["intensity5"].mean()
    media_intensidad6 = df["intensity6"].mean()
    media_intensidad7 = df["intensity7"].mean()
    media_intensidad8 = df["intensity8"].mean()
    media_intensidad9 = df["intensity9"].mean()
    media_corriente = df["current"].mean()

    x = ['Voltaje', 'Intensidad 1', 'Intensidad 2', 'Intensidad 3', 'Intensidad 4', 'Intensidad 5', 'Intensidad 6', 'Intensidad 7', 'Intensidad 8', 'Intensidad 9', 'Corriente']
    y = [media_voltaje, media_intensidad1, media_intensidad2, media_intensidad3, media_intensidad4, media_intensidad5, media_intensidad6, media_intensidad7, media_intensidad8, media_intensidad9, media_corriente]
    colores = ['#173541', '#1E4554', '#245467', '#2A647B', '#30748E', '#3684A2', '#3C93B5', '#47A1C3', '#5AABCA', '#6DB5D1', '#6DB5D1']

    fig, ax = plt.subplots(figsize=(7, 7))
    # Crear el gráfico de barras
    bars = ax.bar(x, y, color=colores)

    ax.set_xlabel('Nombre de medición')
    ax.set_ylabel('Valor promedio')
    ax.set_title('Valores promedio de mediciones')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(f"{height:.2f}"), ha='center', va='bottom')

    plt.xticks(rotation=45)

    ruta_archivo = 'C:/Users/asana/Desktop/Proyecto_E6/ProyectoApp/static/ProyectoApp/plots/mi_grafico3.png'

    # Verificar si el archivo ya existe
    if os.path.isfile(ruta_archivo):
        # Si el archivo existe, eliminarlo
        os.remove(ruta_archivo)

    # Guardar el gráfico en un archivo
    plt.savefig(ruta_archivo)

    return (media_voltaje, media_corriente)

# Generacion de imagen de stream (5m)
def generate_image4():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Obtener la hora actual
    now = datetime.now()

    # Restar una hora a la hora actual para obtener la hora hace una hora
    one_hour_ago = now - timedelta(hours=0.083)

    # Formatear las fechas para usarlas en la consulta SQL
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago_formatted = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Consulta SQL para obtener los datos de la última hora
    consulta = f'SELECT date, measurement, intensity, current FROM "ProyectoApp_static_panel" WHERE date BETWEEN \'{one_hour_ago_formatted}\' AND \'{now_formatted}\';'

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    media_voltaje = df["measurement"].mean()
    media_intensidad = df["intensity"].mean()
    media_corriente = df["current"].mean()

    # Convertir la columna 'date' a formato de fecha
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['date'].dt.strftime('%H:%M:%S')

    # Obtener los puntos máximos de cada curva
    max_measurement_idx = df.groupby('intensity')['measurement'].idxmax()
    max_measurement = df.loc[max_measurement_idx, ['date', 'measurement', 'intensity']]
    max_intensity_idx = df.groupby('measurement')['intensity'].idxmax()
    max_intensity = df.loc[max_intensity_idx, ['date', 'measurement', 'intensity']]

    # Graficar los datos
    plt.figure(figsize=(12, 7))
    plt.plot(df['time'], df['measurement'], label='Voltaje')
    plt.plot(df['time'], df['intensity'], label='Intensidad')
    plt.plot(df['time'], df['current'], label='Corriente')
    plt.xlabel('Fecha')
    plt.ylabel('Voltaje/Intensidad/Corriente')
    plt.title('Registro de Medición e Intensidad')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    ruta_archivo = 'C:/Users/asana/Desktop/Proyecto_E6/ProyectoApp/static/ProyectoApp/plots/mi_grafico_live.png'

    # Verificar si el archivo ya existe
    if os.path.isfile(ruta_archivo):
        # Si el archivo existe, eliminarlo
        os.remove(ruta_archivo)

    # Guardar el gráfico en un archivo
    plt.savefig(ruta_archivo)

    return (media_voltaje, media_intensidad, media_corriente)

# Comprobacion de ingreso de datos en ultimo 3m
def comprobar_en_vivo():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
            dbname= config('DB_NAME'),
            user= config('DB_USER'),
            password= config('DB_PASSWORD'),
            host= config('DB_HOST'),
            port= config('DB_PORT'),
        )

    # Obtener la hora actual
    now = datetime.now()

    # Restar una hora a la hora actual para obtener la hora hace una hora
    one_hour_ago = now - timedelta(hours=.05)

    # Formatear las fechas para usarlas en la consulta SQL
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_ago_formatted = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    # Consulta SQL para obtener los datos de la última hora
    consulta = f'SELECT date, measurement FROM "ProyectoApp_static_panel" WHERE date BETWEEN \'{one_hour_ago_formatted}\' AND \'{now_formatted}\';'
    print(consulta)

    # Leer los datos en un DataFrame de Pandas
    df = pd.read_sql(consulta, conn)

    # Cerrar la conexión con la base de datos
    conn.close()

    media_voltaje = df["measurement"].mean()

    return (media_voltaje)  
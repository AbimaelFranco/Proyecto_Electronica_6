import pandas as pd
import psycopg2
from decouple import config


def data():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
        # dbname="proyecto_electronica_6",
        # user="postgres",
        # password="Km2_R#%Si",
        # host="localhost",
        # port="5432"
        dbname= config('DB_NAME'),
        user= config('DB_USER'),
        password= config('DB_PASSWORD'),
        host= config('DB_HOST'),
        port= config('DB_PORT'),
    )

    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()

    # Consulta SQL para obtener los datos de interés de la tabla en PostgreSQL
    consulta = 'SELECT id, measurement, intensity, current FROM "ProyectoApp_static_panel";'

    # Ejecutar la consulta y obtener los resultados
    cursor.execute(consulta)
    rows = cursor.fetchall()

    # Crear un DataFrame de Pandas con los resultados obtenidos
    df = pd.DataFrame(rows, columns=["id", "medicion", "intensity", "current"])

    # Realizar análisis de datos con Pandas
    # Por ejemplo, obtener información estadística básica del DataFrame
    # print("Estadísticas básicas del DataFrame:")
    # print(df.describe())

    # Calcular la media de la columna "intensidad"
    media_intensidad = df["intensity"].mean()
    # print(f"Media de intensidad: {media_intensidad}")

    # Calcular la mediana de la columna "intensidad"
    std_intensidad = df["intensity"].std()
    # print(f"Mediana de intensidad: {mediana_intensidad}")

    # Calcular la media de la columna "measurement"
    media_medicion = df["medicion"].mean()
    # print(f"Media de medicion: {media_medicion}")

    # Calcular la moda de la columna "measurement"
    std_medicion = df["medicion"].std()
    # print(f"Moda de medicion: {moda_medicion}")

    # Calcular la media de la columna "current"
    media_corriente = df["current"].mean()
    # print(f"Media de corriente: {media_corriente}")

    # Calcular la moda de la columna "current"
    std_corriente = df["current"].std()
    # print(f"Moda de corriente: {moda_corriente}")

    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()

    return (media_intensidad, media_medicion, media_corriente, std_intensidad, std_medicion, std_corriente)
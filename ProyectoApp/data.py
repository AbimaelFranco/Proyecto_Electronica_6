import pandas as pd
import psycopg2

def data():
    # Establecer la conexión con la base de datos en PostgreSQL
    conn = psycopg2.connect(
        dbname="proyecto_electronica_6",
        user="postgres",
        password="Km2_R#%Si",
        host="localhost",
        port="5432"
    )

            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # 'NAME': 'proyecto_electronica_6',
            # 'USER': 'postgres',
            # 'PASSWORD': 'It@lia2001',
            # 'HOST': '127.0.0.1',
            # 'PORT': '5432',

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
    print("Estadísticas básicas del DataFrame:")
    print(df.describe())

    # Calcular la media de la columna "intensidad"
    media_intensidad = df["intensity"].mean()
    print(f"Media de intensidad: {media_intensidad}")

    # Calcular la mediana de la columna "intensidad"
    mediana_intensidad = df["intensity"].median()
    print(f"Mediana de intensidad: {mediana_intensidad}")

    # Calcular la media de la columna "measurement"
    media_medicion = df["medicion"].mean()
    print(f"Media de medicion: {media_medicion}")

    # Calcular la moda de la columna "measurement"
    moda_medicion = df["medicion"].mode().values[0]
    print(f"Moda de medicion: {moda_medicion}")

    # Calcular la media de la columna "current"
    media_corriente = df["current"].mean()
    print(f"Media de corriente: {media_corriente}")

    # Calcular la moda de la columna "current"
    moda_corriente = df["current"].mode().values[0]
    print(f"Moda de corriente: {moda_corriente}")

    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()

    return (media_intensidad, media_medicion, media_corriente)

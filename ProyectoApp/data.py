import pandas as pd
import psycopg2

# Establecer la conexión con la base de datos en PostgreSQL
conn = psycopg2.connect(
    dbname="proyecto_electronica_6",
    user="postgres",
    password="It@lia2001",
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
consulta = 'SELECT id, measurement, intensity FROM "ProyectoApp_static_panel";'

# Ejecutar la consulta y obtener los resultados
cursor.execute(consulta)
rows = cursor.fetchall()

# Crear un DataFrame de Pandas con los resultados obtenidos
df = pd.DataFrame(rows, columns=["id", "medicion", "intensity"])

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

# # Calcular la moda de la columna "medicion"
moda_medicion = df["measurement"].mode().values[0]
print(f"Moda de medicion: {moda_medicion}")

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()

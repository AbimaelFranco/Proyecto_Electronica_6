import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from decouple import config


# Establecer la conexión con la base de datos en PostgreSQL
conn = psycopg2.connect(
    dbname= config('DB_NAME'),
    user= config('DB_USER'),
    password= config('DB_PASSWORD'),
    host= config('DB_HOST'),
    port= config('DB_PORT'),
)

# Consulta SQL para obtener los datos
consulta = 'SELECT date, measurement FROM "ProyectoApp_static_panel";'

# Leer los datos en un DataFrame de Pandas
df = pd.read_sql(consulta, conn)

# Cerrar la conexión con la base de datos
conn.close()

# Convertir la columna 'date' a formato de fecha
df['date'] = pd.to_datetime(df['date'])

# Graficar los datos
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['measurement'])
plt.xlabel('Fecha')
plt.ylabel('Medición')
plt.title('Gráfico de Medición vs Fecha')
plt.xticks(rotation=45)
plt.show()
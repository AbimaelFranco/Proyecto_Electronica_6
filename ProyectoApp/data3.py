import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Establecer la conexión con la base de datos en PostgreSQL
conn = psycopg2.connect(
    dbname="proyecto_electronica_6",
    user="postgres",
    password="It@lia2001",
    host="127.0.0.1",
    port="5432"
)

# Consulta SQL para obtener los datos
consulta = 'SELECT date, measurement, intensity FROM "ProyectoApp_static_panel";'

# Leer los datos en un DataFrame de Pandas
df = pd.read_sql(consulta, conn)

# Cerrar la conexión con la base de datos
conn.close()

# Convertir la columna 'date' a formato de fecha
df['date'] = pd.to_datetime(df['date'])

# Obtener los puntos máximos de cada curva
max_measurement_idx = df.groupby('intensity')['measurement'].idxmax()
max_measurement = df.loc[max_measurement_idx, ['date', 'measurement', 'intensity']]
max_intensity_idx = df.groupby('measurement')['intensity'].idxmax()
max_intensity = df.loc[max_intensity_idx, ['date', 'measurement', 'intensity']]

# Graficar los datos
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['measurement'], label='Measurement')
plt.plot(df['date'], df['intensity'], label='Intensity')
plt.scatter(max_measurement['date'], max_measurement['measurement'], color='red', label='Puntos máximos de Measurement')
plt.scatter(max_intensity['date'], max_intensity['intensity'], color='green', label='Puntos máximos de Intensity')
plt.xlabel('Fecha')
plt.ylabel('Medición/Intensidad')
plt.title('Gráfico de Medición e Intensidad vs Fecha')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()
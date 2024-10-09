import contextily as cx
import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from geodatasets import get_path
from env import API_KEY

# Declarar la fecha
date = '2024-10-09'
days_rate = 1
filter_hour = '510'

# Cargar los datos
df = pd.read_csv(f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/VIIRS_NOAA20_NRT/ARG/{days_rate}/{date}')

# Filtrar los datos por la hora deseada (dentro de la hora especificada)
df = df[df['acq_time'].astype(str).str.startswith(filter_hour)]

# Imprimir información sobre los datos
print(f"Número total de puntos de incendio: {len(df)}")

if len(df) == 0:
    print("No hay datos de incendios para el período solicitado.")
    exit()

print(f"Rango de latitudes: {df['latitude'].min()} a {df['latitude'].max()}")
print(f"Rango de longitudes: {df['longitude'].min()} a {df['longitude'].max()}")

# Establecer los datos de incendios para Argentina
df['acq_datetime'] = pd.to_datetime(df['acq_date'] + ' ' + df['acq_time'].astype(str).str.zfill(4), format='%Y-%m-%d %H%M')
gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
)

# Establecer el mapa
extent = [-75, -55, -53, -21]  # Ajustado para Argentina
world = geopandas.read_file(get_path("naturalearth.land"))
ax = world.plot(figsize=(12, 15), alpha=0)

ax.set_xlim([extent[0], extent[2]])
ax.set_ylim([extent[1], extent[3]])

ax.set(title=f'Incendios en Argentina fecha:{date} periodo:{days_rate} días hora:{filter_hour}')
ax.set_axis_off()

# Dibujar todos los puntos en rojo
gdf.plot(ax=ax, color="red", markersize=5)

cx.add_basemap(ax, crs=gdf.crs, source=cx.providers.OpenStreetMap.Mapnik)

plt.tight_layout()
plt.show()
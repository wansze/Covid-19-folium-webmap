import pandas as pd
import requests
import folium

# Creating a base map (other style:  tiles = 'cartodbpositron')
map = folium.Map(location = [51.50,-0.1276], tiles="OpenStreetMap", zoom_start = 5, max_bounds=True, min_zoom=2)
map.save("BaseMap.html")

# Pull the data from corona-api
res = requests.get('https://corona-api.com/countries')
covid_current = res.json()

# Creating the covid-19 dataframe
df = []
covid_data = covid_current['data']

for country in covid_data:
    df.append([country['name'],
               country['latest_data']['confirmed']])

df_covid = pd.DataFrame(df, columns = ['Country', 'Total Cases'])

# Replacing country names to match Folium
df_covid.replace('UK', 'United Kingdom', inplace = True)
df_covid.replace('Congo', "Republic of the Congo", inplace = True)
df_covid.replace('Tanzania', "United Republic of Tanzania", inplace = True)
df_covid.replace('USA', "United States of America", inplace = True)
df_covid.replace('Tanzania', "United Republic of Tanzania", inplace = True)
df_covid.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace = True)
df_covid.replace('Congo', "Republic of the Congo", inplace = True)
df_covid.replace('Serbia', "Republic of Serbia", inplace = True)
df_covid.replace('Czechia', "Czech Republic", inplace = True)

url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'

# Adding the chloropleth layer onto the base map
folium.Choropleth(
   geo_data=country_shapes,
    name='choropleth',
    data=df_covid,
    columns=['Country', 'Total Cases'],
    key_on='feature.properties.name',
    fill_color='PuRd',
    nan_fill_color='white'
).add_to(map)

# Adding an interactive drop pin indicating the country's name
# Coordinates data obtained from countries.txt file 
df_coords = pd.read_csv('countries.txt')

for latitude, longitude, name in zip(df_coords['latitude'], df_coords['longitude'], df_coords['name']):

    # Creating the marker
    folium.Marker(
        location = [latitude, longitude], 
        popup = name,
        icon = folium.DivIcon(html=f"""<div style="font-family: courier new; color:blue">{name}</div>""")
            ).add_to(map)

map.save("BaseMap.html")
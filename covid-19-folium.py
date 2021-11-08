import pandas as pd
import requests
import folium

# creating a base map
map = folium.Map(location = [51.50,-0.1276], zoom_start = 12)
map.save("BaseMap.html")


res = requests.get('https://corona-api.com/countries')
covid_current = res.json()


df = []
for country in covid_current['data']:
    df.append([country['name'],
               country['latest_data']['confirmed']])

df_covid = pd.DataFrame(df, columns = ['Country', 'Total Case'])
print(df_covid)


df_covid.replace('USA', "United States of America", inplace = True)
df_covid.replace('Tanzania', "United Republic of Tanzania", inplace = True)
df_covid.replace('Democratic Republic of Congo', "Democratic Republic of the Congo", inplace = True)
df_covid.replace('Congo', "Republic of the Congo", inplace = True)
df_covid.replace('Lao', "Laos", inplace = True)
df_covid.replace('Syrian Arab Republic', "Syria", inplace = True)
df_covid.replace('Serbia', "Republic of Serbia", inplace = True)
df_covid.replace('Czechia', "Czech Republic", inplace = True)
df_covid.replace('UAE', "United Arab Emirates", inplace = True)


url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'


# Adding the chloropleth layer onto the base map

folium.Choropleth(
   geo_data=country_shapes,
    name='choropleth',
    data=df_covid,
    columns=['Country', 'Total Case'],
    key_on='feature.properties.name',
    fill_color='PuRd',
    nan_fill_color='white'
).add_to(map)

# folium.LayerControl().add_to(m)
map.save("BaseMap.html")
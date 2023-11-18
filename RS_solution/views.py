from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
import folium
import pandas as pd # type: ignore
import os # type: ignore
import geopandas as gpd
import numpy as np
import fiona
import matplotlib
import locale
import json
from folium import plugins
from django.shortcuts import render, redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import rasterio as rio
from pyproj import Transformer

# Convert WindowsPath object to string
data_loc_str = str(settings.DATA_LOC)


def initialise_chart(year = '2021'):
    #________________

    #// MAP CANVAS (1) //
    
    #________________
    world_geo = os.path.join(data_loc_str, 'RSDATA', 'NDVI_' + year + '.png')

    world_map = folium.Map(location=[9.3054, -1.2591], zoom_start= 6.5)

    # Create a custom icon using the image
    # bounds = [[northern_lat, western_lon], [southern_lat, eastern_lon]]
    bounds = [[11.0257, -3.4226], [7.8539, 1.0593]]

    # Add a marker to the map using the custom icon
    overlay = folium.raster_layers.ImageOverlay(world_geo, bounds=bounds, opacity=1)
    overlay.add_to(world_map)

    folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map)

    fullscreen_control = folium.plugins.Fullscreen()
    world_map.add_child(fullscreen_control)

    folium.LayerControl().add_to(world_map)

    world_map = world_map._repr_html_()


    #________________

    #// MAP CANVAS (2) //
    
    #________________
    world_geo2 = os.path.join(data_loc_str, 'RSDATA', 'LULC_' + year + '.png')

    world_map2 = folium.Map(location=[9.3054, -1.2591], zoom_start= 6.5)

    # Create a custom icon using the image
    # bounds = [[northern_lat, western_lon], [southern_lat, eastern_lon]]
    bounds2 = [[11.0257, -3.4226], [7.8539, 1.0593]]

    # Add a marker to the map using the custom icon
    overlay2 = folium.raster_layers.ImageOverlay(world_geo2, bounds=bounds2, opacity=1)
    overlay2.add_to(world_map2)


    folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map2)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map2)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map2)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map2)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map2)

    fullscreen_control2 = folium.plugins.Fullscreen()
    world_map2.add_child(fullscreen_control2)

    folium.LayerControl().add_to(world_map2)

    world_map2 = world_map2._repr_html_()


    #________________

    #// MAP CANVAS (3) //
    
    #________________
    world_geo3 = os.path.join(data_loc_str, 'RSDATA', 'LST_' + year + '.png')

    world_map3 = folium.Map(location=[9.3054, -1.2591], zoom_start= 6.5)

    # Create a custom icon using the image
    # bounds = [[northern_lat, western_lon], [southern_lat, eastern_lon]]
    bounds3 = [[11.0257, -3.4226], [7.8539, 1.0593]]

    # Add a marker to the map using the custom icon
    overlay3 = folium.raster_layers.ImageOverlay(world_geo3, bounds=bounds3, opacity=1)
    overlay3.add_to(world_map3)


    folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map3)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map3)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map3)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map3)
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map3)

    fullscreen_control3 = folium.plugins.Fullscreen()
    world_map3.add_child(fullscreen_control3)

    folium.LayerControl().add_to(world_map3)

    world_map3 = world_map3._repr_html_()

    #_____________________

    #// PREPROCESSING //

    #____________________

    filename1 = os.path.join(data_loc_str, 'RSDATA', 'NDVI' + year + '.csv')
    filename = os.path.join(data_loc_str, 'RSDATA', 'LST' + year + '.csv')

    df1 = gpd.read_file(filename1)
    df2 = gpd.read_file(filename)


    dfGroupAA = df1[["system:time_start", "NDVI"]] # Selecting specific columns and getting rid of the commas in the string
    dfGroupAA["NDVI"] = dfGroupAA["NDVI"].astype('float') # Converting all the string in the columns to float
    graph1AXA = dfGroupAA['system:time_start'].values.tolist()
    graph1AYA = dfGroupAA['NDVI'].values.tolist()


    dfGroupA = df2[["system:time_start", "LST_Day_1km"]] # Selecting specific columns and getting rid of the commas in the string
    dfGroupA["LST_Day_1km"] = dfGroupA["LST_Day_1km"].astype('float') # Converting all the string in the columns to float
    graph1AX = dfGroupA['system:time_start'].values.tolist()
    graph1AY = dfGroupA['LST_Day_1km'].values.tolist()


    context = {
        'world_map' : world_map,
        'world_map2' : world_map2,
        'world_map3' : world_map3,
        'graph1AX' : graph1AX,
        'graph1AY' : graph1AY,
        'graph1AXA' : graph1AXA,
        'graph1AYA' : graph1AYA   
    }
    return context

def map(request):
    data = initialise_chart()
    return render(request, 'map.html', data)

def update_charts(request):
    
    selected_year = request.GET.get("year")
    
    if selected_year == "2019":
        csv_path = os.path.join(data_loc_str, 'RSDATA', 'LST2019.csv')
        csv_path2 = os.path.join(data_loc_str, 'RSDATA', 'NDVI2019.csv')
        csv_path3 = os.path.join(data_loc_str, 'RSDATA', 'NDVI_2019.png')
        csv_path4 = os.path.join(data_loc_str, 'RSDATA', 'LULC_2019.png')
        csv_path5 = os.path.join(data_loc_str, 'RSDATA', 'LST_2019.png')
    elif selected_year == "2020":
        csv_path = os.path.join(data_loc_str, 'RSDATA', 'LST2020.csv')
        csv_path2 = os.path.join(data_loc_str, 'RSDATA', 'NDVI2020.csv')
        csv_path3 = os.path.join(data_loc_str, 'RSDATA', 'NDVI_2020.png')
        csv_path4 = os.path.join(data_loc_str, 'RSDATA', 'LULC_2020.png')
        csv_path5 = os.path.join(data_loc_str, 'RSDATA', 'LST_2020.png')
    elif selected_year == "2021":
        csv_path = os.path.join(data_loc_str, 'RSDATA', 'LST2021.csv')
        csv_path2 = os.path.join(data_loc_str, 'RSDATA', 'NDVI2021.csv')
        csv_path3 = os.path.join(data_loc_str, 'RSDATA', 'NDVI_2021.png')
        csv_path4 = os.path.join(data_loc_str, 'RSDATA', 'LULC_2021.png')
        csv_path5 = os.path.join(data_loc_str, 'RSDATA', 'LST_2021.png')
    else:
        return JsonResponse({"error": "Invalid selection."})

    
    if selected_year == '':
        data = initialise_chart(selected_year)
    else:
        data = initialise_chart(selected_year)
        
    return JsonResponse(data)
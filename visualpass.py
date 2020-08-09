################################################################################
#                   #### visualpass.py #####                                   #
#                 #### written by: Etienne Deneault #####                      #
#    Program to construct visualization as a Function, called in the           #
#    Hiking_project_API.py program.                                            #
################################################################################

import json
from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
     CustomJS, CustomJSFilter, GeoJSONDataSource, HoverTool,
    LinearColorMapper, Slider, OpenURL, TapTool, Title, WheelZoomTool)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer, all_palettes, mpl
from bokeh.plotting import figure
import sqlite3
import requests
import visualpass

def visualization():
    # Read sqlite query results into a pandas DataFrame index
    db1 = sqlite3.connect("SQL_data/index.sqlite")
    df1 = pd.read_sql_query("SELECT * from Trails", db1)
    db1.close()

    # Set renderer for plotting
    sqlsource = ColumnDataSource(df1)
    # print(sqlsource)

    # Read in shapefile and examine data
    contiguous_usa = gpd.read_file('Data/cb_2018_us_state_20m.shp')
    # print(contiguous_usa.head())

    # Read in state population data and examine
    read_file = pd.read_excel ('Data/US_State_Elev_Peaks_name.xlsx')
    read_file.to_csv ('Data/US_STATE_EP.csv', index = None, header=True)
    state_elav = pd.read_csv('Data/US_STATE_EP.csv')
    # print(state_elav.head())

    # Merge shapefile with Highest Peaks data
    elav_states = contiguous_usa.merge(state_elav, left_on=["NAME"], right_on=["NAME"])

    # Drop Alaska and Hawaii
    elav_states = elav_states.loc[~elav_states['NAME'].isin(['Alaska', 'Hawaii'])]

    geosource = GeoJSONDataSource(geojson = elav_states.to_json())

    # Create figure object.
    p = figure(title = 'Hiking Trails Mapping',
               plot_height = 600 ,
               plot_width = 950,
               toolbar_location = 'right',
               tools = "pan,wheel_zoom,box_zoom,reset",
               active_scroll= "wheel_zoom")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    states = p.patches('xs','ys', source = geosource,
                       fill_color = None,
                       line_color = "gray",
                       line_width = 0.25,
                       fill_alpha = 1)

    # Define color palettes
    palette = brewer['BrBG'][11]
    # palette = mpl['Cividis'][10]
    # ('#440154', '#30678D', '#35B778', '#FDE724')
    palette = palette[::-1] # reverse order of colors so higher values have darker colors
    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 15000)

    # Define custom tick labels for color bar.
    tick_labels = {"0": "0", "500": "500",
     "1000":"1,000", "1500": "1,500", "2500": "2,500",
     "3500": '3,500', "4000": "4,000",
     "7,000":"7,000", "10000":"10,000",
     "14,000":"14,000", "18000":"18,000", "22000":"22,000+"}

    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=10,width = 500, height = 20,
                          border_line_color=None, scale_alpha = 0.5 , location = (0,0), orientation = 'horizontal',
                          major_label_overrides = tick_labels)

    # Create figure object.
    p = figure(title = 'Hiking Trail Locations and Highest State Elevation Peak Data (US mainland)', plot_height = 600 ,
                plot_width = 950, toolbar_location = 'right',
                tools = "pan, wheel_zoom, box_zoom, reset, tap")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text_font_size = "6px"
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)

     # Add patch renderer to figure.
    states = p.patches('xs','ys', source = geosource,
                        fill_color = {'field' :'H_Elevation', 'transform' : color_mapper},
                        line_color = 'gray', line_width = 0.25, fill_alpha = 0.5)

    trails = p.circle('longitude', 'latitude', radius=0.01, source=sqlsource, color="black")
    # Create Tap tool
    taptool = p.select(type=TapTool)
    # url = df[url]
    taptool.callback = OpenURL(url='@url')

    # Create hover tool (trail location circles)
    p.add_tools(HoverTool(renderers = [trails],
                          tooltips = [('Trail','@name'), ('Length', '@length'), ('Latitude', '@latitude'),
                          ('Longitude', '@longitude'), ("Stars", "@stars"), ("URL", '@url')]))
    # Create hover tool (States and Highest Elevation)
    p.add_tools(HoverTool(renderers = [states],
                          tooltips = [('State','@NAME'),
                                    ('Highest Elevation','@H_Elevation')]))

    p.add_tools
    # Add the Legend Color Bar
    p.add_layout(color_bar, 'below')
    # add text info to layout
    p.title.text_font_size = "20px"
    p.add_layout(Title(text="Legend: Altitude(feet)", align="left"), "below")
    p.add_layout(Title(text="Click on Trail for url", align="left"), "above")

    # return to ___main___
    return show(p)

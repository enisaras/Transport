from __future__ import annotations

import os
import json
import requests
import pendulum
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, LineString, Polygon, MultiLineString
from shapely import wkt
# import csv
from airflow.decorators import dag, task
import pandas as pd

# [END import_module]


# [START instantiate_dag]
@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["subway"],
)
def plot_subway_lines():
    """
    ### TaskFlow API Tutorial Documentation
    This task plo
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    # [END instantiate_dag]

    # [START extract]

    @task
    def getSubwayLines(url):
        os.environ['NO_PROXY'] = '*'
        """
        Grabs data from the MTA subway lines.
        parameters: url(string)
        returns: response(json)
        """
        response = requests.get(url)
        with open("/Users/earas/airflow/csvs/lines.json", "x") as outfile:
            json.dump(response.json(), outfile)


    @task()
    def getStops(url):
        os.environ['NO_PROXY'] = '*'
        """
        Grabs data from the MTA stops.
        parameters: url(string)
        returns: None
        """
        stops_data_list = requests.get(url).json()
        with open("/Users/earas/airflow/csvs/stops.json", "x") as outfile:
            json.dump(stops_data_list, outfile)


    @task()
    def initLineGeoDataFrame(path):
        """
        """
        f = open(path)
        data = json.load(f)
        
        line_strings = [0] * len(data)
        # Convert into LineString object
        for i in range(len(data)):
            coordinates = data[i]['the_geom']['coordinates']
            line_strings[i] = LineString(coordinates)
            data[i]['the_geom'] = line_strings[i]

        crs = {'init':'EPSG:4326'}
        geo_dataframe = gpd.GeoDataFrame(data, geometry="the_geom", crs=crs)

        routes = list(geo_dataframe['rt_symbol'].unique())
        # add RGB colors for each route
        route_colors = {routes[0]: "#7CFC00", 
                        routes[1]: "#FFFF00", 
                        routes[2]: "#FFA500",
                        routes[3]: "#696969",
                        routes[4]: "#00008B",
                        routes[5]: "#800080",
                        routes[6]: "#D2691E",
                        routes[7]: "#FF0000",
                        routes[8]: "#008000"}
        geo_dataframe['color'] = geo_dataframe['rt_symbol'].map(route_colors)

        geo_dataframe.to_csv('/Users/earas/airflow/csvs/linesdataframe.csv')


    @task
    def initStopsGeoDataFrame(path):
        f = open(path)
        data = json.load(f)
        stop_shapes = [0] * len(data)
        print(len(stop_shapes))
        for i in range(len(data)):
            coordinates = data[i]['the_geom']['coordinates']
            stop_shapes[i] = Point(coordinates)
            data[i]['the_geom'] = stop_shapes[i]
        # Init dataframe
        stops_geoframe = gpd.GeoDataFrame(data, geometry = 'the_geom')
        # set crs
        crs = {'init':'EPSG:4326'}
        stops_geoframe = stops_geoframe.set_crs(crs)
        stops_geoframe.to_csv('/Users/earas/airflow/csvs/stopsdataframe.csv')
        

    """    
    @task
    
    def initStopGeoDataframe(stop_data):
        stops_geoframe = gpd.GeoDataFrame(stop_data, geometry = 'the_geom')
        crs = {'init':'EPSG:4326'}
        stops_geoframe = stops_geoframe.set_crs(crs)
        return stops_geoframe
    """

    """
    @task
    def plotSubwayMap(lines_path, stops_path):
        plt.ioff()
        lines_df = pd.read_csv(lines_path)
        stops_df = pd.read_csv(stops_path)
        lines_df['the_geom'] = lines_df['the_geom'].apply(wkt.loads)
        stops_df['the_geom'] = stops_df['the_geom'].apply(wkt.loads)
        lines_gdf = gpd.GeoDataFrame(lines_df, geometry='the_geom', crs = 'EPSG:4326')
        stops_gdf = gpd.GeoDataFrame(stops_df, geometry='the_geom', crs = 'EPSG:4326')

        nyc_map = gpd.read_file('/Users/earas/Downloads/nyad_23b/nyad.shp')
        fig, ax = plt.subplots(figsize = (20,30))
        nyc_map.to_crs(epsg=4326).plot(ax=ax, color='lightgrey')
        # lines_gdf.plot(ax=ax, color=lines_gdf['color'])
        # stops_gdf.plot(ax=ax)
        plt.close(fig)
        fig.savefig('/Users/earas/airflow/plots/subway_plot.jpg')
    """
    # [START main_flow]
    getSubwayLines("https://data.cityofnewyork.us/resource/s7zz-qmyz.json") >> initLineGeoDataFrame("/Users/earas/airflow/csvs/lines.json")
    getStops("https://data.cityofnewyork.us/resource/kk4q-3rt2.json") >> initStopsGeoDataFrame("/Users/earas/airflow/csvs/stops.json")
    # plotSubwayMap('/Users/earas/airflow/csvs/linesdataframe.csv', '/Users/earas/airflow/csvs/stopsdataframe.csv')
    # [END main_flow]


# [START dag_invocation]
plot_subway_lines()
# [END dag_invocation]

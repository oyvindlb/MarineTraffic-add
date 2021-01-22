
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:47:13 2021

@author: oyvin
"""

#conda install -c conda-forge basemap-data-hires=1.0.8.dev0
#pip install Marine-Traffic-API

import os
os.environ['PROJ_LIB'] = 'INSERT DIRECTORY FOR BASEMAP LIBRARY'
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain
import schedule
import requests
import time
import datetime
from datetime import datetime, timedelta
from copy import copy
from marinetrafficapi import MarineTrafficApi
import pandas as pd





class marine_data_plot:
    
    def __init__(self):
        
        "Constructur"
        self.dict_lon = {}
        self.dict_lat = {}

        

    def vessel_info_API(self, mmsi_number):
        
        api = MarineTrafficApi(api_key="_INSERT__API__KEY__")
        for vessel in mmsi_number:
            vessel_positions = api.vessel_historical_track(period='daily', days=2, mmsi=vessel)
            MarineTrafficApi.print_params_for('vessel_historical_track')
            
            #print(len((vessel_positions)))
            
            print(vessel)
            for position in vessel_positions.models:
                longitude = position.longitude.value
                latitude = position.latitude.value
                print(longitude)
                print(latitude)
                #time = position.timestamp.value
                if vessel in self.dict_lon or vessel in self.dict_lat:
                    self.dict_lon[vessel].append(latitude)
                    self.dict_lat[vessel].append(longitude)
                else:
                    self.dict_lon[vessel] = []
                    self.dict_lat[vessel] = []
                    self.dict_lon[vessel].append(latitude)
                    self.dict_lat[vessel].append(longitude)
            
        
    def make_figure(self, names_dict):
        
        plt.figure(figsize=(50, 50))
        m = Basemap(width=12000000,height=9000000,projection='lcc', resolution='c',lat_1=-30,lat_2=0,lat_0=65,lon_0=12.)
        m.drawcoastlines()
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='coral',lake_color='aqua')

        for key, value in self.dict_lon.items():
            #plt.plot(self.dict_lat[key], value)
            x, y = m(self.dict_lat[key], value)
            plt.plot(x, y, 'o-', markersize=15, linewidth=5, label=names_dict[key])
            plt.legend()
            
        plt.rc('font', size=35)
        plt.rc('axes', labelsize=35)
        
        m.shadedrelief()
        plt.show()
        

def initiating():
    
    graph_class = marine_data_plot()
    starttime = time.time()
    label_name_dict = {258778000:"GADUS POSEIDON",
                       257317000:"Gadus Neptun",
                       257656000:"Gadus Njord",
                       257267000:"Nordtind",
                       259683000:"Vesttind",
                       259707000:"Havtind"
                       }
    vessels = [258778000, 257317000, 257656000] #, 257267000, 259683000, 259707000]

    graph_class.vessel_info_API(vessels)
    graph_class.make_figure(label_name_dict)

    
        

if __name__ == '__main__':

    initiating()    

        

    
    
    
    
    
    
    
    
    

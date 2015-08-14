# -*- coding: utf-8 -*-

import scipy
import numpy as np
import pandas as pd

import geopandas.io.osm as osm

import pandana

import pandana.loaders.osm as osm_load


# In[2]:

met_areas = pd.read_table('Gaz_ua_national.txt', header = 0, names = 
                          ['id', 'name', 'type', 'pop','households',
                           'area', 'water', 'area_mi', 'water_mi',
                           'lat', 'lon'])
big_mets = met_areas[met_areas['pop'] > 100000]
print big_mets[['name', 'area']]
print 'number of metropolitan areas is {}'.format(len(big_mets))


# In[3]:

# coords = pd.DataFrame()

# met_per_lon = 111000
# met_per_lat = 88000

# coords['name'] = big_mets.name
# coords['x_min'] = big_mets.lon - 0.5 * np.sqrt(big_mets.area)/met_per_lon
# coords['y_min'] = big_mets.lat - 0.5 * np.sqrt(big_mets.area)/met_per_lat
# coords['x_max'] = big_mets.lon + 0.5 * np.sqrt(big_mets.area)/met_per_lon
# coords['y_max'] = big_mets.lat + 0.5 * np.sqrt(big_mets.area)/met_per_lat

# print coords.head()


# In[4]:

# coords.to_csv('met_area_coords.csv')


# In[4]:

pandana.network.reserve_num_graphs(len(big_mets)) # TODO figure out how to delete networks

print 'reserved {} networks'.format(len(big_mets))


# In[8]:

met_per_lon = 111000
met_per_lat = 91000


for num, row in big_mets.iterrows():
    # for row in atlanta
    leng = np.sqrt(row['area'])/2

    x_min, x_max = row.lon - leng/met_per_lon, row.lon + leng/met_per_lon
    y_min, y_max = row.lat - leng/met_per_lat, row.lat + leng/met_per_lat

    print x_min, x_max, y_min, y_max

    osm_load.h5_from_bbox(y_min, x_min, y_max, x_max, '{}.h5'.format(row['name'].replace(' ', '')))

    print 'saved {}'.format(row['name'])


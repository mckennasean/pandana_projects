# -*- coding: utf-8 -*-

import scipy
import numpy as np
import pandas as pd

import geopandas.io.osm as osm

import pandana

import pandanas.loaders.osm as pdosm

def h5_from_bbox(lat_min, lng_min, lat_max, lng_max, filename, rm_nodes=None,
                network_type='walk', two_way=True):
    """
    Save an HDF5 file with 'nodes' and 'edges' panels from a bounding lat/lon box.

    Parameters
    ----------
    lat_min, lng_min, lat_max, lng_max : float
    filename : string
    rm_nodes : array_like
        A list, array, Index, or Series of node IDs that should *not*
        be saved as part of the Network.
    network_type : {'walk', 'drive'}, optional
        Specify whether the network will be used for walking or driving.
        A value of 'walk' attempts to exclude things like freeways,
        while a value of 'drive' attempts to exclude things like
        bike and walking paths.
    two_way : bool, optional
        Whether the routes are two-way. If True, node pairs will only
        occur once.

    Returns
    -------
    Nothing. Writes an HDF5 file to the current directory.

    """
    net =  pdosm.network_from_bbox(lat_min, lng_min, lat_max, 
                        lng_max, network_type, two_way)
    pandana.loaders.pandash5.network_to_pandas_hdf5(net, filename, rm_nodes)



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

    h5_from_bbox(y_min, x_min, y_max, x_max, '{}.h5'.format(row['name'].replace(' ', '')))

    print 'saved {}'.format(row['name'])


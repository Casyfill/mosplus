#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import geopandas as gp
from shapely.geometry import shape
import os


def _processGeom(x):
	'''process geometry,
	if problem - return NAN
	'''
	try:
		return shape(x)
	except:
		return pd.np.NAN


def processData(path='raw.json', chunks=4):
	'''
	read data from raw dump, process and split to few chunks, if necessary

	Args:
		path(str): path to the raw file
		chunks(int): number of files to save into
	Returns:
		none: saves chunks as geojsons in espg4326 as "footprint2utf_N.json" files in the root 
	'''

	df = pd.read_json(path)
	DF = pd.DataFrame.from_dict(df['Cells'].tolist())

    DF['AdmArea'] = DF['AdmArea'].apply(lambda x: ', '.join(x))
    DF['geometry'] = DF['geoData'].apply(processGeom)

    problem = DF[pd.isnull(DF['geometry'])]
    print 'Detected {0} rows with ambigious geometry. saved to: problematic.csv'.format(len(problem))
    problem.to_csv('problematic.csv', encoding='utf8')

    G2 = gp.GeoDataFrame(DF[pd.notnull(DF['geometry'])], geometry='geometry')
    G2.crs = {'init': 'epsg:4326', 'no_defs': True}
    G2.drop('geoData', 1, inplace=1)

    print 'Generating {0} files:'.format(chunks)
    for i, chunk in enumerate(pd.np.array_split(G2, chunks)):
        print '...chunk {0} generated'.format(i)
        with open('footprint2utf_{0}.json'.format(i), 'w') as f:
            f.write(chunk.to_json(encoding='utf8'))

if __name__ == '__main__':
	path = 'raw.json'
	if os.path.isfile(path):
		processData(path, chunks=4)
	

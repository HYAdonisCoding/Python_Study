# -*- coding: utf-8 -*-
import pandas as pd
import geopandas as gpd
import sys

def main():
    
    df = sys.argv[1]
    dfs = pd.read_csv(df)
    dfs['LON']=dfs['Longitude(deg)']
    dfs['LAT']=dfs['Latitude(deg)']
    dfs['WS']=dfs['Wind Speed (m/s)']
    dfs['radius']=0
    num = len(dfs)
    for i in range(0, num):
        # print(dfs['Ut'].loc[i])
        rad = (10.4/max(0.1, abs(dfs['WS'][int(i)])))**(1/1.935)
        out1 = max(1.5, rad)
        outf = min(25, out1)
        dfs[' radius' ].loc[i] = outf
    
    gdf = gpd.GeoDataFrame(dfs, geometry=gpd.points_from_xy(dfs['LON'], dfs['LAT']))
    gdf = gdf.set_crs(epsg=4326, inplace=True)
    gdf=gdf.to_crs("EPSG:32650")
    gdff = gdf.buffer(gdf['radius'])
    
    output = gpd.GeoDataFrame(geometry=[gdff.unary_union])
    output = output.set_crs(epsg=32650, inplace=True)
    output= output.to_crs(epsg=4326)
    
    output.to_file('out.js', outdriver='GeoJSON')

if __name__ == '__main__':
    main()
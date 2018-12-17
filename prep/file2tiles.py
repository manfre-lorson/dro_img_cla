# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 08:55:22 2018

@author: fw56moba
"""

'''image to tile'''


import sys
import osgeo.gdalnumeric as zz_gdalnum
import osgeo.gdalconst as zz_gdalcon

import os

from osgeo import gdal
from osgeo import osr

import MacPyver as mp
import numpy as np


def read_tif(tif,band=1,nodata=0):
    """reads in the a tif, the specified band or all bands
        band default is 1 
        if you read in on band the return is a 2d array
        if band is set to 'all', it will return a 3d array (bands, x, y)""" 
    try:
        #default band is 1 and default for return nodata value is False ~ 0 ;1 ~ True
        inTif = zz_gdalnum.gdal.Open(tif, zz_gdalcon.GA_ReadOnly)
        if type(inTif)!='NoneType':
            #test if passed band is in the raster
            nr_of_bands = inTif.RasterCount
            if band > nr_of_bands and band != 'all':
                raise NameError('band not in file max Nr. of bands: {0}'.format(nr_of_bands))
            if band == 'all':
                #create a 3d stack of the data (band, x, y)
                bands = inTif.GetRasterBand(1)
                data = zz_gdalnum.BandReadAsArray(bands)
                y,x = data.shape
                shape = (1,y,x )
                data = data.reshape(shape)
                for b in range(2, nr_of_bands):
                    bands = inTif.GetRasterBand(b) 
                    data = np.vstack((data, zz_gdalnum.BandReadAsArray(bands).reshape(shape)))
            else:
                
                band = inTif.GetRasterBand(band)
                data = zz_gdalnum.BandReadAsArray(band)
                inTif = None
                
            if type(data)==None.__class__:
                raise
            else:
                if nodata==0:
                    return data
                elif nodata==1:
                    noda = band.GetNoDataValue()
                    return data, noda
        else:
            raise NameError('input is not a file or file is broken')
    except:
        print "Error:", sys.exc_info()[:2]
        inTif = None
        raise


def calc_dst_extent(src_extent, x,y):
    left, top, col, row, px, py = src_extent.ret_extent()
    newleft = left + x*tileshape[0] * px
    newtop = top + y*tileshape[1]* py
    return (newleft,px, 0, newtop,0 ,py)

def write_raster(full_output_name, dataset, dst_extent, dtype=2):
    dtypeL = [zz_gdalcon.GDT_Int16,
              zz_gdalcon.GDT_Int32,
              zz_gdalcon.GDT_UInt16,
              zz_gdalcon.GDT_UInt32,
              zz_gdalcon.GDT_Float32,
              zz_gdalcon.GDT_Float64,
              zz_gdalcon.GDT_Byte]
    try:
        if len(data.shape)==3:
            nr_of_bands = data.shape[0]
        elif len(data.shape)==2:
            nr_of_bands = 1
        else:
            print('error in Bands')
            sys.exit(1)
        
        outraster = gdal.GetDriverByName('GTIFF').Create(full_output_name, tileshape[0], tileshape[1], nr_of_bands, dtypeL[dtype], options=['COMPRESS=DEFLATE'])
        outraster.SetGeoTransform(dst_extent)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        outraster.SetProjection(srs.ExportToWkt())
        for band in range(nr_of_bands):
            if nr_of_bands==1:
                outraster.GetRasterBand(band+1).WriteArray(dataset)            
                #bandOut = outraster.GetRasterBand(band+1)
                #zz_gdalnum.BandWriteArray(bandOut,data)
            else:
                outraster.GetRasterBand(band+1).WriteArray(dataset[band,:,:])
                #zz_gdalnum.BandWriteArray(bandOut,data[band,:,:])
                #bandOut = None            
        #outraster.GetRasterBand(1).WriteArray(dataset)
        outraster = None
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
        print ("Could not write the nodata value")
    except:
        print "Unexpected error:", sys.exc_info()
      
    

path = r'S:\Andrea_Perino\Fieldwork_2016\gcp_fights_2016\composite_flight_1.tif'
outpath = r'S:\Florian_Wolf\Lab\drone_ki_slope\drone_nn\images'
tileshape = (100,100) #(x-res, y-res)
data = read_tif(path, 'all')
epsg = 32629
src_extent = mp.raster.tiff.get_extent(path)


for x in range(134):
    for y in range(140):
        outdata = data[:, y*tileshape[1]:tileshape[1]+y*tileshape[1], x*tileshape[0]:tileshape[0]+x*tileshape[0]]
        dst_extent = calc_dst_extent(src_extent, x, y)
        outname = outpath + os.sep + '{0}_x{1}_y{2}.tif'.format(path.split(os.sep)[-1][:-4], x, y)
        write_raster(outname, outdata, dst_extent)

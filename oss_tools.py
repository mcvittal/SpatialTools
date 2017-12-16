import numpy, gdal

from osgeo import gdal_array

from gdalconst import *

## RasterToNumPyArray: String NumPy(Datatype) --> NumPy Array 
##
## Description:
## 
## Takes in a raster and returns it as a 2D (if single band) or 3D (if >1 band) raster.
## Datatype of array is determined by input data, or can be passed in. 
##
## Inputs:
## 
## raster_path:  Path to a valid Raster-type file. 
## 
## dtype:        numpy datatype. 
##               ex. numpy.uint8 
##
## Outputs:
## Returns a numpy array. Output is a 2D array if singular band input, and 3D if multiple bands. 

def RasterToNumPyArray(raster_path, dtype=None):
    if dtype == None:
        return gdal.Open(raster_path).ReadAsArray()
    else:
        return gdal.Open(raster_path).ReadAsArray().astype(dtype)

## getProjection: String --> GDAL Projection Datatype 
##
## Description: 
## 
## Gets the projection info from an existing raster file as a GDAL datatype.
##
## Inputs: 
## 
## in_raster_path: Path to a valid raster file 
##
## Outputs:
## 
## Returns the projection of the input raster 

def getProjection(in_raster_path):
    return gdal.Open(in_raster_path).GetProjection()

## getProjection: String --> GDAL Geotransformation Datatype 
##
## Description: 
## 
## Gets the transformation info from an existing raster file as a GDAL datatype.
##
## Inputs: 
## 
## in_raster_path: Path to a valid raster file 
##
## Outputs:
## 
## Returns the transformation of the input raster 
def getGeoTransform(in_raster_path):
    return gdal.Open(in_raster_path).GetGeoTransform()


## NumPyArrayToRaster: Array[][], GDAL Projection, GDAL Geotransform, String, Datatype 
##
## Description:
##
## Converts a Numpy array into a GeoTIFF using GDAL libraries. 
## Designed to be a replacement to ESRI's equivalent function NumPyArrayToRaster.
##
## Inputs:
## 
## nparr:               A valid 2D or 3D Numpy array containing numerical data. 
##
## proj:                A valid GDAL projection datatype. Can be obtained by using getProjection() 
##
## geot:                A valid GDAL geotransform datatype. Can be obtained by using getGeoTransform()
##
## out_raster_path:     A path to where you would like to save the raster dataset.
##
## dtype:               Optional, allows user to specify the datatype in the output TIFF. Is a GDAL datatype.
##                      If not specified, will use the closest match to what is contained in the Numpy array.

def NumPyArrayToRaster(nparr, proj, geot, out_raster_path, dtype=None):
    gdal.AllRegister()
    np_dt = nparr.dtype 
    if dtype == None:
        dtype = gdal_array.NumericTypeCodeToGDALTypeCode(np_dt)

    print( "saving")
    # Check if working with multiband raster
    if len(nparr.shape) == 3:
        n_bands = nparr.shape[0] 
        for x in range(0, n_bands):
            driver = gdal.GetDriverByName('GTIFF')
            outDs = driver.Create(out_raster_path, nparr.shape[2], nparr.shape[1], n_bands, dtype,
                                  ['COMPRESS=LZW', 'TILED=YES', 'BLOCKXSIZE=128', 'BLOCKYSIZE=128'])
            outDs.GetRasterBand(x + 1).WriteArray(nparr[x])
            outDs.GetRasterBand(x + 1).FlushCache()
            outDs.SetProjection(proj)
            outDs.SetGeoTransform(geot)

            outDs = None
    else:
        driver = gdal.GetDriverByName('GTIFF')
        outDs = driver.Create(out_raster_path, nparr.shape[1], nparr.shape[0], 1, dtype,
                              ['COMPRESS=LZW', 'TILED=YES', 'BLOCKXSIZE=128', 'BLOCKYSIZE=128'])
        outDs.GetRasterBand(1).WriteArray(nparr)
        outDs.GetRasterBand(1).FlushCache()
        outDs.SetProjection(proj)
        outDs.SetGeoTransform(geot)
        outDs = None


import numpy, gdal 

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


    
def NumPyArrayToRaster(nparr, proj, geot, out_raster_path, dtype=None):
    gdal.AllRegister()
    np_dt = nparr.dtype 
    
    
    # Merge the output raster with the raster saved to disk - does not seem to want to overwrite the output 
    # so instead, read in, merge, delete and save to file. 
    try:
        os.remove(out_raster_path)
        # Sometimes has to wait a bit for IO to finish deleting the file. 
        while os.path.isfile(out_raster_path):
            time.sleep(1)

    except:
        pass # For first run, it won't be able to merge, rather just write it to file. Hence try catch. 

    print "saving"
    driver = gdal.GetDriverByName('GTIFF')             
    outDs = driver.Create(out_raster_path, nparr.shape[1], nparr.shape[0], 1, GDT_UInt16, 
                          ['COMPRESS=LZW', 'TILED=YES', 'BLOCKXSIZE=128', 'BLOCKYSIZE=128'])
    outDs.GetRasterBand(1).WriteArray(nparr)
    outDs.GetRasterBand(1).SetNoDataValue(255)
    outDs.GetRasterBand(1).FlushCache()
    outDs.SetProjection(proj)
    outDs.SetGeoTransform(geot)
       
    outDs = None 
    

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

        
## convertToNetlogo: String String --> None 
## 
## Purpose
##      Converts an input GeoTIFF raster into a plaintext file that can be read in by the NetLogo 
##      modelling language and use it as a surface for the turtles to interact with. 
##
## Inputs
##      tif_file                A path to a valid GeoTIFF file. Spatial information does not necessarily matter. 
##      output_nlogo_textfile   A path to where you'd like the output netlogo surface file to go 
##      percentage_increase     How often you'd like progress indicators to print to the screen. Default value: 20. Optional.

def convertToNetLogo(tif_file, output_nlogo_textfile, percentage_increase=20):
    # Specifies which band the input data is in for the raster.
    data_band = 1
    
    # Read the TIF file as a GDAL object
    tif_connection = gdal.Open(tif_file)

    # Convert the TIF connection to a Numpy 2D array (First band only)
    tif_array = numpy.array(tif_connection.GetRasterBand(data_band).ReadAsArray())
    #tif_array = numpy.full((200, 10000), 0)

    # Setup connection to output dataset
    output_connection = open(output_nlogo_textfile, 'w')

    # An indicator dict to print percentage
    progress = {}
    for x in range(0, 101, percentage_increase):
        progress[x] = True
    # Begin looping through numpy array
    for y in range(tif_array.shape[0] - 1, -1, -1):
        for x in range(0, tif_array.shape[1]):
            # Get percentage (Current PercenTage)
            cpt = round((((x + 1) * ( y + 1)) / float(tif_array.shape[0] * tif_array.shape[1])) * 100, 0 )
            cpt = int(cpt)
            # Print the progress if it hasn't been printed before - good simple UI
            if cpt in progress.keys():
                if progress[cpt]:
                    print ("{}% done".format(cpt))
                    progress[cpt] = False
            # Write current indice to output file
            output_connection.write("{}\t{}\t{}\n".format(y, tif_array.shape[1] - x, tif_array[y][x]))

    # Close the IO stream
    output_connection.close()

    
## reclass:     String List String --> None 
## Purpose 
##      Reclassifies a raster based on a raster reclassification table 
##
## Inputs 
##      in_raster       Path to a singleband input raster 
##      reclass_table   A list of three element lists. 
##                      [start_range, end_range, reclass_value] 
##                      Mathematically, this looks like 
##                      start_range <= x < end_range 
##
##                      There is a final element where it is a single value where you reclass all other
##                      values not in the specified ranges. 
##
##      out_raster      Path to an output raster
def reclass(in_raster, reclass_table, out_raster):
    nparr = RasterToNumPyArray(in_raster) 
    min_start_range = 0 
    max_end_range = 0 
    for i in reclass_table[:-1]:
        start_range = i[0]
        end_range = i[1]
        if start_range < min_start_range:
            min_start_range = start_range 
        if end_range > max_end_range:
            max_end_range = end_range 
        rc_val = i[2] 
        nparr[(start_range <= nparr)  & (nparr < end_range)] = rc_val 
    final_rc_val = reclass_table[-1:][0]
    #nparr[nparr < min_start_range] = final_rc_val
    #nparr[nparr >= max_end_range] = final_rc_val
    NumPyArrayToRaster(nparr, getProjection(in_raster), getGeoTransform(in_raster), out_raster)
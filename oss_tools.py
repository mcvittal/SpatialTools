import numpy, gdal 

def RasterToNumPyArray(raster_path):
    try:
        return gdal.Open(raster_path).ReadAsArray().astype(numpy.uint8)
    except:
        time.sleep(0.5)
        return RasterToNumPyArray(raster_path)

        
def getProjection(in_raster_path):
    return gdal.Open(in_raster_path).GetProjection() 

def getGeoTransform(in_raster_path):
    return gdal.Open(in_raster_path).GetGeoTransform()

    
def NumPyArrayToRaster(nparr, proj, geot, out_raster_path):
    gdal.AllRegister()
    
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
import oss_tools as o_t
raster_path = "/home/alex/Documents/gis/World_Data/30 arc-second grid/asciito_worl1/hdr.adf"

d = o_t.RasterToNumPyArray(raster_path)
print ('test')
geot = o_t.getGeoTransform(raster_path)
print ('test2')
proj = o_t.getProjection(raster_path)
print ('test3')
nodata = o_t.getNoDataValue(raster_path)
print ('test4')
o_t.NumPyArrayToRaster(d, proj, geot, nodata, "/tmp/l.tif")


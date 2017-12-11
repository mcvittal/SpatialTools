# SpatialTools


This is split into three different classes:


## arcpy_tools.py

Contains functions that require the `arcpy` libraries.

## oss_tools.py

Contains various geospatial tools that use GDAL and numpy for processing. 

## general_tools.py 

Contains some helper functions that are still used in both oss_tools and arcpy_tools, but aren't necessarily spatial-releated or need special spatial libraries to execute.



# Using this repository


Simply create a new python file in the root of the repository, and import the classes 

    import arcpy_tools as a_t 
	import oss_tools as o_t 
	
	
	a_t.force_license(['spatial'])
	
	spatial_reference = o_t.getProjection("D:\\GIS\\elevation.tiff")
	
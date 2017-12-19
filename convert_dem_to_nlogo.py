#!/usr/bin/env python3

# This codebase converts a TIF elevation file into a netlogo-compatible file
# Requirements - GDAL, Numpy. Should work in either python2 or python3.

# If using a Linux system (Debian-based specifically), use the packages python3-gdal, python3-numpy
#     or python-gdal, python-numpy if using python2. pip can be problematic for getting gdal installed.


# Basic imports
import sys, os

# Spatial imports
import gdal, numpy

# Get the output and input filenames from either system arguments or from hardcoded values
try:
	tif_file = sys.argv[1]
	output_nlogo_textfile = sys.argv[2]
except:
	tif_file = "/tmp/placeholder.tif"
	output_nlogo_textfile = "/tmp/elevation.txt"

# For printing out how far it is.
percentage_increase = 20

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


# Introduction

This is a tool written in Python that automatically formats and joins census data downloaded from the CHASS census analyzer and generates census data dictionaries.

# Pre-processing steps needed

In order for this to join to the shapefiles, you must create a field that ends with the text “Long” of datatype Long Integer that contains the GEO UID of the given census level. For instance, your DA boundary file should have a field added named DAUIDLong that contains the DA ID’s.

# Downloading the census data

The tool is robust and can handle very large datasets, but the CHASS tool does not seem to like you checking every single variable and asking it to download the over 6000 columns. In testing, 1400 columns seemed to work just fine. Simply go through each census sheet page and click “Check All” until you’ve reached ~1000 columns, at which point scroll to the bottom of the page and select the Download as CSV option. 

**Be sure to also include the Age & Sex – Age Characteristics Total in all downloads.**  This will ensure that the total population statistics are included in all joins. 


* Note: Do not check any of the “Optionally include in the result” checkboxes.*


Once the CHASS tool accepts your query and processes the end results, save both the header and data file to a directory. Do not rename the files, leave them as is. The census formatter tool will not be able to process the data if the header file is named differently from the data file apart from the “_header.txt” and “_data.csv” portion of the filenames. 


Now that you have all the data downloaded and ready for processing, it’s time to process the data. 

# Tool setup

There is very little setup needed in this Python tool, after the GEO UID fields have been appropriately set up and all files have been downloaded. 

**input data dir**  
This is a path to the folder that contains all the raw data and header files. 

**boundary_files**  
This is a dictionary that contains the paths to the boundary files that will be used for joining. Currently, both digital and cartographic shapefile paths are included, but the tool only joins to the cartographic.   
Double check the paths to make sure that it is for the current census year, and that it points to the files with the proper field names set.  
out_directoryThis is the directory where all geodatabases containing joined census data, along with the folder that will contain the census dictionaries, will be put. 

**temp_directory**  
A temporary working directory that will house miscellaneous files during processing steps.


# Running the tool

Now that you have everything set up, it’s time to run it! Simply open in your favourite Python IDE that is configured to use the ArcMap python libraries and run. It prints helpful messages letting you know what it is currently processing.




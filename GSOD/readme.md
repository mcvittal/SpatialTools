# GSOD scripts

This folder details methods to download and organize NOAA's Global Surface Of the Day dataset (GSOD).

## Download

Use the `gsod_downloader.sh` script to bulk download the entire dataset.

## Organization

`gsod_organizer.py` will organize the raw files downloaded by country and then by year for a more manageable dataset.

## Conversion to useable CSV formats

`gsod_datahandler.py` will convert the raw plaintext, fixed-width delimited .op files into CSV files.  
The format of these files are simple: All stations for a given year are included, with the lat/lon of the stations included, as well as the station name and country code.  
Each column is a singular date, with 999.9 being nodata values. The 12 variables included in the dataset are stored as separate files.

`gsod_csvtogdbtable.py` uses Arcpy libraries to convert the CSV files into ESRI feature classes.

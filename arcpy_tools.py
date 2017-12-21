import arcpy, time, os, shutil 

import general_tools as gt

## Arcpy_Tools.py 
## 
## Contains python tools pertaining to Arcpy-related functions 



## force_license: list(String) --> None 
##
## Description: 
##
## Repeatedly attempts to sign out each license in the list of licenses passed in.
## Useful to include in scripts that require a specific license to run if there are limited licenses available in the office. 
##
## Requirements: 
## 
## Requires that there is at least one of each license you are requesting in the license server. Otherwise it will never finish. 
##
## Inputs:
##
## list_of_licenses: A list of strings that are the codes for the different licenses.
##       Code                   Description 
##       ==================     ==========================
##       3D                     ArcGIS 3D Analyst extension
##       Datareviewer           ArcGIS Data Reviewer for Desktop
##       DataInteroperability   ArcGIS Data Interoperability extension for Desktop
##       Airports               ArcGIS for Aviation: Airports
##       Aeronautical           ArcGIS for Aviation: Charting
##       Bathymetry             ArcGIS for Maritime: Bathymetry
##       Nautical               ArcGIS for Maritime: Charting
##       GeoStats               ArcGIS Geostatistical Analyst extension
##       Network                ArcGIS Network Analyst extension
##       Spatial                ArcGIS Spatial Analyst extension
##       Schematics             ArcGIS Schematics extension
##       Tracking               ArcGIS Tracking Analyst extension
##       JTX                    ArcGIS Workflow Manager for Desktop
##       ArcScan                ArcScan
##       Business               Business Analyst
##       Defense                Esri Defense Solution
##       Foundation             Esri Production Mapping
##       Highways               Esri Roads and Highways
##       StreetMap              StreetMap
##
## Outputs:
## 
## The function returns None, but prints when it is waiting for each license, and the total time elapsed. 
##
## Example run: 
##
## >> force_license(["3D", "Spatial", "Network"])
## Waiting for 3D
## Waiting for Spatial 
## Waiting for Network 
## All licenses checked out. Completed in 0:12:35
## >> 
def force_license(list_of_licenses):
    start_time = time.time()
    not_checked_out = []
    for license in list_of_licenses:
        print ("Waiting for {}".format(license))
        while arcpy.CheckExtension(license) != 'Available':
            time.sleep(0.001)
        result = arcpy.CheckOutExtension(license)
        if result != "CheckedOut":
            not_checked_out.append(license)
    # Use recursion to ensure that all licenses get checked out 
    if len(not_checked_out) > 0:
        return force_license(not_checked_out)
    else:
        end_time = time.time()
        t = gt.readable_time(start_time, end_time) 
        print("All licenses checked out. Completed in {}:{}:{}".format(t["hh"], t["mm"], t["ss"]))

## make_identical_tif_extents: list(String) String String --> list(String) 
##
## Description:
##
## Takes in a list of GeoTIFF files and processes them to all have identical projection, XY resolution, and extents. Very useful if doing 
## array work with a set of images. 
##
## Requirements: 
## 
## Requires spatial analyst and 3D analyst licenses. (Use force_license(["3D", "Spatial"]) to check them out)
##
## Inputs: 
## 
## tif_list:            A list of filepaths of valid GeoTIFF files. Can either be fullpaths or partial paths. 
## 
## working_directory:   A folder to store the intermediate TIFF files. 
##
##
## Outputs:
## 
## Returns a list of filepaths to GeoTIFF files that are the processed tiff files. 
## Length of output should be the same as input_tif_list. 
##
##
## 

def make_identical_tif_extents(tif_list, temp_dir="tmp"):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
    start_time = time.time() 
    print("Setting extents to be identical on {} GeoTIFFS...".format(len(tif_list)))
    # Temporary variables 
    output_tif_list = [] 
    tif_list_fixed_extents = []
    tif_properties = {}
    cell_extentX = []
    cell_extentY = []
    coords = set()
    coords_str = set()
    coords_str_l = []
    coords_l = []
    all_top = []
    all_bottom = []
    all_left = []
    all_right = []
    outlines_unchanged = []
    arcpy.env.overwriteOutput = True 
    main_coord_s = arcpy.Describe(tif_list[0]).spatialReference
    
    # Load tif properties that we care about into dictionary 
    for a_tif in tif_list:                                    
        coord, csX, csY = (arcpy.Describe(a_tif).spatialReference,
                           arcpy.GetRasterProperties_management(a_tif, "CELLSIZEX"),
                           arcpy.GetRasterProperties_management(a_tif, "CELLSIZEY"))

        cell_extentX.append(float(str(csX)))
        cell_extentY.append(float(str(csY)))
        coords.add(coord)
        coords_str.add(coord.name)
        coords_str_l.append(coord.name)
        coords_l.append(coord)
        tif_properties[a_tif] = [coord.name]
    print("Step 1/4: Setting projections to be identical....")
    # Reproject rasters to one projection
    j = 0
    for a_tif in tif_properties.keys():
        desc = arcpy.Describe(a_tif).baseName
        if not os.path.isfile(os.path.join(temp_dir, desc + "_reproject.tif")):
            arcpy.ProjectRaster_management(a_tif, os.path.join(temp_dir, desc + "_reproject.tif"), main_coord_s)
        tif_properties[os.path.join(temp_dir, desc + "_reproject.tif")] = main_coord_s
                                                                           
        del tif_properties[a_tif]
        
    print("Step 2/4: Setting cell sizes to be identical....")
    
    # Set cell sizes to be identical if necessary    
    if len(set(cell_extentX)) > 1 or len(set(cell_extentY)) > 1:
        x_freq = max(set(cell_extentX), key=cell_extentX.count)
        y_freq = max(set(cell_extentY), key=cell_extentY.count)
        tif_list = tif_properties.keys()
        for a_tif in tif_list: 
            desc = arcpy.Describe(a_tif).baseName
            if float(str(arcpy.GetRasterProperties_management(a_tif, "CELLSIZEX"))) != x_freq or float(str(arcpy.GetRasterProperties_management(a_tif, "CELLSIZEY"))) != y_freq:
                if not os.path.isfile(os.path.join(temp_dir, desc + "_resample.tif")):
                    arcpy.Resample_management(a_tif,os.path.join(temp_dir, desc + "_resample.tif"), x_freq)
                tif_properties[os.path.join(temp_dir, desc + "_resample.tif")] = main_coord_s
                try:
                    del tif_properties[a_tif]
                except:
                    pass
    # Generate polygon extent shape for each tif
    print("Step 3/4: Generating minimum bounding polygon....")
    for a_tif in tif_properties.keys():
        desc = arcpy.Describe(a_tif).baseName
        arcpy.RasterDomain_3d(a_tif, os.path.join(temp_dir, desc + "_Outline_notproj.shp"), "POLYGON")
        arcpy.Project_management(os.path.join(temp_dir, desc + "_Outline_notproj.shp"),os.path.join(temp_dir, desc + "_Outline.shp"), main_coord_s)
        outlines_unchanged.append(os.path.join(temp_dir, desc + "_Outline.shp"))
    for x in range(0, len(outlines_unchanged)):
        this_outline = outlines_unchanged[x]
        if x == 0:
            outline_to_clip_to = outlines_unchanged[x + 1]
            outline_to_save_to = os.path.join(temp_dir, "final_cutout_tmp.shp")
            arcpy.Clip_analysis(this_outline, outline_to_clip_to, outline_to_save_to)
            arcpy.CopyFeatures_management(outline_to_save_to, os.path.join(temp_dir, "final_cutout.shp"))
        else:
            outline_to_clip_to = os.path.join(temp_dir, "final_cutout.shp")
            outline_to_save_to = os.path.join(temp_dir, "final_cutout_tmp.shp")
            arcpy.Clip_analysis(this_outline, outline_to_clip_to, outline_to_save_to)
            arcpy.CopyFeatures_management(outline_to_save_to, outline_to_clip_to)
    desc = arcpy.Describe(os.path.join(temp_dir, "final_cutout.shp"))
    bounding = "{} {} {} {}".format(desc.extent.XMin, desc.extent.YMin, desc.extent.XMax, desc.extent.YMax)
    print("Step 4/4: Clipping rasters to minimum bounding polygon....")
    for a_tif in tif_properties.keys():
        desc = arcpy.Describe(a_tif).baseName
        ## Reproject the shapefile to be the same projection as the input raster 
        coord_system = arcpy.Describe(a_tif).spatialReference 
        arcpy.Project_management(os.path.join(temp_dir, "final_cutout.shp"), os.path.join(temp_dir, "final_cutout_proj.shp"), main_coord_s)
        if not os.path.isfile(os.path.join(temp_dir, desc + "_clip.tif")):
            outExtract = arcpy.sa.ExtractByMask(a_tif, os.path.join(temp_dir, "final_cutout_proj.shp"))
            outExtract.save(os.path.join(temp_dir, desc + "_clip.tif"))
        tif_list_fixed_extents.append(os.path.join(temp_dir, desc + "_clip.tif"))
    end_time = time.time()
    t = gt.readable_time(start_time, end_time) 
    output_tif_list = tif_list_fixed_extents
    print("{} GeoTIFFs processed to have identical extents in {} days, {}:{}:{}".format(len(tif_list), t['dd'], t["hh"], t["mm"], t['ss']))
    
    return output_tif_list
    
## gdb_table_to_csv: String String Boolean --> None 
##
## Description:
## Takes in a geodatabase table and converts it to a CSV. 
##
## Requirements:
## None. 
## 
## Inputs:
## in_table: Path to a table contained within an ESRI file geodatabase. 
## 
## out_csv: Path to a CSV file that will be either created or overwritten.
##
## ordered: Boolean flag to specify if you would like to order the fields alphabetically. True will sort the fields and false will put the fields in the same order as the input table 


def gdb_table_to_csv(in_table, out_csv, ordered=True):
    fields = [n.name for n in arcpy.ListFields(in_table)]
    if ordered:
        fields = sorted(fields)
    f = open(out_csv, 'w')
    cursor = arcpy.SearchCursor(in_table)
    f.write(",".join(fields))
    f.write("\n")
    for row in cursor:
        line = ",".join([str(row.getValue(n)) for n in fields])
        f.write(line)
        f.write("\n")
    f.close()
    

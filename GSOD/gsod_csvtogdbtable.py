import arcpy, glob, os
arcpy.env.overwriteOutput = True
csvdir = r"Z:\Alex\GSOD_PROCESSED\csv"
gdbdir = r"Z:\Alex\GSOD_PROCESSED\gdb_final"
for year in range(1929, 2019):
    print(year)
    csvs = glob.glob(csvdir + "\\" + str(year) + "*.csv")
    if not os.path.exists(gdbdir + "\\{}.gdb".format(year)):
        arcpy.CreateFileGDB_management(gdbdir, str(year) + ".gdb")
    cur_gdb = gdbdir + "\\{}.gdb".format(year)
    for csv in csvs:
        tbl_name = csv.split("\\")[-1].replace(".csv", "")[5:]
        arcpy.TableToTable_conversion(csv, cur_gdb, tbl_name)
        arcpy.MakeXYEventLayer_management(cur_gdb + "\\" + tbl_name,
                                          "LON", "LAT", tbl_name + "FLAYER")
        arcpy.CopyFeatures_management(tbl_name + "FLAYER",
                                      cur_gdb + "\\" + tbl_name + "_spatial")
        arcpy.Delete_management(cur_gdb + "\\" + tbl_name)

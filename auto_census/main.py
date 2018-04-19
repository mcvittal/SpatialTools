import os, sys, glob, arcpy
arcpy.env.overwriteOutput = True
## This script takes in a folder of census tabular data and 
## programatically joins the CSV files to a given shapefile. 

## Note: The folder must contain both the CSV file and the TXT header file. 


## VARIABLE MODIFICATION SECTION 

input_data_dir = r"C:\ajmcvitt\census\allprofiles"

# TODO: Check to make sure the keys in this dict line up with the first line of the headers.
# Provinces is correct: It lines up with the word(s) after "Profile of". Example below:
#
# 2016 Census Profiles Files / Profile of Provinces
#                                         ---------
boundary_files = {"Census Subdivisions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CSD\lcsd000b16a_e.shp",
                                         "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\CSD\lcsd000a16a_e.shp"},
                  "Census Disseminations Areas":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\DA\lda_000b16a_e.shp",
                                                 "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\DA\lda_000a16a_e.shp"},
                  "Provinces":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\Prov\lpr_000b16a_e.shp",
                               "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\Prov\lpr_000a16a_e.shp"},
                  "Aggergate Dissemination Areas":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\ADA\lada000b16a_e.shp",
                               "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\Prov\lpr_000a16a_e.shp"},
                  "Census Agricultural Regions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CAR\lcar000b16a_e.shp",
                               "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\Prov\lpr_000a16a_e.shp"},
                  "Census Consolidated Subdivisions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CCS\lccs000b16a_e.shp",
                               "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\Prov\lpr_000a16a_e.shp"},
                  "Census Consolidated Subdivisions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CCS\lccs000b16a_e.shp",
                               "Digital":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Digitial Boundary Files\Prov\lpr_000a16a_e.shp"},
                  "Census Divisions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CD\lcd_000b16a_e.shp"},
                  "Census Metropolitan Area & Census Agglomerations":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CMA\lcma000b16a_e.shp"},
                  "Census Tracts":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\CT\lct_000b16a_e.shp"},
                  "Census Disseminations Blocks":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\DB\ldb_000b16a_e.shp"},
                  "Designated places":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\Designated places\ldpl000b16a_e.shp"},
                  "Census Economic Regions":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\ER\ler_000b16a_e.shp"},
                  "Census Federal Electoral Districts":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\Fed\lfed000b16a_e.shp"},
                  "Census Population Centers":{"Cartographic":r"Z:\AShawa\Statistics Canada_Census 2016\Boundaries\Cartographic Boundary Files\Population centres\lpc_000b16a_e.shp"}
                  }

out_directory = r"C:\ajmcvitt\census\allprofiles\out"
temp_dir = r"C:\ajmcvitt\census\allprofiles\temp"


#out_directory = r"Z:\Stephanie\Census2016\TESTCENSUS"
#temp_dir = r"Z:\Stephanie\Census2016\TESTCENSUS\temp"


## DO NOT MODIFY BELOW THIS LINE UNLESS YOU ARE MAINTAINING THIS SCRIPT

csvs = glob.glob(input_data_dir + "\\*.csv")
population_raw_data = os.path.join(temp_dir, "PopulationData")


try:
        os.mkdir(out_directory)
except:
        pass

dictionary_directory = os.path.join(out_directory, "Census dictionaries")

try:
        os.mkdir(dictionary_directory)
except:
        pass

try:
        os.mkdir(population_raw_data)
except:
        pass

population_txt = []


print(" ****************** ")
print(" * PRE PROCESSING * ")
print(" ****************** ")

print("Splitting master census files into individual sheets")
for csv in csvs:
        print(csv)
        header_txt = csv.replace("data.csv", "header.txt")
        header_conn = open(header_txt, 'r')
        header_data = header_conn.read().split("\n")
        profile = header_data[0].split(" / ")[-1].replace("Profile of ", "").replace("(", "").replace(")", "").replace("&","")

        variables = {}
        geo = ""
        geo_l = ""
        all_txt = []
        # Generate individual header files
        for l in header_data[1:]:
                col_value = l.split(" ")[0]
                if "GEO UID" in l:
                        geo = col_value
                        geo_l = l
                        continue
                full_name = " ".join(l.split(" ")[1:]).strip()[1:].strip().replace("(", "").replace(")", "").replace("&","")

                census_sheet = "-".join(l.split("/")[0].split("-")[1:]).strip().replace("(", "").replace(")", "").replace("&","")

                if census_sheet not in variables.keys():
                        variables[census_sheet] = [geo]
                        f = open(os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)), 'a')
                        f.write("{}\n{}\n".format(header_data[0], geo_l))
                        f.close()
                variables[census_sheet].append(col_value)
                f = open(os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)), 'a')
                f.write("{}\n".format(l))
                f.close()
                if os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)) not in population_txt:
                        population_txt.append(os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)))
                if os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)) not in all_txt:
                        all_txt.append(os.path.join(temp_dir, "{}_{}_header.txt".format(profile, census_sheet)))
        # Read in the master CSV
        csv_conn = open(csv, 'r')
        csv_data = csv_conn.read().split("\n")
        csv_cols = csv_data[0].split(",")

        # Generate individual CSV files from generated header files
        for txt in all_txt:
                f = open(txt, 'r').read().split("\n")
                indexes = []
                for l in f:
                        if "COL" not in l:
                                continue
                        col_short = l.split("-")[0].strip()
                        try:
                                indexes.append(csv_cols.index('"' + str(col_short) + '"'))
                        except:
                                pass
                        try:
                                indexes.append(csv_cols.index( str(col_short)))
                        except:
                                pass
                txt_data = []
                for l in csv_data:
                        l = l.split(",")
                        try:
                                txt_data.append(",".join([l[x] for x in indexes]))
                        except:
                                pass
                f = open(txt.replace("_header.txt", "_data.csv"), 'w')
                try:
                        f.write("\n".join(txt_data))
                except:
                        print(txt_data)
                f.close()
                
                
        
print("Fixing population CSV files and generating census dictionaries")

try:
        arcpy.CreateFileGDB_management(population_raw_data, "Populationtables.gdb")
except:
        pass

for population in population_txt:
        data = open(population, 'r').read().split("\n")
        profile = data[0].split(" / ")[-1].replace("Profile of ", "").replace("(", "").replace(")", "").replace("&","")

        if "Age  Sex - Both sexes" not in population:
                continue
        data = data[1:]
        header_fixed = []
        header_dict = {}
        print(population)
        for l in data:
                l = l[6:].strip()
                if l == "GEO UID":
                        header_fixed.append("GEOUID")
                        header_dict["GEOUID"] = "GEO UID"
                        continue
                l = [i.strip() for i in l.split("/")]
                if l[-1] == "Total - Age groups and average age of the population - 100% data ; Both sexes":
                        header_fixed.append("TOT_POP")
                        header_dict["TOT_POP"] = "Total - Age groups and average age of the population - 100% data ; Both sexes"
                elif l[-1] == "Average age of the population ; Both sexes":
                        header_fixed.append("AVG_AGE")
                        header_dict["AVG_AGE"] = "Average age of the population ; Both sexes"
                elif l[-1] == "Total - Distribution (%) of the population by broad age groups - 100% data ; Both sexes":
                        header_fixed.append("TOT_DIST")
                        header_dict["TOT_DIST"] = "Total - Distribution (%) of the population by broad age groups - 100% data ; Both sexes"
                elif "over" in l:
                        header_fixed.append("OVER_" + l[2])
                        header_dict["OVER_" + l[2]] = l
                else:
                        h = "_".join(l[-1].split(" ")[:3]).upper() + "Y"
                        header_fixed.append(h)
                        header_dict[h] = l
        new_header = ",".join(header_fixed)
        csv = population.replace("header.txt", "data.csv")
        f = open(csv, 'r').read().split("\n")
        f[0] = new_header
        new_csv = open(population_raw_data + profile + ".csv", 'w')
        new_csv.write("\n".join(f))
        new_csv.close()
        try:
                os.mkdir(os.path.join(population_raw_data, "Population_dictionaries"))
        except:
                pass
        f = open(os.path.join(population_raw_data, "Population_dictionaries", profile + ".csv"), 'w')
        f.write("Abbreviated,Full\n")
        for k in header_fixed[:-1]:
                f.write("{},{}\n".format(k, header_dict[k]))
        f.close()
        arcpy.TableToTable_conversion(population_raw_data + profile + ".csv", population_raw_data + "/Populationtables.gdb/", profile.replace(" ", ""))

print(" ******************* ")
print(" *    PROCESSING   * ")
print(" ******************* ")
   
        
print("Beginning processing of individual census variables")                        


for csv in glob.glob(os.path.join(temp_dir, "*_data.csv")):
        ## Part 1:
        ##   Preparation of CSV file and generation of census dictionary 
        ##
        # Get the header 
        header = csv.replace("_data.csv", "_header.txt")
        header_data = open(header, 'r').read().split("\n")
        # Determine what census division this is 
        census_division = header_data[0]
        profile = header_data[0].split(" / ")[-1].replace("Profile of ", "").replace("(", "").replace(")", "").replace("&","")
        cartographic_shp, digital_shp = ("", "")
        current_gdb = ""
        census_sheet = " - ".join(header_data[-2].split(" / ")[0].split(" - ")[1:]).replace("(", "").replace(")", "").replace("&","")
        population_csv = ""
        flag = False
        for k in boundary_files.keys():
                if k in census_division:
                        # Save paths to boundary files
                        cartographic_shp = boundary_files[k]["Cartographic"]
                        #digital_shp = boundary_files[k]["Digital"]
                        #print(csv)
                        if census_sheet == "":
                                flag = True
                                break
                        print("Running census formatting on {} at level {}".format(census_sheet, k))
                        census_division = k
                        
                        try:
                                current_gdb = os.path.join(out_directory, k + ".gdb")
                                if not os.path.exists(current_gdb):
                                        arcpy.CreateFileGDB_management(out_directory, k + ".gdb")
                        except:
                                pass 
        
        if flag:
                continue
        # Exit if no boundary file found
        if cartographic_shp == "":
                #print(csv)
                #print(header)
                print("Error! No suitable boundary file found for {}".format(census_division))
                sys.exit(1)
        
        
        #print("Joining {} to the following files:\nCartographic: {}\nDigital: {}\n".format(census_sheet, cartographic_shp, digital_shp))
        print("[ 1 / 5 ] Shortening field names and generating census dictionary")
        corr_header = []
        corr_header_dict = {}
        full_nam_variables = {}
        for variable in header_data:
                # Determine if this line is one that contains a census variable
                if variable.startswith("COL"):
                        if False:
                                pass
                        else:
                                # Remove commas, since its going into a new CSV file
                                variable = "-".join(variable.split("-")[1:]).replace(",", " ")
                        
                                try:
                                        #print(variable)
                                        o_var = variable
                                        variable = variable.split(" / ")[-1].strip()
                                        full_nam_variables[variable] = o_var
                                        #print(variable)
                                except:
                                        variable = variable.strip()
                else:
                        continue
                # Generation of shortened census variable names
                variable_nospace = variable.replace(" ", "").strip()
                if len(variable_nospace) > 10:
                        variable_wordlist = variable.replace("(", "").replace(")", "").replace("$", "").replace("%", "").split(" ")
                        variable_wordlist = filter(None, variable_wordlist)
                        if len(variable_wordlist) > 4:
                                x = 0
                                variable_trunc = "_".join([v.replace('.', '')[0] for v in variable_wordlist[:4]])
                                if len(variable_trunc.replace("_", "")) == 0:
                                        variable_trunc = "FIELD"
                                if variable_trunc not in corr_header_dict.keys():
                                        corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                        corr_header.append(variable_trunc)
                                else:
                                        while variable_trunc in corr_header_dict.keys():
                                                variable_trunc = "_".join([v.replace('.', '')[0] for v in variable_wordlist[:4]]) + str(x)
                                                x += 1
                                        
                                        corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                        corr_header.append(variable_trunc)
                        else:
                                n_undersc = len(variable_wordlist) - 1
                                n_char = int((10 - n_undersc ) / len(variable_wordlist)) - 1
                                variable_trunc = "_".join([v.replace('.', '')[:n_char] for v in variable_wordlist])
                                if len(variable_trunc.replace("_", "")) == 0:
                                        variable_trunc = "FIELD"
                                if variable_trunc not in corr_header_dict.keys():
                                        corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                        corr_header.append(variable_trunc)
                                else:
                                        x = 0
                                        while variable_trunc in corr_header_dict.keys():
                                                variable_trunc = "_".join([v.replace(".", '')[0] for v in variable_wordlist]) + str(x)
                                                x += 1
                                        corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                        corr_header.append(variable_trunc)
                        
                else:
                        variable_trunc = variable_nospace.replace("$", "").replace("%", "")
                        
                        if variable_trunc not in corr_header_dict.keys():
                                corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                corr_header.append(variable_trunc)
                        else:
                                x = 0
                                while variable_trunc in corr_header_dict.keys():
                                        variable_trunc = variable_nospace[:7] + str(x)
                                        x += 1
                                corr_header_dict[variable_trunc] = full_nam_variables[variable]
                                corr_header.append(variable_trunc)
                
        
        d = open(csv, 'r')
        data = d.read().split("\n")
        data[0] = ",".join(corr_header)
        data = "\n".join(data)
        # Arcmap is very picky about special characters.
        fname = census_sheet.replace(" ", "_").replace("/", "_")
        fname = fname.replace(".", "").replace("_", "").replace("-","") 
        f = open(os.path.join(out_directory, fname  + "data.csv"), 'w')
        f.write(data)
        f.close()
        f = open(os.path.join(dictionary_directory, census_division + "_" + fname + ".csv"), 'w')
        # Write out the census dictionary
        f.write("Abbreviated fieldname,Full fieldname\n")
        for k in corr_header:
                f.write("{},{}\n".format(k, corr_header_dict[k]))
        f.close()
        d.close()
        del d
        del f
        
        ## Part 2: Joining of fields to the shapefile 
        ##
        ##
        # Get the GEO ID field
        for k in corr_header_dict:
                if "GEOUID" in k:
                        geouid = k
                        break
        id_field = [x for x in [f.name for f in arcpy.ListFields(cartographic_shp)] if x.endswith("Long")][0]

        try:        
                fname_safe = fname.replace("&", "").replace("(", "").replace(")", "")
                if fname_safe == "":
                        continue
                print("[ 2 / 5 ] Converting CSV file to ESRI GDB table")
                
                arcpy.TableToTable_conversion(out_directory + "\\" +  fname + "data.csv", current_gdb, fname_safe + "data")
                os.remove(out_directory + "\\" +  fname + "data.csv")
                print("[ 3 / 5 ] Copying original shapefile to GDB for joining")
                
                arcpy.CopyFeatures_management(cartographic_shp, current_gdb + "\\{}".format(fname_safe))
                print("[ 4 / 5 ] Joining Populationdata to shapefile")
                if "Age" in fname and "Sex" in fname and ("TotalSex" in fname or "BothSex" in fname):
                        print("Skipping")
                else:
                        arcpy.JoinField_management(current_gdb + "\\{}".format(fname_safe),
                                                   id_field, population_raw_data + "\\Populationtables.gdb\\" + profile.replace(" ", ""),
                                                   "GEOUID")
                print("[ 5 / 5 ] Joining current census variables to shapefile")
                arcpy.JoinField_management(current_gdb + "\\{}".format(fname_safe),
                                           id_field, current_gdb + "\\" + fname_safe  + "data", geouid)
                #arcpy.Delete_management(current_gdb + "\\" + fname_safe  + "data")
                try:
                        os.rename(csv, csv.replace("raw\\", "raw\\processed\\"))
                        os.rename(csv.replace("data.csv", "header.txt"),
                                  csv.replace("data.csv", "header.txt").replace("raw\\", "raw\\processed\\"))
                except:
                        pass
                print("Done. Joined output in " + current_gdb + "\\" + fname_safe)
        except Exception as e:
                print(str(e))
                print("Failed. Moving to next variable")

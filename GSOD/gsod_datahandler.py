import glob, os, sys

csv_master_guide = "isd-history.csv"
output_directory = os.getcwd()
master_file_conn = open(csv_master_guide, 'r')

master_file = master_file_conn.read().split("\n")

header = master_file[0]
data = master_file[1:]

master_dict = {}
v = 0 
i = 0 
c = 0 
for stn in data:
        c += 1
        stn = stn.replace('"', "").split(",")
        usaf = stn[0]
        
        try:
                wban = stn[1]
        except:
                pass
        try:
                ctry = stn[3] 
                state = stn[4]
                icao = stn[5] 
                lat = stn[6]
                lon = stn[7]
                begin = stn[9]
                try:
                        begin_y = int(begin[:4])
                except:
                        continue
                begin_m = begin[4:6]
                begin_d = begin[6:]
                end = stn[10]
                end_y = int(end[:4])
                end_m = end[4:6]
                end_d = end[6:]
                name = '"' + stn[2] + '"'
                print(" [ {} / {} ] {}".format(c, len(data), name))
                # Print current name of station being processed.
                #print(name)
                elev = stn[10]
        except:
                continue
        # Generate a blank dictionary
        date_dict = {}
        for m in range(1, 13):
                if m not in date_dict.keys():
                        date_dict[m] = {}
                for d in range(1, 32):
                        date_dict[m][d] = 999.9
                        if m in [1, 3, 5, 7, 8, 10, 12]:
                                continue
                        elif m == 2 and d > 29:
                                del date_dict[m][d]
                        elif m in [4, 6, 9, 11] and d > 30:
                                del date_dict[m][d]
        for year in range(begin_y, end_y + 1):
                # Generate a path to an OP file.
                op_file = os.path.join("Z:\\World\\GSOD\\{}\\{}\\{}-{}-{}.op".format(ctry, year, usaf, wban, year))
                #print(op_file)
                if os.path.isfile(op_file):
                        # Determined filename is valid.
                        v += 1
                        op_file_conn = open(op_file, 'r')
                        op_dict = {}
                        op_file_data = op_file_conn.read().split("\n")[1:]
                        allvars = {}
                        varl = ["temp",
                                "dewpoint",
                                "mean_sealevel_pressure",
                                "mean_station_pressure",
                                "mean_visibility",
                                "mean_windspeed",
                                "max_windspeed",
                                "max_windgust",
                                "max_temperature",
                                "min_temperature",
                                "total_precipitation_liquid",
                                "total_precipitation_snow"]
                        for avar in varl:
                                allvars[avar] = date_dict.copy()
                        # Store the blank dictionary in new copies
                        temp_dict = date_dict.copy()
                        dewpoint_dict = date_dict.copy()
                        mean_sealevel_pressure_dict = date_dict.copy()
                        mean_station_pressure_dict = date_dict.copy()
                        mean_visibility_dict = date_dict.copy()
                        mean_windspeed_dict = date_dict.copy()
                        max_windspeed_dict = date_dict.copy()
                        max_windgust_dict = date_dict.copy()
                        max_temperature_dict = date_dict.copy()
                        min_temperature_dict = date_dict.copy()
                        total_precipitation_liquid_dict = date_dict.copy()
                        total_precipitation_snow_dict = date_dict.copy()
                         
                        for date_data in op_file_data:
                                if len(date_data) < 130:
                                        continue
                                stnNum = int(date_data[:7].strip())
                                wban = int(date_data[7:13].strip())
                                year = int(date_data[14:18])
                                month = int(date_data[18:20])
                                day = int(date_data[20:22])
                                temp = float(date_data[24:30].strip()) # Fahrenheit
                                allvars["temp"][month][day] = temp
                                
                                dewpoint = float(date_data[35:41].strip()) # Fahrenheit
                                allvars["dewpoint"][month][day] = dewpoint
                                
                                mean_sealevel_pressure = float(date_data[46:52]) #Millibars
                                allvars["mean_sealevel_pressure"][month][day] = mean_sealevel_pressure

                                mean_station_pressure = float(date_data[57:63]) # Millibars
                                allvars["mean_station_pressure"][month][day] = mean_station_pressure
                                
                                mean_visibility = float(date_data[68:73]) # Miles
                                allvars["mean_visibility"][month][day] = mean_visibility
                                
                                mean_windspeed = float(date_data[84:86]) # Knots
                                allvars["mean_windspeed"][month][day] = mean_windspeed
                                
                                max_windspeed = float(date_data[88:93]) # Knots
                                allvars["max_windspeed"][month][day] = max_windspeed

                                max_windgust = float(date_data[95:100]) # Knots
                                allvars["max_windgust"][month][day] = max_windgust

                                max_temperature = float(date_data[102:108]) # Fahrenheit
                                allvars["max_temperature"][month][day] = max_temperature
                                
                                min_temperature = float(date_data[110:116]) # Fahrenheit
                                allvars["min_temperature"][month][day] = min_temperature

                                total_precipitation_liquid = float(date_data[118:123]) # Inches
                                allvars["total_precipitation_liquid"][month][day] = total_precipitation_liquid

                                total_precipitation_snow = float(date_data[125:130]) # Inches
                                allvars["total_precipitation_snow"][month][day] = total_precipitation_snow

                        
                        for avar in varl:
                                cur_csv = os.path.join(output_directory, "csv", "{}_{}.csv".format(year, avar))
                                line = [lat, lon, name, ctry]
                                if os.path.exists(cur_csv):
                                        f = open(cur_csv, 'a')
                                else:
                                        f = open(cur_csv, 'w')
                                        line_header = "LAT,LON,NAME,CTRY".split(",")
                                        for m in sorted(date_dict.keys()):
                                                for d in sorted(date_dict[m].keys()):
                                                     line_header.append("{}_{}".format(m, d))
                                        line_header = ",".join(line_header)
                                        f.write(line_header)
                                for m in sorted(date_dict.keys()):
                                        for d in sorted(date_dict[m].keys()):
                                                line.append(allvars[avar][m][d])
                                line = [str(l) for l in line]
                                f.write("\n")
                                f.write(",".join(line))
                                f.close()
                else:
                        #Determined filename is invalid and does not exist in the system.
                        i += 1 
# Show ratio of valid to invalid filenames.
print(i / float(v + i ) * 100)
        


#       stnNum = int(stn[:7].strip())
#       wban = int(stn[7:13].strip())
#       year = int(stn[

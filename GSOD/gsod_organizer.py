#!/usr/bin/env python3
import glob, os, sys, shutil
# This script takes all the extracted .gz files from the NOAA
# tarballs and moves them into appropriate country-level folders
# separated by years
input_folder = os.path.join(os.getcwd(), "ftp.ncdc.noaa.gov/pub/data/decompress")
output_folder = os.path.join(os.getcwd(), "ftp.ncdc.noaa.gov/pub/data/organized")
input_csv = os.path.join(os.getcwd(), "isd-history.csv")
data = {}
os.chdir(input_folder)
with open(input_csv, "r") as f:
    for line in f:
        line = line.split(",")

        if "USAF" in line[0]:
            header = line
            for i in header:
                data[i.replace('"', "")] = []
            print(data)

            continue
        for x in range(0, len(line)):
            data[header[x].replace('"', "")].append(line[x])
        cur_USAF = data["USAF"][-1].replace('"', '')
        cur_WBAN = data["WBAN"][-1]
        cur_CTRY = data["CTRY"][-1].replace('"', '')
        if cur_CTRY not in ["MX", "CA", "US"]:
            continue
        print(cur_CTRY)
        cur_dir_gzs = glob.glob(os.path.join(input_folder, f"*{cur_USAF}*.op.gz"))
        # print(cur_dir_gzs)
        for gz in cur_dir_gzs:
            if cur_CTRY == "":
                cur_CTRY = "OTHER"
                try:
                    os.mkdir(os.path.join(output_folder, "OTHER"))
                except:
                    #print("Oh no! #1")
                    #print(sys.exc_info())
                    pass
            else:
                try:
                    os.mkdir(os.path.join(output_folder, cur_CTRY))
                except:
                    #print("Oh no! #2")
                    #print(sys.exc_info())
                    pass
            year = gz.split("-")[-1].replace(".op.gz", "")
            # print(year)
            try:
                os.mkdir(os.path.join(output_folder, f"{cur_CTRY}/{year}"))
            except:
                #print("Oh no! #3")
                #print(sys.exc_info())
                pass
            # print(year)
            try:
                #print(gz, os.path.join(cur_CTRY, year, gz))
                gz = gz.split("/")[-1]
                shutil.copyfile(gz, os.path.join(output_folder,cur_CTRY, year, gz))
            except:
                #print("Oh no! #4")
                print(sys.exc_info())
                pass

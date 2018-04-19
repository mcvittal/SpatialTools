#!/usr/bin/env bash

station_files="ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.csv"

main_ftp="ftp://ftp.ncdc.noaa.gov/pub/data/gsod"

wget $station_files -o "isd-history.csv"

wget --no-parent --accept “*.tar” -r $main_ftp

cd ftp.ncdc.noaa.gov/pub/data/gsod
for atar in */*.tar; do tar -xvf $atar; done
mkdir decompress
for agz in *.gz; do mv $agz decompress/; gunzip decompress/$agz; done

cd ../../..

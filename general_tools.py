from datetime import datetime, timedelta 
## readable_time: Int Int --> Dict{"hh":String, "mm":String, "ss":String)
##
## Description: 
## Takes in a start time in seconds and end time in seconds, and produces a dictionary containing 
## a readable time in hours minutes seconds. 
##
## Requirements:
## start_time <= end_time 
##
## Inputs:
## start_time:  Time that a process started 
## end_time:    Time that a process ended. 
##
## Outputs:
## Returns a dict with four indices. 
## 
## 
## Example: 
##
## >> start = time.time()
## >> time.sleep(76)
## >> end = time.time() 
## >> t = readable_time(start, end)
## >> t["hh"]
## "00"
## >> t["mm"]
## "01"
## >> t["ss"]
## "16"
## >> 

def readable_time(start_time, end_time):
    elapsed = end_time - start_time 
    sec = timedelta(seconds=elapsed) 
    d = datetime(1,1,1) + sec 
    
    t = {}
    t["dd"] = str(int(d.day - 1))
    t["hh"] = str(int(d.hour))
    t["mm"] = str(d.minute)
    t["ss"] = str(d.second)
    for k in t:
        if len(t[k]) == 1:
            t[k] = "0{}".format(t[k])
    return t 


from collections import defaultdict
from run_procpip import run_procpip
from caculate_distance import write_to_txt
import time
import os

def buildtime(path,build_dir,map_file):
    buildorder=[]
    for i in path:
        if i == 0:
            continue
        buildorder.append(map_file[i])
    print(buildorder)
    timelist = defaultdict(list)
    timecount = 0
    for n in range(0,1):
        comm = "make clean"
        run_procpip(comm,build_dir)
        for config in buildorder:
            num = 0
            timecm = time.time()
            for i in config:
                if i == "-":
                    item = config[num:]
                    command = "./configure " + item.split(".json")[0]
                    run_procpip(command,build_dir)
                    break
                else:
                    num = num +1
            timeCO = time.time()-timecm
            command = "make"
            timeA = time.time()
            run_procpip(command,build_dir)
            timeB = time.time()-timeA
            timelist[config.split(".json")[0]].append(timeB)
            timelist[config.split(".json")[0]].append(timeCO)
            timecount = timecount+ timeB 
        timelist["Timecount"].append(timecount)
        timecount = 0
    avg = 0
    for item in timelist["Timecount"]:
        avg = avg + item
    avg = avg / len(timelist["Timecount"])
    timelist["AvgTime"].append(str(avg))
    return timelist

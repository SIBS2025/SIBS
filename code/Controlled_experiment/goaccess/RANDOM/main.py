from collections import defaultdict
from run_procpip import run_procpip
import random
import time
import os
import re

def write_to_txt(directory, data, file_name):

    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")

def extract_id_configs(folder_path):

    id_configs_mapping = {}
    for filename in os.listdir(folder_path):
        match = re.match(r'C(\d+)\s+(.+)\.json', filename)
        if match:
            id = match.group(1)
            configs = match.group(2)
            id_configs_mapping[id] = configs
    return id_configs_mapping

def buildtime(random_sequence, build_dir, map_file):
    print(map_file)
    buildorder = []
    for i in random_sequence:
        if i == 0:
            continue

        key = str(i)
        if key in map_file:
            buildorder.append(map_file[key])
        else:
            print(f"KeyError: {key} not found in map_file")
    print(buildorder)


    timelist = defaultdict(list)
    for n in range(1): 
        comm = "make clean"
        run_procpip(comm, build_dir)
        timecount = 0
        for config in buildorder:
            timecm = time.time()
            command = "./configure " + config
            run_procpip(command, build_dir)
            timeCO = time.time() - timecm

            command = "make"
            timeA = time.time()
            run_procpip(command, build_dir)
            timeB = time.time() - timeA

            timelist[config].append(timeB)
            timelist[config].append(timeCO)
            timecount += timeB

        timelist["Timecount"].append(timecount)

    avg = sum(timelist["Timecount"]) / len(timelist["Timecount"])
    timelist["AvgTime"].append(str(avg))
    return timelist

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.getcwd())
    build_dir = os.path.join(parent_dir, "goaccess/")
    folder_path = os.path.join(build_dir, "Json")
    id_configs_mapping = extract_id_configs(folder_path)

    for id, configs in id_configs_mapping.items():
        print(f'id: {id}, configs: {configs}')

    for k in range(1, 4):
        random_sequence = random.sample(range(1, 21), 20)
        print(random_sequence)
        timelist = buildtime(random_sequence, build_dir, id_configs_mapping)
        write_to_txt(os.getcwd(), timelist, f"Timecount{k}.txt")

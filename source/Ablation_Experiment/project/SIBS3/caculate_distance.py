import os
import json
import re
import math
import numpy as np
from collections import defaultdict
import subprocess
import filecmp
# from analyzer import compute_config_distance

def write_to_txt(directory, data, file_name):
   
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")

def calculate_distance(graph1, graph2):
    
    len_a = sum(1 + len(deps) for deps in graph1.values())
    len_b = sum(1 + len(deps) for deps in graph2.values())

    count_difference = 0
    matched_deps = 0

    for target, deps in graph1.items():
        if target in graph2:
            if str(deps) not in str(graph2[target]):
                count_difference += len(deps)

            else:
                matched_deps += 1 + len(deps)
        else:
            count_difference += len(deps)

    distance = abs(len_b - matched_deps) + count_difference
    percentage = round(100 * (len_a - count_difference + matched_deps) / (len_a + len_b))
    return distance, percentage

def calculate_all_distances(build_dir,length):
    matrix = np.zeros((length+1, length+1), dtype=np.int32)
    map = {}
    
    file_list = os.listdir(os.path.join(build_dir, "CJson"))
    distances = []
    
    for file1 in file_list:
        with open(os.path.join(build_dir, "CJson", file1), "r") as f1:
           graph1 = json.load(f1)
	
        distancelist = defaultdict(list)
        total_distance, total_percentage, comparisons = 0, 0, 0
        min_distance, max_distance = float('inf'), float('-inf')
        closest_file, farthest_file = None, None

        for file2 in file_list:
            if file1 == file2:
                continue
            
            with open(os.path.join(build_dir, "CJson", file2), "r") as f2:
               graph2 = json.load(f2)
            
            distance, percentage = calculate_distance(graph1, graph2)
            #distance=compute_config_distance(graph1, graph2)
            
            print(file1,file2)
            a = int(re.search(r"C(\d+)", file1).group(1))
            b = int(re.search(r"C(\d+)", file2).group(1))

            map[a] = file1
            map[b] = file2
            matrix[a, b] = distance
            matrix[b, a] = distance
            
            total_distance += distance
            
            comparisons += 1

            if distance < min_distance:
                min_distance = distance
                closest_file = file2
            if distance > max_distance:
                max_distance = distance
                farthest_file = file2

        for file2 in file_list:
            if file1 == file2:
                continue
            a = int(re.search(r"C(\d+)", file1).group(1))
            b = int(re.search(r"C(\d+)", file2).group(1))
            path = os.path.join(build_dir,"configs")
            if(a and b):
                if len(os.listdir(path)) == 0 :
                    continue
                filea = f"{path}/config{a}.h"
                fileb = f"{path}/config{b}.h"
                k = filecmp.cmp(filea, fileb)
                print(filea,fileb,k)
                if k == False:
                    matrix[a,b] = max(matrix[a,0],matrix[b,0])
                    matrix[b,a] = matrix[a,b]
           
            distancelist[f"{file1} - {file2}"].append(matrix[a,b])
        
        avg_distance = total_distance / comparisons
        #avg_percentage = round(total_percentage / comparisons)
        distancelist["avg_distance"].append(avg_distance)
        distancelist["closest_file"].append(closest_file)
        distancelist["min_distance"].append(min_distance)
        distancelist["farthest_file"].append(farthest_file)
        distancelist["max_distance"].append(max_distance)

        write_to_txt(os.path.join(build_dir, "CDistance"), distancelist, file1)

    return matrix,map

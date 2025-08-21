import os
import json
import re
import math
import numpy as np
from collections import defaultdict
import subprocess

            
def write_to_txt(Dir,lists,name):
    with open (Dir+name,'w') as f:
        for target,i in lists.items():
            f.writelines(str(target)+str(i)+'\n')
        f.close
        
def calculate_distance(graph1, graph2):
    """计算两个依赖图之间的距离和相似度百分比"""
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

def calculate_all_distances(buildDir,length):
    matrix = np.zeros((length+1, length+1), dtype=np.int32)
    map = {}
    """计算所有文件之间的依赖距离"""
    filelist = os.listdir(buildDir +"CJson")
    firstonfig = str()
    disavg = -1
    dis = []
    for fileitem1 in filelist:
        file1 = open(buildDir +"CJson/"+fileitem1,"r")
        makegraph1 = json.load(file1)
        distancelist = defaultdict(list)
        countdis = 0
        countper = 0
        i = 0
        Secstr = str()
        mindis = -1
        maxdis = -1
####### calculate all distance ,average dis, min dis #######
        for fileitem2 in filelist:

            if fileitem2 != fileitem1:
                file2 = open(buildDir +"CJson/"+fileitem2,"r")
                makegraph2 = json.load(file2)
                distance,per = calculate_distance(makegraph1,makegraph2)
                distancelist[fileitem1+" - " + fileitem2].append(str(distance))
                a = int(re.search(r"C(\d+)", fileitem1).group(1))
                b = int(re.search(r"C(\d+)", fileitem2).group(1))
                map[a] = fileitem1
                map[b] = fileitem2
                matrix[a][b] = distance
                matrix[b][a] = distance
                # dis.append(per)
                i = i +1
                countper = countper +per
                countdis = countdis + distance
                if mindis == -1:
                    mindis = distance
                    maxdis = distance
                    firststr = fileitem1
                    Secstr = fileitem2
                else:
                    if mindis > distance:
                        mindis = distance
                        Secstr = fileitem2
                    if maxdis < distance:
                        maxdis = distance
        avgper = round(countper / i)
        dis.append(avgper)
        countavg = countdis / i
        distancelist["avg"].append(countavg)
        distancelist["Secstr"].append(Secstr)
        distancelist["mindis"].append(str(mindis))
        distancelist["maxdis"].append(str(maxdis))
        write_to_txt(buildDir + "CDistance/", distancelist,fileitem1)
        
    return matrix,map

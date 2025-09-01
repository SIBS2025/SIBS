import os
import time
import configuration as cf
import tools
import json
import re
from collections import defaultdict
from create_dependencies import run_config_and_clean
import caculate_distance as cd 
from buildtime import buildtime

def readdeps(firstconfig,buildDir):
    if".json" not in firstconfig:
        firstconfig = firstconfig +".json"
    f = open(buildDir + "CDistance/" + firstconfig,"r")
    dislist = defaultdict(list)
    for lists in f.readlines():
        item , target = lists.split("[")
        target = re.findall(r"'(.*?)'", target, re.DOTALL)
        dislist[item].append(target)
    return dislist

def minbuid(buildDir):
    # filelist = os.listdir(buildDir +"/Json")
    filelist = os.listdir(buildDir +"CJson")
    firstonfig = str()
    dismin = 0
    dis = []
    for fileitem1 in filelist:
        file1 = open(buildDir +"/CJson/"+fileitem1,"r")
        makefile = json.load(file1)
        lenmakefile = 0
        for target,deps in makefile.items():
            lenmakefile = lenmakefile + len(deps) + 1
            i = 1
            for dep in deps:
                if dep == "-O0":
                    lenmakefile = lenmakefile - 5*len(deps)/6
                if dep == "-O1" or dep == "-O":
                    lenmakefile = lenmakefile - 4*len(deps)/6
                if dep == "-O2":
                    lenmakefile = lenmakefile - 3*len(deps)/6
                if dep == "-O3"or dep == "-Os":
                    lenmakefile = lenmakefile - 2*len(deps)/6
                if dep == "-Og":
                    lenmakefile = lenmakefile - 1*len(deps)/6
                else:
                    i = i+1
        if dismin == 0 :
            dismin = lenmakefile
            firstonfig = fileitem1
        elif dismin > lenmakefile:
            dismin = lenmakefile
            firstonfig = fileitem1
        elif dismin == lenmakefile:
            dis.append(fileitem1)
    dis.append(firstonfig)
    dis = sorted(dis,key=len,reverse=False)
    firstonfig = dis[0]
    return firstonfig

def BuddiOrderer(buildDir):
    firstconfig = minbuid(buildDir)
    buildorder = []
    buildorder.append(firstconfig.split(".json")[0])
    nodelist = os.listdir(buildDir+"Json")
    for i in  range(0,len(nodelist)-1):
        dislist = readdeps(firstconfig,buildDir)
        firstconfig = dislist["Secstr"][0][0]
        firstconfig = firstconfig.split(".json")[0]
        if firstconfig not in buildorder:
            buildorder.append(firstconfig)
        else:
            mindis = float(dislist["mindis"][0][0])
            maxdis = float(dislist["maxdis"][0][0])
            for config , dis in dislist.items():
                if config != "avg" and config != "mindis" and config != "maxdis" and config != "Secstr": 
                    item, config = config.split(" - ")
                    if config.split(".json")[0] in  buildorder:
                        continue
                    if float(dis[0][0]) == mindis:
                        secmindis = []##search all mindis
                        for config , dis in dislist.items():
                            if config != "avg" and config != "mindis" and config != "maxdis" and config != "Secstr":
                                if float(dis[0][0]) == mindis:
                                    config = config.replace(".json", "")
                                    num= 0
                                    for i in config:
                                        if i == "-":
                                            config = config[num:]
                                            secmindis.append(config)
                                            break
                                    else:
                                        num = num +1                                   
                        if len(secmindis)==1:
                            item1,item2 = secmindis.split(" - ")
                            if item2 not in buildorder:
                                firstconfig = item2.split(".json")[0]
                        else:
                            fir ={}
                            for item in secmindis:
                                first ,second = item.split(" - ")
                                num= 0
                                Dsec = str()
                                for i in first:
                                    if i == "-":
                                        first = first[num:]
                                        first = first.split(".json")[0]
                                        break
                                    else:
                                        num = num +1
                                num= 0
                                for i in second:
                                    if i == "-":
                                        Dsec = second[num:]
                                        break
                                    else:
                                        num = num +1
                                sec = []
                                count = 0
                                per = 0
                                sec= [x.strip() for x in Dsec.split('--') if x != ""]
                                for i in sec:
                                    if i in first:
                                        count = count +1
                                    per = round((count*100)/len(sec))
                                fir[second]=per 
                            fir = sorted(fir.items(),key=lambda x: x[1],reverse=True)
                            for i in range(0,len(fir)):
                                if fir[i][0] not in buildorder:
                                    firstconfig = fir[i][0].split(".json")[0]
                                    break     
                    elif maxdis > float(dis[0][0]):
                        maxdis = float(dis[0][0])
                        firstconfig = config
                    elif maxdis == float(dis[0][0]) and config not in buildorder:
                        firstconfig = config
                    elif i == len(nodelist)-2:
                        if float(dis[0][0]) == maxdis and config not in buildorder:
                            firstconfig = config
            buildorder.append(firstconfig.split(".json")[0])
    neworder = []
    for item in buildorder:
      match = re.search(r'C(\d+)', item)  
      neworder.append(int(match.group(1)))
    return neworder
    
def main():
    parent_dir = os.path.dirname(os.getcwd()) 
    build_dir = os.path.join(parent_dir,"goaccess1/")
    time_map = {}
    length = 20
    # print("Step 1: Generating configuration files...")
    #cf.generate_configs(build_dir,length)
    
    print("Step 2: Generating dependencies...")    
    filename = "C0 --.json"        
    folder_path = os.path.join(build_dir, "CJson")
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
      os.remove(file_path)
    folder_path = os.path.join(build_dir, "CDistance")
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
      os.remove(file_path)
    folder_path = os.path.join(build_dir, "configs")
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
      os.remove(file_path) 

    print("Step 3: Calculating distances and adjacency matrix...")
    time1=time.time()
    adjacency_matrix,map_file = cd.calculate_all_distances(build_dir,length)
    time_map["CalculatingTime"] = time.time()-time1
    matrix_str_list = adjacency_matrix.tolist()
    formatted_matrix_str = '\n'.join('[' + ', '.join(f'{elem:5}' for elem in row) + ']' for row in adjacency_matrix)
    with open('matrix.txt', 'w') as file:
        file.write(formatted_matrix_str)
    
    print("Step 4: Finding optimal configuration execution order...")
    time1=time.time()
    optimal_path = BuddiOrderer(build_dir)
    time_map["OrderingTime"] = time.time()-time1
    path = optimal_path
    path.insert(0,0)
    optimal_cost = sum(adjacency_matrix[optimal_path[i]][optimal_path[i + 1]] for i in range(len(optimal_path) - 1))
    with open('path.txt', 'w') as file:
        file.write(str(optimal_path))
        file.write("    ")
        file.write(str(optimal_cost))
        file.write("\n")
    
    print("Step 5: Calculating total build time...")
    timelist = buildtime(optimal_path, build_dir,map_file)
    tools.write_to_txt(os.getcwd(),timelist,"Timecount.txt")

    time_map["Sum"] = sum(float(value) for value in time_map.values())
    time_map["BuildTime"] = timelist["AvgTime"][0]
    time_map["AllTime"] = sum(float(value) for value in time_map.values()) -  time_map["Sum"] 
    time_map["Percentage"] = round(time_map["Sum"] / time_map["AllTime"] * 100, 2)
    tools.write_to_txt(os.getcwd(),time_map,"BUDDI_Summarize.txt")

if __name__ == "__main__":
    main()


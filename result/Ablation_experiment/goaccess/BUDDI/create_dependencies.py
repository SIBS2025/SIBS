import os
import json
import re
import math
import time
import numpy as np
from collections import defaultdict
from run_procpip import run_procpip
import subprocess


def list_files(directory):
    """列出目录中的所有文件"""
    return os.listdir(directory)

def run_config_and_clean(file_name, build_dir):
    """执行配置命令并清理构建目标"""
    CommandTime,AnalysisTime = 0,0
    for idx, char in enumerate(file_name):
        if char == "-":
            config_name = file_name[idx:].split(".json")[0]
            command = f"./configure {config_name}"
            run_procpip(command, build_dir)
            time1,time2 = clean_build_to_target_command(file_name, build_dir)
            CommandTime += time1
            AnalysisTime += time2
            break
    return CommandTime,AnalysisTime

def clean_build_to_target_command(pathname, build_dir):
    """清理构建目标并生成依赖关系"""
    time1 = time.time()
    command = f'cd {build_dir} && make -n --debug=basic'
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    time1 = time.time() - time1
    dict = {}
    targetsum = []
    lines = result.splitlines()
    i = 0
    time2 = time.time()
    while (i < len(lines)):
        if lines[i].strip().startswith('Must remake target'):
            index = lines[i].find('\'')
            target = lines[i][index+1:-2]
            targetsum.append(target)
            i += 1
            command = ''
            while i < len(lines) and lines[i].strip().startswith('Successfully remade target') == False:
                command += lines[i].strip()
                i += 1
            deps = re.split(" ", command)
            deps=[x.strip() for x in deps if x.strip() != '']
            dict[target] = deps
        i += 1
    time2 = time.time() - time2
    dict["target_sum"]=targetsum
    json_data = json.dumps(dict, indent=4)
    with open(build_dir+"CJson/"+pathname, "w") as f:
        f.write(json_data)
    return time1,time2

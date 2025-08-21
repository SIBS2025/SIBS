import os
import shutil
import subprocess
import time
import os
import sys
import shutil
from subprocess import Popen

sibs_folder = os.path.join(os.getcwd(),"SIBS") 
buddi_folder = os.path.join(os.getcwd(),"BUDDI") 
random_folder = os.path.join(os.getcwd(),"RANDOM") 
output_folder = "yourpathto/SIBS/code/Controlled_Experiment/reslut/project"                  #The directory you want to output
source_folder = os.path.join(os.getcwd(),"goaccess")       #source_folder
source_folder1 = os.path.join(os.getcwd(),"goaccess1")     #source_folder1

timecount_random_folder = os.path.join(output_folder, "Timecount_random")
timecount_folder = os.path.join(output_folder, "Timecount")
summarize_folder = os.path.join(output_folder, "Summarize")
matrix_folder = os.path.join(output_folder, "Matrix")
path_folder = os.path.join(output_folder, "Path")
os.makedirs(timecount_random_folder, exist_ok=True)
os.makedirs(timecount_folder, exist_ok=True)
os.makedirs(summarize_folder, exist_ok=True)
os.makedirs(matrix_folder, exist_ok=True)
os.makedirs(path_folder, exist_ok=True)


def execute_python_file(script_path, work_dir):
    if not os.path.isfile(script_path):
        print(f"Script not found: {script_path}")
        return False
    try:
        subprocess.run(["python3", script_path], cwd=work_dir, check=True)
        print(f"Executed: {script_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error while executing {script_path}: {e}")
        return False

def save_result_file(source_folder, source_file_name, prefix, iteration, target_folder):
    source_file = os.path.join(source_folder, source_file_name)
    if os.path.isfile(source_file):
        target_file = os.path.join(target_folder, f"{prefix}({iteration}).txt")
        shutil.move(source_file, target_file)
        print(f"Saved: {target_file}")
    else:
        print(f"No {source_file_name} found in {source_folder}")

def copy_and_rename_folder(source_folder):
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist!")
        return
    
    new_folder_name = source_folder + '1'
    
    if os.path.exists(new_folder_name):
        shutil.rmtree(new_folder_name)
        print(f"Removed existing destination folder {new_folder_name}")
    
    shutil.copytree(source_folder, new_folder_name)
    print(f"Folder copied and renamed successfully to {new_folder_name}")

def run_procpip(args, kwargs):
    sys.stdout.flush()

    proc = Popen(args, shell=True,cwd= kwargs)

    stdout, stderr  = proc.communicate()

    if proc.returncode != 0:
        print(stdout, '\n', stderr)
        sys.stdout.flush()
        
def main():
    number = 0
    if len(sys.argv) > 1:
        number = sys.argv[1]
        print(f"This is execution number {number}")
    else:
        print("No 'number' argument provided")

    print(f"--- Iteration {number} ---")
    i = number

    comm = "make clean"
    run_procpip(comm, source_folder)

    sibs_script = os.path.join(sibs_folder, "main.py")
    if execute_python_file(sibs_script, sibs_folder):
        save_result_file(sibs_folder, "matrix.txt", "matrix_sibs", i, matrix_folder)
        save_result_file(sibs_folder, "path2.txt", "path_sibs", i, path_folder)
        save_result_file(sibs_folder, "Timecount.txt", "Timecount_sibs", i, timecount_folder)
        save_result_file(sibs_folder, "Summarize.txt", "Summarize_sibs", i, summarize_folder)

    copy_and_rename_folder(source_folder)
    run_procpip(comm, source_folder1)

    buddi_script = os.path.join(buddi_folder, "main.py")
    if execute_python_file(buddi_script, buddi_folder):
        save_result_file(buddi_folder, "matrix.txt", "matrix_BUDDI", i, matrix_folder)
        save_result_file(buddi_folder, "path.txt", "path_BUDDI", i, path_folder)
        save_result_file(buddi_folder, "Timecount.txt", "Timecount_BUDDI", i, timecount_folder)
        save_result_file(buddi_folder, "BUDDI_Summarize.txt", "Summarize_BUDDI", i, summarize_folder)

    random_script = os.path.join(random_folder, "main.py")
    if execute_python_file(random_script, random_folder):
        for k in range(1, 11):
            save_result_file(
                random_folder,
                f"Timecount{k}.txt",
                f"Timecount_random_{i}_",
                k,
                timecount_random_folder,
            )
if __name__ == "__main__":
    main()

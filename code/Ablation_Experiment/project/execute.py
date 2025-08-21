import os
import shutil
import subprocess
import time
import os
import sys
import shutil
from subprocess import Popen

sibs_folder = os.path.join(os.getcwd(),"SIBS") 
sibs1_folder = os.path.join(os.getcwd(),"SIBS1")  
sibs2_folder = os.path.join(os.getcwd(),"SIBS2")  
sibs3_folder = os.path.join(os.getcwd(),"SIBS3")  
buddi_folder= os.path.join(os.getcwd(),"BUDDI")  
output_folder = "yourpathto/SIBS/code/Ablation_Experiment/reslut/project"    #The directory you want to output
source_folder = os.path.join(os.getcwd(),"goaccess")


timecount_folder = os.path.join(output_folder, "Timecount")
summarize_folder = os.path.join(output_folder, "Summarize")
matrix_folder = os.path.join(output_folder, "Matrix")
path_folder = os.path.join(output_folder, "Path")
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
        save_result_file(sibs_folder, "matrix.txt", "matrix_SIBS", i, matrix_folder)
        save_result_file(sibs_folder, "path2.txt", "path_SIBS", i, path_folder)
        save_result_file(sibs_folder, "Timecount.txt", "Timecount_SIBS", i, timecount_folder)
        save_result_file(sibs_folder, "Summarize.txt", "Summarize_SIBS", i, summarize_folder)
    
    
    # run_procpip(comm,source_folder)
    # buddi_script = os.path.join(buddi_folder, "main.py")
    # if execute_python_file(buddi_script, buddi_folder):
    #     save_result_file(buddi_folder, "matrix.txt", "matrix_BUDDI", i, matrix_folder)
    #     save_result_file(buddi_folder, "path.txt", "path_BUDDI", i, path_folder)
    #     save_result_file(buddi_folder, "Timecount.txt", "Timecount_BUDDI", i, timecount_folder)
    #     save_result_file(buddi_folder, "BUDDI_Summarize.txt", "Summarize_BUDDI", i, summarize_folder)   

    run_procpip(comm,source_folder)
    sibs1_script = os.path.join(sibs1_folder, "main.py")
    if execute_python_file(sibs1_script, sibs1_folder):
        save_result_file(sibs1_folder, "matrix.txt", "matrix_SIBS1", i, matrix_folder)
        save_result_file(sibs1_folder, "path2.txt", "path_SIBS1", i, path_folder)
        save_result_file(sibs1_folder, "Timecount.txt", "Timecount_SIBS1", i, timecount_folder)
        save_result_file(sibs1_folder, "Summarize.txt", "Summarize_SIBS1", i, summarize_folder)              
   
    run_procpip(comm,source_folder)
    sibs2_script = os.path.join(sibs2_folder, "main.py")
    if execute_python_file(sibs2_script, sibs2_folder):
        save_result_file(sibs2_folder, "matrix.txt", "matrix_SIBS2", i, matrix_folder)
        save_result_file(sibs2_folder, "path2.txt", "path_SIBS2", i, path_folder)
        save_result_file(sibs2_folder, "Timecount.txt", "Timecount_SIBS2", i, timecount_folder)
        save_result_file(sibs2_folder, "Summarize.txt", "Summarize_SIBS2", i, summarize_folder)
    
    run_procpip(comm,source_folder)
    sibs3_script = os.path.join(sibs3_folder, "main.py")
    if execute_python_file(sibs3_script, sibs3_folder):
        save_result_file(sibs3_folder, "matrix.txt", "matrix_SIBS3", i, matrix_folder)
        save_result_file(sibs3_folder, "path2.txt", "path_SIBS3", i, path_folder)
        save_result_file(sibs3_folder, "Timecount.txt", "Timecount_SIBS3", i, timecount_folder)
        save_result_file(sibs3_folder, "Summarize.txt", "Summarize_SIBS3", i, summarize_folder)
    
    execute_python_file(sibs_script, sibs_folder)
        
if __name__ == "__main__":
    main()


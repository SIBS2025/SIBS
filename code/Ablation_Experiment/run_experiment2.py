import os
import shutil
import subprocess
import psutil
import mmap
from multiprocessing import Pool

def set_memory_limit(process_id, memory_size_mb):
    try:
        process = psutil.Process(process_id)
        process.rlimit(psutil.RLIMIT_AS, (memory_size_mb * 1024 * 1024, psutil.RLIM_INFINITY))
        print(f"Memory limit set to {memory_size_mb} MB for process {process_id}")
    except Exception as e:
        print(f"Error setting memory limit: {e}")

def copy_folder_and_execute(src_folder, copy_number, memory_size_mb):

    new_folder = f"{src_folder}_copy_{copy_number}"
    print(f"Starting to copy folder {src_folder} to {new_folder}...")
    try:
        shutil.copytree(src_folder, new_folder)
        print(f"Successfully copied folder {src_folder} to {new_folder}")

        # Get current process PID and set memory limit
        process_id = os.getpid()
        set_memory_limit(process_id, memory_size_mb)

        # Run execute.py script, passing copy_number as argument
        execute_script(new_folder, copy_number)

    except Exception as e:
        print(f"Error during copy or execution: {e}")

def execute_script(folder, copy_number):
    execute_path = os.path.join(folder, 'execute.py')
    if os.path.exists(execute_path):
        try:
            print(f"Starting to execute {folder}/execute.py with argument {copy_number}...")
            # Run execute.py via subprocess, passing copy_number as command-line argument
            result = subprocess.run(
                ['python3', execute_path, str(copy_number)],
                cwd=folder,
                check=True,
                capture_output=True
            )
            print(f"Successfully executed {folder}/execute.py, output:\n{result.stdout.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute {folder}/execute.py, error:\n{e.stderr.decode()}")
    else:
        print(f"execute.py file not found in {folder}!")


def worker_function(copy_number, memory_size_mb):
    src_folder = "yourpathto/SIBS/code/Ablation_Experiment/project"  # Folder to be copied
    copy_folder_and_execute(src_folder, copy_number, memory_size_mb)

def main():
    num_copies = 16             # Number of copies to create
    memory_per_process_mb = 1024   # Memory allocated per process, in MB

    # Use process pool to handle tasks in parallel
    with Pool(processes=8) as pool:  # Allow up to x concurrent processes
        pool.starmap(worker_function, [(i, memory_per_process_mb) for i in range(1, num_copies + 1)])

if __name__ == "__main__":
    main()
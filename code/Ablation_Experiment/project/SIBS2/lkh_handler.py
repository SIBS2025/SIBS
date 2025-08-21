import subprocess
import os

class LKHHandler:
    def __init__(self, tsplib_file, par_file="lkh.par"):

        self.tsplib_file = tsplib_file
        self.par_file = par_file

    def create_parameter_file(self):

        with open(self.par_file, "w") as f:
            f.write(f"PROBLEM_FILE = {self.tsplib_file}\n")
            f.write("OUTPUT_TOUR_FILE = test_solution.txt\n")
            f.write("MAX_TRIALS = 100\n")
            f.write("RUNS = 10\n")
            f.write("TRACE_LEVEL = 1\n")

    def run_lkh(self):

        if not os.access('./LKH', os.X_OK):  
            subprocess.run(['chmod', '+x', './LKH'], check=True)

        self.create_parameter_file()
        
        result = subprocess.run(["./LKH", self.par_file], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"LKH execution failed: {result.stderr}")
        
        return result.stdout

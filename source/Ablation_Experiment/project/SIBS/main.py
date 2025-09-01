import os
import time
import configuration as cf
import tools
from create_dependencies import run_config_and_clean
import caculate_distance as cd 
from buildtime import buildtime
from tsplib_handler import TSPLibHandler
from lkh_handler import LKHHandler

def main():
    parent_dir = os.path.dirname(os.getcwd()) 
    build_dir = os.path.join(parent_dir,"goaccess/")
    time_map = {}
    tools.clear(build_dir)
    length = 20

    print("Step 1: Generating configuration files...")
    tools.create_folder(os.path.join(build_dir,"Json"))
    cf.generate_configs(build_dir,length)
    

    print("Step 2: Generating dependencies...")
    tools.create_json_file(build_dir)
    tools.create_folder(os.path.join(build_dir,"CJson"))
    tools.create_folder(os.path.join(build_dir,"configs"))
    config_dir = os.path.join(build_dir, "Json")
    CommandTime,AnalysisTime = 0,0
    for config_file in os.listdir(config_dir):
        if config_file.endswith(".json"):
            time1,time2 = run_config_and_clean(config_file, build_dir)
            CommandTime += time1
            AnalysisTime += time2
    time_map["CommandTime"]=CommandTime
    time_map["AnalysisTime"]=AnalysisTime


    print("Step 3: Calculating distances and adjacency matrix...")
    time1=time.time()
    adjacency_matrix,map_file = cd.calculate_all_distances(build_dir,length)
    time_map["CalculatingTime"] = time.time()-time1
    matrix_str_list = adjacency_matrix.tolist()
    formatted_matrix_str = '\n'.join('[' + ', '.join(f'{elem:5}' for elem in row) + ']' for row in adjacency_matrix)
    with open('matrix.txt', 'w') as file:
        file.write(formatted_matrix_str)
    

    print("Step 4: Finding optimal configuration execution order...")
    n = len(adjacency_matrix)                         
    # Output file paths
    tsplib_file = "test.tsp"
    #solution_file = tsplib_file.replace(".tsp", ".tour")  # Replace with the actual LKH-generated solution file path
    solution_file = "test_solution.txt"
    # Initialize TSPLibHandler and create TSPLIB file
    tsp_handler = TSPLibHandler(adjacency_matrix) 
    tsp_handler.write_tsplib_with_virtual_node(tsplib_file)
    # Initialize and run the LKH solver
    lkh_handler = LKHHandler(tsplib_file)
    time1=time.time()
    try:
        lkh_output = lkh_handler.run_lkh()
        print("LKH Output:", lkh_output)
    except RuntimeError as e:
        print(e)
    time_map["OrderingTime"] = time.time()-time1    
    
    # Parse the LKH solution
    optimal_path, shortest_distance = tsp_handler.parse_lkh_solution(solution_file)
    with open('path2.txt', 'w') as file:
        file.write(str(optimal_path))
        file.write(str(shortest_distance))

    print("Step 5: Calculating total build time...")
    timelist = buildtime(optimal_path, build_dir,map_file)
    tools.write_to_txt(os.getcwd(),timelist,"Timecount.txt")

    time_map["Sum"] = sum(float(value) for value in time_map.values())
    time_map["BuildTime"] = timelist["AvgTime"][0]
    time_map["AllTime"] = sum(float(value) for value in time_map.values()) -  time_map["Sum"] 
    time_map["Percentage"] = round(time_map["Sum"] / time_map["AllTime"] * 100, 2)
    tools.write_to_txt(os.getcwd(),time_map,"Summarize.txt")

if __name__ == "__main__":
    main()


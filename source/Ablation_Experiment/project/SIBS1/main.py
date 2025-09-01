import os
import time
import configuration as cf
import tools
from create_dependencies import run_config_and_clean
import caculate_distance as cd 
from order import greedy_hamiltonian_path
from buildtime import buildtime


def main():
    parent_dir = os.path.dirname(os.getcwd()) 
    build_dir = os.path.join(parent_dir,"goaccess/")
    time_map = {}
    length = 20


    # 3. 计算距离和邻接矩阵
    print("Step 3: Calculating distances and adjacency matrix...")
    time1=time.time()
    adjacency_matrix,map_file = cd.calculate_all_distances(build_dir,length)
    time_map["CalculatingTime"] = time.time()-time1
    matrix_str_list = adjacency_matrix.tolist()
    formatted_matrix_str = '\n'.join('[' + ', '.join(f'{elem:5}' for elem in row) + ']' for row in adjacency_matrix)
    with open('matrix.txt', 'w') as file:
        file.write(formatted_matrix_str)
    
    # 4. 确定最佳顺序
    print("Step 4: Finding optimal configuration execution order...")
    n = len(adjacency_matrix)
    if(n != 1):
        time1=time.time()
        shortest_distance, optimal_path = greedy_hamiltonian_path(n, adjacency_matrix)
        time_map["OrderingTime"] = time.time()-time1
        with open('path2.txt', 'w') as file:
            file.write(str(optimal_path))
            file.write(str(shortest_distance))

    
    print(f"Optimal path: {optimal_path} with distance: {shortest_distance}")
    
    # 5. 计算总时间
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


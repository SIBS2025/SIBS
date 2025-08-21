import numpy as np


class TSPLibHandler:
    def __init__(self, distance_matrix, virtual_node_cost=100000):

        self.distance_matrix = distance_matrix
        self.virtual_node_cost = virtual_node_cost
        self.num_nodes = len(distance_matrix)

    def write_tsplib_with_virtual_node(self, output_file):

        n = self.num_nodes

        # Create a new distance matrix including the virtual node
        tsp_matrix = np.full((n + 1, n + 1), self.virtual_node_cost, dtype=int)
        tsp_matrix[:n, :n] = self.distance_matrix  # Original matrix part
        tsp_matrix[n, 0] = tsp_matrix[0, n] = 0    # Distance from the virtual node to the start is 0
        tsp_matrix[n, n] = 0                       # Distance from the virtual node to itself is 0

        # Write to a TSPLIB format file
        with open(output_file, "w") as f:
            f.write("NAME: HPP_Converted\n")
            f.write("TYPE: TSP\n")
            f.write(f"DIMENSION: {n + 1}\n")
            f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
            f.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
            f.write("EDGE_WEIGHT_SECTION\n")
            for row in tsp_matrix:
                f.write(" ".join(map(str, row)) + "\n")
            f.write("EOF\n")

    def parse_lkh_solution(self, solution_file):

        with open(solution_file, 'r') as f:
            lines = f.readlines()

        # Locate the TOUR_SECTION part
        start_idx = lines.index("TOUR_SECTION\n") + 1
        end_idx = lines.index("-1\n")
        tour = list(map(int, lines[start_idx:end_idx]))

        # Remove the virtual node (node number is num_nodes + 1 since LKH numbering starts from 1)
        hpp_path = [node for node in tour if node <= self.num_nodes]

        # Adjust the path to start from node 1
        zero_idx = hpp_path.index(1)  # LKH numbering starts from 1
        hpp_path = hpp_path[zero_idx:] + hpp_path[:zero_idx]

        # Convert the path to 0-based indexing
        hpp_path = [node - 1 for node in hpp_path]

        # Calculate the total cost of the path
        total_cost = 0
        for i in range(len(hpp_path) - 1):
            total_cost += self.distance_matrix[hpp_path[i]][hpp_path[i + 1]]

        return hpp_path, total_cost

import create_dependencies 

def greedy_hamiltonian_path(n, adjacency_matrix):
    INF = float('inf')
    visited = [False] * n      # Track visited vertices
    path = []                  # Store the resulting path
    total_distance = 0         # Total length of the path

    # Start from vertex 0
    start_node = 0
    visited[start_node] = True
    path.append(start_node)

    # Iteratively select the nearest unvisited vertex
    for _ in range(n - 1):
        current_node = path[-1]
        min_distance = INF
        next_node = -1

        # Find the closest unvisited vertex
        for i in range(n):
            if not visited[i] and adjacency_matrix[current_node][i] < min_distance:
                min_distance = adjacency_matrix[current_node][i]
                next_node = i

        # If no next vertex is reachable, the path cannot be completed
        if next_node == -1:
            return float('inf'), []

        # Update path and accumulated distance
        visited[next_node] = True
        path.append(next_node)
        total_distance += min_distance

    # Ensure all vertices have been visited
    if len(path) != n:
        return float('inf'), []

    return total_distance, path
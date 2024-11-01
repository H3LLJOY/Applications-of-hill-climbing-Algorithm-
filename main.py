import numpy as np

def parse_input(file_path):
    with open(file_path, 'r') as file:
        # Parse the map matrix
        lines = file.readlines()
        n = len([line for line in lines if ',' in line])  # Number of nodes
        matrix = []

        for i in range(n):
            row = lines[i].strip().split(',')
            matrix.append([int(val) if val != 'N' else float('inf') for val in row])

        # Parse truck information
        trucks = []
        for line in lines[n:]:
            if line.strip():
                truck_id, capacity = line.strip().split('#')
                trucks.append({'id': truck_id, 'capacity': int(capacity), 'route': [], 'distance': 0})

    return np.array(matrix), trucks

def hill_climbing_algorithm(matrix, trucks):
    n = len(matrix)
    unvisited_nodes = list(range(1, n))  # Exclude starting node 'a'

    for truck in trucks:
        truck_route = [0]  # Start from the courier station, assumed as node 0
        while len(truck_route) - 1 < truck['capacity'] and unvisited_nodes:
            last_node = truck_route[-1]

            # Sort unvisited nodes based on distance from last node (greedy choice)
            next_node = min(unvisited_nodes, key=lambda x: matrix[last_node][x])
            if matrix[last_node][next_node] == float('inf'):
                break  # No accessible nodes left

            truck_route.append(next_node)
            truck['distance'] += matrix[last_node][next_node]
            unvisited_nodes.remove(next_node)

        truck['route'] = truck_route

    return trucks

def write_output(file_path, trucks):
    total_distance = sum(truck['distance'] for truck in trucks)
    with open(file_path, 'w') as file:
        for truck in trucks:
            # Convert node indices back to letters
            delivery_route = [chr(97 + node) for node in truck['route'][1:]]  # Skip start node
            file.write(f"{truck['id']}#{','.join(delivery_route)}\n")
        file.write(f"{total_distance}\n")

if __name__ == "__main__":
    # Change 'input.txt' and 'output.txt' with your actual file paths or index number
    matrix, trucks = parse_input('input.txt')
    trucks = hill_climbing_algorithm(matrix, trucks)
    write_output('220716x.txt', trucks)

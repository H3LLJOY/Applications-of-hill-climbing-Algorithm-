import numpy as np

def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the matrix
    matrix_lines = [line.strip() for line in lines if ',' in line]
    matrix = []
    for line in matrix_lines:
        row = []
        for val in line.split(','):
            if val != 'N':
                row.append(int(val))
            else:
                row.append(float('inf'))
        matrix.append(row)

    # Extract truck information
    truck_lines = [line.strip() for line in lines[len(matrix_lines):] if line.strip()]
    trucks = [
        {'id': truck_id, 'capacity': int(capacity), 'route': [], 'distance': 0}
        for truck_id, capacity in (line.split('#') for line in truck_lines)
    ]

    return np.array(matrix), trucks

def hill_climbing_algorithm(matrix, trucks):
    n = len(matrix)
    for truck in trucks:
        current_route = [0]  # Start from the courier service station (node 'a')
        current_distance = 0

        while len(current_route) - 1 < truck['capacity']:
            last_node = current_route[-1]
            next_node = None
            min_distance = float('inf')

            for i in range(n):
                if i not in current_route and matrix[last_node][i] < min_distance:
                    next_node = i
                    min_distance = matrix[last_node][i]

            if next_node is None:
                break

            current_route.append(next_node)
            current_distance += min_distance

        truck['route'] = current_route[1:]  # Exclude the starting node 'a'
        truck['distance'] = current_distance

    return trucks

def write_output(file_path, trucks):
    with open(file_path, 'w') as file:
        total_distance = 0
        for truck in trucks:
            route_str = ','.join(chr(97 + node) for node in truck['route'])  # Convert node index to letter
            file.write(f"{truck['id']}#{route_str}\n")
            total_distance += truck['distance']
        file.write(f"{total_distance}\n")

if __name__ == "__main__":
    matrix, trucks = parse_input("input.txt")
    trucks = hill_climbing_algorithm(matrix, trucks)
    write_output("220716x.txt", trucks)
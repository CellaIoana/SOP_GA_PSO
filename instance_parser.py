def parse_sop_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    dimension = 0
    matrix = []
    precedence_constraints = []
    reading_matrix = False
    reading_precedence = False

    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split(":")[1].strip())
        elif line.startswith("EDGE_WEIGHT_SECTION"):
            reading_matrix = True
            continue
        elif line.startswith("PRECEDENCE_SECTION"):
            reading_matrix = False
            reading_precedence = True
            continue
        elif line.startswith("EOF"):
            break

        if reading_matrix:
            row = list(map(int, line.split()))
            if row:
                matrix.append(row)

        elif reading_precedence:
            parts = line.split()
            if len(parts) == 2:
                i, j = map(int, parts)
                precedence_constraints.append((i - 1, j - 1))  

    nodes = list(range(dimension))
    return nodes, matrix, precedence_constraints

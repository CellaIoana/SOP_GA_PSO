import random

def respects_precedence(chromosome, precedence_constraints):
    for before, after in precedence_constraints:
        if chromosome.index(before) > chromosome.index(after):
            return False
    return True

def calculate_fitness_matrix(chromosome, matrix, precedence_constraints):
    if not respects_precedence(chromosome, precedence_constraints):
        return float('inf')

    total_cost = 0

    for i in range(len(chromosome) - 1):
        u, v = chromosome[i], chromosome[i + 1]

        
        if u < 0 or v < 0 or u >= len(matrix) or v >= len(matrix[u]):
            return float('inf')

        cost = matrix[u][v]
        if cost >= 999999:
            return float('inf')

        total_cost += cost

    return total_cost



def generate_initial_population_matrix(nodes, population_size, precedence_constraints):
    population = []
    while len(population) < population_size:
        candidate = nodes[:]
        random.shuffle(candidate)
        if respects_precedence(candidate, precedence_constraints):
            population.append(candidate)
    return population

def tournament_selection_matrix(population, matrix, precedence_constraints, k=3):
    tournament = random.sample(population, k)
    tournament.sort(key=lambda ind: calculate_fitness_matrix(ind, matrix, precedence_constraints))
    return tournament[0]

def order_crossover_matrix(p1, p2, precedence_constraints):
    size = len(p1)
    while True:
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[start:end+1] = p1[start:end+1]
        pointer = 0
        for i in range(size):
            if child[i] is None:
                while p2[pointer] in child:
                    pointer += 1
                child[i] = p2[pointer]
        if respects_precedence(child, precedence_constraints):
            return child

def mutate_matrix(individual, precedence_constraints, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        mutated = individual[:]
        mutated[i], mutated[j] = mutated[j], mutated[i]
        if respects_precedence(mutated, precedence_constraints):
            return mutated
    return individual

def run_genetic_algorithm_matrix(nodes, matrix, precedence_constraints,
                                  population_size=50, generations=100,
                                  crossover_rate=0.9, mutation_rate=0.1, elitism=True):
    population = generate_initial_population_matrix(nodes, population_size, precedence_constraints)
    best_fitness_over_time = []

    for gen in range(generations):
        new_population = []

        if elitism:
            best = min(population, key=lambda ind: calculate_fitness_matrix(ind, matrix, precedence_constraints))
            new_population.append(best)

        while len(new_population) < population_size:
            p1 = tournament_selection_matrix(population, matrix, precedence_constraints)
            p2 = tournament_selection_matrix(population, matrix, precedence_constraints)

            
            if random.random() < crossover_rate:
                child = order_crossover_matrix(p1, p2, precedence_constraints)
            else:
                child = p1[:]

            child = mutate_matrix(child, precedence_constraints, mutation_rate)
            new_population.append(child)

        population = new_population
        best_fitness = min(calculate_fitness_matrix(ind, matrix, precedence_constraints) for ind in population)
        best_fitness_over_time.append(best_fitness)

    best_individual = min(population, key=lambda ind: calculate_fitness_matrix(ind, matrix, precedence_constraints))
    return best_individual, best_fitness_over_time

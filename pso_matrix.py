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



def generate_swap_sequence(a, b):
    a = a[:]
    swaps = []
    for i in range(len(a)):
        if a[i] != b[i]:
            j = a.index(b[i])
            a[i], a[j] = a[j], a[i]
            swaps.append((i, j))
    return swaps

class Particle:
    def __init__(self, nodes, matrix, precedence_constraints):
        while True:
            random.shuffle(nodes)
            if respects_precedence(nodes, precedence_constraints):
                break
        self.position = nodes[:] 
        self.velocity = [] 
        self.best_position = self.position[:] 
        self.matrix = matrix
        self.precedence_constraints = precedence_constraints
        self.pbest_fitness = calculate_fitness_matrix(self.position, matrix, precedence_constraints)
        

    def update_personal_best(self):
        current_fitness = calculate_fitness_matrix(self.position, self.matrix, self.precedence_constraints)
        if current_fitness < self.pbest_fitness:
            self.best_position = self.position[:]
            self.pbest_fitness = current_fitness

def run_pso_matrix(nodes, matrix, precedence_constraints,
                   num_particles=50, generations=100, w=0.4, c1=1.5, c2=1.5):

    swarm = [Particle(nodes[:], matrix, precedence_constraints) for _ in range(num_particles)]
    global_best = min(swarm, key=lambda p: p.pbest_fitness)
    global_best_position = global_best.best_position[:]
    global_best_fitness = global_best.pbest_fitness
    history = [global_best_fitness]

    for _ in range(generations):
        for p in swarm:
            p.update_personal_best()
            fitness = calculate_fitness_matrix(p.position, matrix, precedence_constraints)
            if fitness < global_best_fitness:
                global_best_position = p.position[:]
                global_best_fitness = fitness
                

        for p in swarm:
            
            inertia_sample_size = min(len(p.velocity), int(w * len(p.velocity))) if p.velocity else 0
            inertia = random.sample(p.velocity, inertia_sample_size) if inertia_sample_size > 0 else []

            cognitive = generate_swap_sequence(p.position, p.best_position)
            cognitive_sample_size = min(len(cognitive), int(c1 * random.random() * len(cognitive))) if cognitive else 0
            cognitive = random.sample(cognitive, cognitive_sample_size) if cognitive_sample_size > 0 else []

            social = generate_swap_sequence(p.position, global_best_position)
            social_sample_size = min(len(social), int(c2 * random.random() * len(social))) if social else 0
            social = random.sample(social, social_sample_size) if social_sample_size > 0 else []

            new_velocity = inertia + cognitive + social
            pos = p.position[:]
            for i, j in new_velocity:
                pos[i], pos[j] = pos[j], pos[i]

            if respects_precedence(pos, precedence_constraints):
                p.position = pos
                p.velocity = new_velocity

        history.append(global_best_fitness)

    return global_best_position, history


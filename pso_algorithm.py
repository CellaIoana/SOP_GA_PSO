import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# FUNCTII DE EVALUARE:

# Functia de verificare a constrangerilor o refolosim
def respects_precedence(chromosome, precedence_constraints):
    for before, after in precedence_constraints:
        if chromosome.index(before) > chromosome.index(after):
            return False
    return True

# Functia de fitness (cost total)
def calculate_fitness(chromosome, graph, precedence_constraints):
    if not respects_precedence(chromosome, precedence_constraints):
        return float('inf')

    total_cost = 0
    for i in range(len(chromosome) - 1):
        u = chromosome[i]
        v = chromosome[i + 1]
        if graph.has_edge(u, v):
            total_cost += graph[u][v]['weight']
        else:
            return float('inf')
    return total_cost


def create_graph():
    G = nx.DiGraph() 

    nodes = list(range(1, 6))
    G.add_nodes_from(nodes)

    edges = {
        (1, 2): 10,
        (1, 3): 3,
        (2, 3): 1,
        (2, 4): 2,
        (3, 4): 8,
        (3, 5): 2,
        (4, 5): 4
    }
    for (i, j), cost in edges.items():
        G.add_edge(i, j, weight=cost)

    
    precedence = [(1, 3), (2, 4)] 

    return G, nodes, precedence


class Particle:
    def __init__(self, position, graph, precedence_constraints):
        self.position = position  
        self.graph = graph
        self.precedence_constraints = precedence_constraints

        self.fitness = calculate_fitness(self.position, graph, precedence_constraints)
        self.pbest = position[:]  
        self.pbest_fitness = self.fitness
        
        self.velocity = []  

    
    def update_personal_best(self, current_fitness):
        if current_fitness < self.pbest_fitness:
            self.pbest = self.position[:]
            self.pbest_fitness = current_fitness


    
    def apply_velocity(self):
        for i, j in self.velocity:
            self.position[i], self.position[j] = self.position[j], self.position[i]

        
        if not respects_precedence(self.position, self.precedence_constraints):
            self.position = self.pbest[:]

        self.fitness = calculate_fitness(self.position, self.graph, self.precedence_constraints)


# FUNCTII UTILITARE PENTRU PSO


def generate_swap_sequence(current, target):
    
    current = current[:]  
    swaps = [] 

    for i in range(len(current)):
        if current[i] != target[i]: 
            swap_index = current.index(target[i])
            
            swaps.append((i, swap_index))
            
            current[i], current[swap_index] = current[swap_index], current[i]

    return swaps


def update_velocity(particle, gbest, w=0.5, c1=1, c2=2):
   
    velocity = []

    inertia_component = random.sample(particle.velocity, int(w * len(particle.velocity))) if particle.velocity else []
  
    pbest_component = generate_swap_sequence(particle.position, particle.pbest)
    pbest_component = random.sample(pbest_component, int(c1 * random.random() * len(pbest_component))) if pbest_component else []

    gbest_component = generate_swap_sequence(particle.position, gbest)
    gbest_component = random.sample(gbest_component, int(c2 * random.random() * len(gbest_component))) if gbest_component else []

    velocity.extend(inertia_component)
    velocity.extend(pbest_component)
    velocity.extend(gbest_component)

    particle.velocity = velocity


def run_pso(graph, nodes, precedence_constraints,
            num_particles=30, generations=100,
            w=0.5, c1=1.5, c2=1.5):
   
    swarm = [Particle(nodes, graph, precedence_constraints) for _ in range(num_particles)]

    global_best = min(swarm, key=lambda p: p.pbest_fitness)
    global_best_position = global_best.pbest[:]
    global_best_fitness = global_best.pbest_fitness

    history = [global_best_fitness]  

    for gen in range(generations):
        for particle in swarm:
            
            fitness = calculate_fitness(particle.position, graph, precedence_constraints)
            particle.update_personal_best(fitness)

            
            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = particle.position[:]

        
        for particle in swarm:
            
            inertia_component = random.sample(particle.velocity, int(w * len(particle.velocity))) if particle.velocity else []

            cognitive = generate_swap_sequence(particle.position, particle.pbest)
            cognitive_component = random.sample(cognitive, int(c1 * random.random() * len(cognitive))) if cognitive else []

            social = generate_swap_sequence(particle.position, global_best_position)
            social_component = random.sample(social, int(c2 * random.random() * len(social))) if social else []

            new_velocity = inertia_component + cognitive_component + social_component
            particle.velocity = new_velocity

            particle.apply_velocity()

        history.append(global_best_fitness)
        print(f"Generația {gen + 1}: Best fitness = {global_best_fitness}")

    return global_best_position, history


# Testari rapide

if __name__ == "__main__":
    # Generam graful si datele de intrare
    G, nodes, precedence = create_graph()

    # Test 1: Vitezele
    a = [1, 2, 3, 4, 5]
    b = [2, 1, 3, 5, 4]
    swaps = generate_swap_sequence(a, b)
    print("Swap-uri necesare:", swaps)

    # Test PSO complet
    best_solution, fitness_evolution = run_pso(G, nodes, precedence)

    print("Cea mai buna solutie gasita:", best_solution)
    print("Costul ei:", calculate_fitness(best_solution, G, precedence))

    # Grafic
    import matplotlib.pyplot as plt
    plt.plot(fitness_evolution)
    plt.xlabel("Generatie")
    plt.ylabel("Cel mai bun fitness")
    plt.title("Evolutia PSO")
    plt.grid()
    plt.show()



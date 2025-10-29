import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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


def respects_precedence(chromosome, precedence_constraints):
    """
    Verifica daca un cromozom respecta toate constrangerile de precedenta
    :param chromosome: o lista de noduri (ex: [1, 2, 3, 4, 5])
    :param precedence_constraints: lista de tupluri (ex: [(1, 3), (2, 4)])
    :return: True daca e valid, False daca nu
    """
    for before, after in precedence_constraints:
        if chromosome.index(before) > chromosome.index(after):
            return False
    return True

def calculate_fitness(chromosome, graph, precedence_constraints):
    """
    Calculeaza fitness-ul unui cromozom:
    - daca respecta constrangerile -> suma costurilor muchiilor
    - daca nu -> returneaza inf (penalizare)
    """
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


def generate_initial_population(nodes, population_size, precedence_constraints):
    """
    Genereaza o populatie initială de cromozomi valizi.
    :param nodes: lista nodurilor (ex: [1, 2, 3, 4, 5])
    :param population_size: cati indivizi sa generam
    :param precedence_constraints: reguli de tipul (i inainte de j)
    :return: lista cu cromozomi validati
    """
    population = [] 
    while len(population) < population_size: 
        individual = nodes[:] 
        random.shuffle(individual)
        if respects_precedence(individual, precedence_constraints):
            population.append(individual) 
    return population                     
   


def tournament_selection(population, graph, precedence_constraints, tournament_size=3):
    
    tournament = random.sample(population, tournament_size)
    

    tournament_fitness = [
        (individual, calculate_fitness(individual, graph, precedence_constraints))
        for individual in tournament
    ]
    
    tournament_fitness.sort(key=lambda x: x[1])  

    return tournament_fitness[0][0]  


def order_crossover(parent1, parent2, precedence_constraints):
    
    size = len(parent1)

    
    while True:

       
        start, end = sorted(random.sample(range(size), 2))

        
        child = [None] * size

       
        child[start:end+1] = parent1[start:end+1]

        
        pointer = 0 
        for i in range(size): 
            if child[i] is None: 
                while parent2[pointer] in child: 
                    pointer += 1
                child[i] = parent2[pointer] 
        
        if respects_precedence(child, precedence_constraints):
            return child


def mutate(individual, precedence_constraints, mutation_rate=0.1):
    
    if random.random() < mutation_rate:
        size = len(individual)
        i, j = random.sample(range(size), 2) 
        mutated = individual[:] 
        mutated[i], mutated[j] = mutated[j], mutated[i]

        if respects_precedence(mutated, precedence_constraints):
            return mutated  
    return individual  


def run_genetic_algorithm(graph, nodes, precedence_constraints,
                          population_size=50, generations=100,
                          crossover_rate=0.9, mutation_rate=0.1, elitism=True):
   
    population = generate_initial_population(nodes, population_size, precedence_constraints)
    best_fitness_over_time = [] 

    for gen in range(generations):
        new_population = []

        
        if elitism:
            population_fitness = [
                (ind, calculate_fitness(ind, graph, precedence_constraints)) for ind in population
            ]
            population_fitness.sort(key=lambda x: x[1])
            best_individual = population_fitness[0][0]
            new_population.append(best_individual)

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, graph, precedence_constraints)
            parent2 = tournament_selection(population, graph, precedence_constraints)

            
            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2, precedence_constraints)
            else:
                child = parent1[:]

            
            child = mutate(child, precedence_constraints, mutation_rate)

            new_population.append(child)

        population = new_population

        
        best_fitness = min(calculate_fitness(ind, graph, precedence_constraints) for ind in population)
        best_fitness_over_time.append(best_fitness)

        print(f"Generația {gen + 1}: Best fitness = {best_fitness}")

    
    best_individual = min(population, key=lambda ind: calculate_fitness(ind, graph, precedence_constraints))
    return best_individual, best_fitness_over_time


# testari rapide 
if __name__ == "__main__":
    G, nodes, precedence = create_graph()

    # Test 1: Verificare constrangeri
    cromozom_valid = [1, 2, 3, 4, 5]
    cromozom_invalid = [3, 1, 2, 4, 5]

    print("Valid:", respects_precedence(cromozom_valid, precedence))
    print("Invalid:", respects_precedence(cromozom_invalid, precedence))

    # Test 2: Fitness
    print("Fitness valid:", calculate_fitness(cromozom_valid, G, precedence))
    print("Fitness invalid:", calculate_fitness(cromozom_invalid, G, precedence))

    # Test 3: Populatie
    pop = generate_initial_population(nodes, 5, precedence)
    for i, individual in enumerate(pop):
        print(f"Individ {i+1}: {individual} -> Fitness: {calculate_fitness(individual, G, precedence)}")

    # Test 4: Seceltia parintiilor
    pop = generate_initial_population(nodes, 10, precedence)

    selected = tournament_selection(pop, G, precedence)
    print("Individ selectat pentru reproducere:", selected)

    # Test 5: Swap Mutation
    pop = generate_initial_population(nodes, 5, precedence)

    original = pop[0]
    mutated = mutate(original, precedence_constraints=precedence)

    print("Original:", original)
    print("Mutated :", mutated)

    # Test 6: Algoritmul Principal care repeta toti pasii
    best, history = run_genetic_algorithm(G, nodes, precedence,
                                          population_size=30,
                                          generations=50)

    print("Cel mai bun individ gasit:", best)
    print("Costul lui:", calculate_fitness(best, G, precedence))

        # Test 7: Grafic evolutie fitness
    import matplotlib.pyplot as plt

    plt.plot(history)
    plt.xlabel("Generatie")
    plt.ylabel("Cel mai bun fitness")
    plt.title("Evolutia fitness-ului")
    plt.grid()
    plt.show()







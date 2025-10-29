from genetic_algorithm import run_genetic_algorithm
from pso_algorithm import run_pso, create_graph, calculate_fitness
from instance_parser import parse_sop_file
from genetic_matrix import run_genetic_algorithm_matrix, calculate_fitness_matrix
from pso_matrix import run_pso_matrix
import matplotlib.pyplot as plt
import os

def test_algorithms_on_same_instance():
    G, nodes, precedence = create_graph()  

    
    best_ga, fitness_ga = run_genetic_algorithm(G, nodes, precedence,
                                                 population_size=30, generations=50)

    
    best_pso, fitness_pso = run_pso(G, nodes, precedence,
                                     num_particles=30, generations=50)

    print("GA - Cel mai bun individ:", best_ga)
    print("Cost GA:", calculate_fitness(best_ga, G, precedence))
    print("PSO - Cea mai buna solutie:", best_pso)
    print("Cost PSO:", calculate_fitness(best_pso, G, precedence))

    
    plt.plot(fitness_ga, label="GA")
    plt.plot(fitness_pso, label="PSO")
    plt.xlabel("Generatie")
    plt.ylabel("Cel mai bun fitness")
    plt.title("Compararea evolutiei GA vs PSO")
    plt.legend()
    plt.grid()
    plt.show()


def test_algorithms_on_real_instances():
    instances = ["ESC07.sop", "ESC25.sop", "ESC78.sop"]
    base_path = "sop_instances/"

    for instance in instances:
        print("\n====================")
        print(f" Testare pe instanta: {instance}")
        print("====================")

        filepath = os.path.join(base_path, instance)
        nodes, matrix, precedence = parse_sop_file(filepath)

        
        best_ga, fitness_ga = run_genetic_algorithm_matrix(
            nodes, matrix, precedence,
            population_size=50,
            generations=100
        )
        cost_ga = calculate_fitness_matrix(best_ga, matrix, precedence)
        print(f"GA -> Cel mai bun cost: {cost_ga}")

        
        best_pso, fitness_pso = run_pso_matrix(
            nodes, matrix, precedence,
            num_particles=50,
            generations=100
        )
        cost_pso = calculate_fitness_matrix(best_pso, matrix, precedence)
        print(f"PSO -> Cel mai bun cost: {cost_pso}")

        
        plt.figure()
        plt.plot(fitness_ga, label="Genetic Algorithm (GA)")
        plt.plot(fitness_pso, label="Particle Swarm Optimization (PSO)")
        plt.xlabel("Generatie")
        plt.ylabel("Fitness")
        plt.title(f"Comparare GA vs PSO - {instance}")
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
   # test_algorithms_on_same_instance()
    test_algorithms_on_real_instances()
    




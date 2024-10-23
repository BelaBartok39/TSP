import random
from typing import List, Tuple
from city import City, fitness_function

def genetic_algorithm(cities: List[City], population_size: int = 100, generations: int = 1000,
                      elite_size: int = 20, mutation_rate: float = 0.01,
                      animation_steps: int = 100) -> Tuple[List[City], float, List[float], List[List[City]]]:
    
    def create_route() -> List[City]:
        return random.sample(cities, len(cities))
    
    def create_population(pop_size: int) -> List[List[City]]:
        return [create_route() for _ in range(pop_size)]
    
    def rank_routes(population: List[List[City]]) -> List[Tuple[int, float]]:
        results = [(i, fitness_function(route)) for i, route in enumerate(population)]
        return sorted(results, key=lambda x: x[1])
    
    def selection(ranked_population: List[Tuple[int, float]], elite_size: int) -> List[int]:
        return [i for i, _ in ranked_population[:elite_size]]
    
    def breed(parent1: List[City], parent2: List[City]) -> List[City]:
        child = []
        gene_a, gene_b = sorted(random.sample(range(len(parent1)), 2))
        child.extend(parent1[gene_a:gene_b])
        child += [city for city in parent2 if city not in child]
        return child
    
    def breed_population(mating_pool: List[List[City]], elite_size: int) -> List[List[City]]:
        children = mating_pool[:elite_size]
        pool = random.sample(mating_pool, len(mating_pool))
        for i in range(len(mating_pool) - elite_size):
            children.append(breed(pool[i], pool[len(mating_pool)-1-i]))
        return children
    
    def mutate(individual: List[City], mutation_rate: float) -> List[City]:
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(individual)-1)
                individual[i], individual[j] = individual[j], individual[i]
        return individual
    
    def mutate_population(population: List[List[City]], mutation_rate: float) -> List[List[City]]:
        return [mutate(individual.copy(), mutation_rate) for individual in population]
    
    population = create_population(population_size)
    best_fitness = float('inf')
    best_route = None
    
    convergence = []
    routes_history = []
    
    save_interval = max(1, generations // animation_steps)
    
    for gen in range(generations):
        ranked_pop = rank_routes(population)
        current_best_fitness = ranked_pop[0][1]
        current_best_route = population[ranked_pop[0][0]]
        
        convergence.append(current_best_fitness)
        
        if gen % save_interval == 0:
            routes_history.append(current_best_route.copy())
        
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_route = current_best_route.copy()
            
        selection_results = selection(ranked_pop, elite_size)
        mating_pool = [population[i] for i in selection_results]
        children = breed_population(mating_pool, elite_size)
        population = mutate_population(children, mutation_rate)
    
    if routes_history[-1] != best_route:
        routes_history.append(best_route.copy())
    
    return best_route, best_fitness, convergence, routes_history

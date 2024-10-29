from typing import List, Tuple
import random
from city import City, fitness_function

def genetic_algorithm(
    cities: List[City],
    population_size: int = 500,  
    generations: int = 1000,     
    elite_size: int = 20,        
    mutation_rate: float = 0.015, 
    animation_steps: int = 100,
    convergence_threshold: int = 50  # for early stopping
) -> Tuple[List[City], float, List[float], List[List[City]]]:
    """
    Args:
        cities: List of City objects representing locations to visit
        population_size: Size of the population in each generation
        generations: Maximum number of generations to evolve
        elite_size: Number of best solutions to preserve in each generation
        mutation_rate: Probability of mutation for each gene (0-1)
        animation_steps: Number of intermediate solutions to save for animation
        convergence_threshold: Number of generations without improvement before stopping
    
    Returns:
        Tuple containing:
        - Best route found (List[City])
        - Best fitness score (float)
        - Convergence history (List[float])
        - Route history for animation (List[List[City]])
    """
    def create_route() -> List[City]:
        """Creates a random route visiting all cities."""
        return random.sample(cities, len(cities))
    
    def create_population(pop_size: int) -> List[List[City]]:
        """Creates an initial population of random routes."""
        return [create_route() for _ in range(pop_size)]
    
    def rank_routes(population: List[List[City]]) -> List[Tuple[int, float]]:
        """Ranks all routes in the population by their fitness."""
        results = [(i, fitness_function(route)) for i, route in enumerate(population)]
        return sorted(results, key=lambda x: x[1])
    
    def tournament_select(ranked_population: List[Tuple[int, float]], tournament_size: int = 5) -> int:
        """Selects a parent using tournament selection."""
        tournament = random.sample(ranked_population, tournament_size)
        return min(tournament, key=lambda x: x[1])[0]
    
    def selection(ranked_population: List[Tuple[int, float]], elite_size: int) -> List[int]:
        """Selects parents using elitism and tournament selection."""
        selected_indices = [i for i, _ in ranked_population[:elite_size]]  # Elites
        
        # tournament selection for the rest
        while len(selected_indices) < population_size:
            selected_indices.append(tournament_select(ranked_population))
        return selected_indices
    
    def ordered_crossover(parent1: List[City], parent2: List[City]) -> List[City]:
        """Performs ordered crossover between two parents."""
        size = len(parent1)
        child = [None] * size
        
        # select random subset of parent1
        start, end = sorted(random.sample(range(size), 2))
        child[start:end] = parent1[start:end]
        
        # fill remaining positions with cities from parent2
        parent2_iter = (city for city in parent2 if city not in child[start:end])
        for i in list(range(0, start)) + list(range(end, size)):
            child[i] = next(parent2_iter)
            
        return child
    
    def breed_population(mating_pool: List[List[City]], elite_size: int) -> List[List[City]]:
        """Creates a new population through breeding."""
        children = mating_pool[:elite_size]  # Preserve elites
        
        # breed remaining individuals
        for i in range(elite_size, len(mating_pool), 2):
            parent1 = mating_pool[i]
            parent2 = mating_pool[min(i + 1, len(mating_pool) - 1)]
            children.append(ordered_crossover(parent1, parent2))
            if len(children) < len(mating_pool):
                children.append(ordered_crossover(parent2, parent1))
                
        return children
    
    def swap_mutation(individual: List[City], mutation_rate: float) -> List[City]:
        """Applies swap mutation to a route."""
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[i], individual[j] = individual[j], individual[i]
        return individual
    
    def mutate_population(population: List[List[City]], mutation_rate: float,
                         elite_size: int) -> List[List[City]]:
        """Applies mutation to the population, preserving elites."""
        return (
            population[:elite_size] +  # Keep elites unchanged
            [swap_mutation(individual.copy(), mutation_rate) 
             for individual in population[elite_size:]]
        )

    # initialize population and tracking variables
    population = create_population(population_size)
    best_fitness = float('inf')
    best_route = None
    generations_without_improvement = 0
    
    convergence = []
    routes_history = []
    save_interval = max(1, generations // animation_steps)
    
    # main evolution loop
    for gen in range(generations):
        # rank current population
        ranked_pop = rank_routes(population)
        current_best_fitness = ranked_pop[0][1]
        current_best_route = population[ranked_pop[0][0]]
        
        # update tracking
        convergence.append(current_best_fitness)
        if gen % save_interval == 0:
            routes_history.append(current_best_route.copy())
        
        # update best solution
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_route = current_best_route.copy()
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        
        # check for early stopping
        if generations_without_improvement >= convergence_threshold:
            break
            
        # create next generation
        selection_results = selection(ranked_pop, elite_size)
        mating_pool = [population[i] for i in selection_results]
        children = breed_population(mating_pool, elite_size)
        population = mutate_population(children, mutation_rate, elite_size)
    
    # ensure best route is in history
    if not routes_history or routes_history[-1] != best_route:
        routes_history.append(best_route.copy())
    
    return best_route, best_fitness, convergence, routes_history
import random
import numpy as np
from typing import List, Tuple
from city import City, fitness_function

def simulated_annealing(cities: List[City], initial_temp: float = 1000.0, 
                        cooling_rate: float = 0.995, min_temp: float = 1e-8,
                        animation_steps: int = 100) -> Tuple[List[City], float, List[float], List[List[City]]]:
    current_route = cities.copy()
    current_fitness = fitness_function(current_route)
    best_route = current_route.copy()
    best_fitness = current_fitness
    temperature = initial_temp
    
    convergence = [current_fitness]
    routes_history = [current_route.copy()]
    step_count = 0
    total_steps = 0
    
    while temperature > min_temp:
        i, j = random.sample(range(len(cities)), 2)
        neighbor_route = current_route.copy()
        neighbor_route[i], neighbor_route[j] = neighbor_route[j], neighbor_route[i]
        neighbor_fitness = fitness_function(neighbor_route)
        
        delta = neighbor_fitness - current_fitness
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            current_route = neighbor_route
            current_fitness = neighbor_fitness
            
            if current_fitness < best_fitness:
                best_route = current_route.copy()
                best_fitness = current_fitness
                convergence.append(best_fitness)
                step_count += 1
                if step_count % (total_steps // animation_steps + 1) == 0:
                    routes_history.append(current_route.copy())
        
        temperature *= cooling_rate
        total_steps += 1
    
    if routes_history[-1] != best_route:
        routes_history.append(best_route.copy())
    
    return best_route, best_fitness, convergence, routes_history

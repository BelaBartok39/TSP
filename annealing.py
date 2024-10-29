import random
import numpy as np
from typing import List, Tuple, Optional
from city import City, fitness_function

def simulated_annealing(
    cities: List[City],
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.995,
    min_temp: float = 1e-8,
    animation_steps: int = 100,
    max_iterations: int = 100000,  # Added parameter to prevent infinite loops
    no_improve_threshold: int = 1000  # Added parameter for early stopping
) -> Tuple[List[City], float, List[float], List[List[City]]]:
    """
    Implements simulated annealing algorithm for solving the Traveling Salesman Problem.
    
    Args:
        cities: List of City objects representing locations to visit
        initial_temp: Starting temperature for annealing process
        cooling_rate: Rate at which temperature decreases (0-1)
        min_temp: Minimum temperature at which to stop
        animation_steps: Number of intermediate solutions to save for animation
        max_iterations: Maximum number of iterations to prevent infinite loops
        no_improve_threshold: Number of iterations without improvement before early stopping
    
    Returns:
        Tuple containing:
        - Best route found (List[City])
        - Best fitness score (float)
        - Convergence history (List[float])
        - Route history for animation (List[List[City]])
    """
    def generate_neighbor(route: List[City]) -> Tuple[List[City], int, int]:
        """Generates a neighbor solution using either swap or 2-opt move."""
        if random.random() < 0.5:  # 50% chance for each move type
            # Swap move
            i, j = random.sample(range(len(route)), 2)
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            return neighbor, i, j
        else:
            # 2-opt move
            i, j = sorted(random.sample(range(len(route)), 2))
            neighbor = route[:i] + route[i:j+1][::-1] + route[j+1:]
            return neighbor, i, j

    def accept_neighbor(delta: float, temp: float) -> bool:
        """Determines whether to accept a neighbor solution."""
        if delta < 0:  # Better solution
            return True
        return random.random() < np.exp(-delta / temp)

    # Initialize variables
    current_route = list(cities)  # Convert to list to ensure mutability
    random.shuffle(current_route)  # Start with a random route
    current_fitness = fitness_function(current_route)
    
    best_route = current_route.copy()
    best_fitness = current_fitness
    
    temperature = initial_temp
    iterations = 0
    iterations_without_improvement = 0
    
    # Initialize tracking lists
    convergence = [current_fitness]
    routes_history = [current_route.copy()]
    
    # Calculate save interval for animation
    save_interval = max(1, max_iterations // animation_steps)
    
    while (temperature > min_temp and 
           iterations < max_iterations and 
           iterations_without_improvement < no_improve_threshold):
        
        # Generate neighbor solution
        neighbor_route, i, j = generate_neighbor(current_route)
        neighbor_fitness = fitness_function(neighbor_route)
        
        # Calculate change in fitness
        delta = neighbor_fitness - current_fitness
        
        # Accept or reject neighbor solution
        if accept_neighbor(delta, temperature):
            current_route = neighbor_route
            current_fitness = neighbor_fitness
            
            # Update best solution if improved
            if current_fitness < best_fitness:
                best_route = current_route.copy()
                best_fitness = current_fitness
                iterations_without_improvement = 0
                
                # Track convergence and route history
                convergence.append(best_fitness)
                if iterations % save_interval == 0:
                    routes_history.append(current_route.copy())
            else:
                iterations_without_improvement += 1
        
        # Cool the temperature
        temperature *= cooling_rate
        iterations += 1
        
        # Occasional reheating if stuck
        if iterations_without_improvement > no_improve_threshold // 2:
            temperature = initial_temp * (0.5 ** (iterations // no_improve_threshold))
    
    # Ensure best route is in history
    if routes_history[-1] != best_route:
        routes_history.append(best_route.copy())
    
    return best_route, best_fitness, convergence, routes_history
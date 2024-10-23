import numpy as np
import matplotlib.pyplot as plt
import random
import time
from typing import List, Tuple
from matplotlib.animation import FuncAnimation
from IPython.display import clear_output

class City:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance(self, other: 'City') -> float:
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def generate_cities(n: int, max_coord: int = 100) -> List[City]:
    return [City(random.uniform(0, max_coord), random.uniform(0, max_coord)) for _ in range(n)]

def calculate_total_distance(route: List[City]) -> float:
    return sum(route[i].distance(route[i-1]) for i in range(len(route)))

class TSPAnimation:
    def __init__(self, cities: List[City], title: str):
        self.cities = cities
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.title = title
        self.routes = []
        self.distances = []
        
        # Plot cities
        self.x = [city.x for city in cities]
        self.y = [city.y for city in cities]
        self.ax.scatter(self.x, self.y, c='red', label='Cities')
        
        # Initialize route line
        self.line, = self.ax.plot([], [], 'b-', label='Current Route')
        
        # Text for displaying current distance
        self.distance_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                        verticalalignment='top')
        
        self.ax.set_title(title)
        self.ax.legend()
        self.ax.grid(True)
        
    def update(self, frame):
        if frame < len(self.routes):
            route = self.routes[frame]
            distance = self.distances[frame]
            
            # Update route line
            route_x = [city.x for city in route + [route[0]]]
            route_y = [city.y for city in route + [route[0]]]
            self.line.set_data(route_x, route_y)
            
            # Update distance text
            self.distance_text.set_text(f'Distance: {distance:.2f}')
        
        return self.line, self.distance_text
    
    def animate(self, interval=50):
        anim = FuncAnimation(self.fig, self.update, frames=len(self.routes),
                           interval=interval, blit=True, repeat=False)
        plt.show()

def simulated_annealing(cities: List[City], initial_temp: float = 1000.0, 
                       cooling_rate: float = 0.995, min_temp: float = 1e-8,
                       animation_steps: int = 100) -> Tuple[List[City], float, List[float], List[List[City]]]:
    current_route = cities.copy()
    current_distance = calculate_total_distance(current_route)
    best_route = current_route.copy()
    best_distance = current_distance
    temperature = initial_temp
    
    convergence = [current_distance]
    routes_history = [current_route.copy()]
    step_count = 0
    total_steps = 0
    
    while temperature > min_temp:
        i, j = random.sample(range(len(cities)), 2)
        neighbor_route = current_route.copy()
        neighbor_route[i], neighbor_route[j] = neighbor_route[j], neighbor_route[i]
        neighbor_distance = calculate_total_distance(neighbor_route)
        
        delta = neighbor_distance - current_distance
        if delta < 0 or random.random() < np.exp(-delta / temperature):
            current_route = neighbor_route
            current_distance = neighbor_distance
            
            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
                convergence.append(best_distance)
                step_count += 1
                if step_count % (total_steps // animation_steps + 1) == 0:
                    routes_history.append(current_route.copy())
        
        temperature *= cooling_rate
        total_steps += 1
    
    # Ensure the final best route is included
    if routes_history[-1] != best_route:
        routes_history.append(best_route.copy())
    
    return best_route, best_distance, convergence, routes_history

def genetic_algorithm(cities: List[City], population_size: int = 100, generations: int = 1000,
                     elite_size: int = 20, mutation_rate: float = 0.01,
                     animation_steps: int = 100) -> Tuple[List[City], float, List[float], List[List[City]]]:
    
    def create_route() -> List[City]:
        return random.sample(cities, len(cities))
    
    def create_population(pop_size: int) -> List[List[City]]:
        return [create_route() for _ in range(pop_size)]
    
    def rank_routes(population: List[List[City]]) -> List[Tuple[int, float]]:
        results = [(i, calculate_total_distance(route)) for i, route in enumerate(population)]
        return sorted(results, key=lambda x: x[1])
    
    def selection(ranked_population: List[Tuple[int, float]], elite_size: int) -> List[int]:
        selection_results = [i for i, _ in ranked_population[:elite_size]]
        return selection_results
    
    def breed(parent1: List[City], parent2: List[City]) -> List[City]:
        child = []
        gene_a, gene_b = sorted(random.sample(range(len(parent1)), 2))
        start_genes = parent1[gene_a:gene_b]
        child.extend(start_genes)
        for city in parent2:
            if city not in child:
                child.append(city)
        return child
    
    def breed_population(mating_pool: List[List[City]], elite_size: int) -> List[List[City]]:
        children = mating_pool[:elite_size]
        pool = random.sample(mating_pool, len(mating_pool))
        for i in range(len(mating_pool) - elite_size):
            child = breed(pool[i], pool[len(mating_pool)-1-i])
            children.append(child)
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
    best_distance = float('inf')
    best_route = None
    
    convergence = []
    routes_history = []
    
    # Calculate how often to save routes for animation
    save_interval = max(1, generations // animation_steps)
    
    for gen in range(generations):
        ranked_pop = rank_routes(population)
        current_best_distance = ranked_pop[0][1]
        current_best_route = population[ranked_pop[0][0]]
        
        convergence.append(current_best_distance)
        
        # Save route for animation at regular intervals
        if gen % save_interval == 0:
            routes_history.append(current_best_route.copy())
        
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_route = current_best_route.copy()
            
        selection_results = selection(ranked_pop, elite_size)
        mating_pool = [population[i] for i in selection_results]
        children = breed_population(mating_pool, elite_size)
        population = mutate_population(children, mutation_rate)
    
    # Ensure the final best route is included
    if best_route not in routes_history:
        routes_history.append(best_route.copy())
    
    return best_route, best_distance, convergence, routes_history

def plot_convergence(distances: List[float], algorithm_name: str):
    plt.figure(figsize=(10, 6))
    plt.plot(distances, 'b-')
    plt.title(f'{algorithm_name} Convergence')
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.grid(True)
    plt.show()

def main():
    while True:
        try:
            n = int(input("\nEnter the number of cities (minimum 4): "))
            if n < 4:
                print("Please enter at least 4 cities.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    cities = generate_cities(n)
    initial_distance = calculate_total_distance(cities)
    last_convergence = None
    last_algorithm = None
    
    while True:
        print("\nSelect option:")
        print("1. Simulated Annealing")
        print("2. Genetic Algorithm")
        print("3. Compare Both")
        print("4. Show Last Convergence Graph")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '5':
            print("Goodbye!")
            break
            
        if choice == '4':
            if last_convergence is None:
                print("No algorithm has been run yet!")
            else:
                plot_convergence(last_convergence, last_algorithm)
            continue
            
        if choice in ['1', '2', '3']:
            print(f"\nOriginal total distance: {initial_distance:.2f}")
            
            if choice in ['1', '3']:
                start_time = time.time()
                sa_route, sa_distance, sa_convergence, sa_history = simulated_annealing(cities)
                sa_time = time.time() - start_time
                
                # Animate Simulated Annealing
                print("\nSimulated Annealing Animation:")
                anim = TSPAnimation(cities, "Simulated Annealing Progress")
                anim.routes = sa_history
                anim.distances = [calculate_total_distance(route) for route in sa_history]
                anim.animate(interval=100)  # Adjust interval (ms) to control animation speed
                
                print(f"\nSimulated Annealing Results:")
                print(f"Best distance: {sa_distance:.2f}")
                print(f"Improvement: {((initial_distance - sa_distance) / initial_distance * 100):.2f}%")
                print(f"Time taken: {sa_time:.2f} seconds")
                last_convergence = sa_convergence
                last_algorithm = "Simulated Annealing"
            
            if choice in ['2', '3']:
                start_time = time.time()
                ga_route, ga_distance, ga_convergence, ga_history = genetic_algorithm(cities)
                ga_time = time.time() - start_time
                
                # Animate Genetic Algorithm
                print("\nGenetic Algorithm Animation:")
                anim = TSPAnimation(cities, "Genetic Algorithm Progress")
                anim.routes = ga_history
                anim.distances = [calculate_total_distance(route) for route in ga_history]
                anim.animate(interval=100)  # Adjust interval (ms) to control animation speed
                
                print(f"\nGenetic Algorithm Results:")
                print(f"Best distance: {ga_distance:.2f}")
                print(f"Improvement: {((initial_distance - ga_distance) / initial_distance * 100):.2f}%")
                print(f"Time taken: {ga_time:.2f} seconds")
                last_convergence = ga_convergence
                last_algorithm = "Genetic Algorithm"
            
            if choice == '3':
                print("\nComparison:")
                print(f"SA vs GA improvement: {((ga_distance - sa_distance) / ga_distance * 100):.2f}%")
                print(f"SA vs GA time difference: {(ga_time - sa_time):.2f} seconds")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
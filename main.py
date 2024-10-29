from city import (generate_cities, fitness_function, load_berlin52, load_kroA100, 
                 get_benchmark_info)
from annealing import simulated_annealing
from genetic import genetic_algorithm
from animation import TSPAnimation, plot_convergence
import time

def main():
    cities = None
    optimal_solution = None
    
    while True:
        print("\nSelect dataset:")
        print("1. Generate random cities")
        print("2. Berlin52 benchmark")
        print("3. KroA100 benchmark")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '4':
            print("Goodbye!")
            break
            
        if choice == '1':
            while True:
                try:
                    n = int(input("\nEnter the number of cities (minimum 4): "))
                    if n < 4:
                        print("Please enter at least 4 cities.")
                        continue
                    cities = generate_cities(n)
                    break
                except ValueError:
                    print("Please enter a valid number.")
        
        elif choice == '2':
            cities, optimal_solution = load_berlin52()
            print("\nLoaded Berlin52 dataset:")
            print(get_benchmark_info("berlin52"))
        
        elif choice == '3':
            cities, optimal_solution = load_kroA100()
            print("\nLoaded KroA100 dataset:")
            print(get_benchmark_info("kroa100"))
        
        if cities:
            initial_fitness = fitness_function(cities)
            last_convergence = None
            last_algorithm = None
            
            while True:
                print("\nSelect option:")
                print("1. Simulated Annealing")
                print("2. Genetic Algorithm")
                print("3. Compare Both")
                print("4. Show Last Convergence Graph")
                print("5. Return to Dataset Selection")
                print("6. Exit")
                
                algo_choice = input("Enter your choice (1-6): ")
                
                if algo_choice == '6':
                    print("Goodbye!")
                    return
                    
                if algo_choice == '5':
                    break
                    
                if algo_choice == '4':
                    if last_convergence is None:
                        print("No algorithm has been run yet!")
                    else:
                        plot_convergence(last_convergence, last_algorithm)
                    continue
                    
                if algo_choice in ['1', '2', '3']:
                    print(f"\nInitial fitness (distance): {initial_fitness:.2f}")
                    if optimal_solution:
                        print(f"Optimal solution: {optimal_solution:.2f}")
                    
                    if algo_choice in ['1', '3']:
                        start_time = time.time()
                        sa_route, sa_fitness, sa_convergence, sa_history = simulated_annealing(cities)
                        sa_time = time.time() - start_time
                        
                        print("\nSimulated Annealing Animation:")
                        anim = TSPAnimation(cities, "Simulated Annealing Progress")
                        anim.routes = sa_history
                        anim.distances = [fitness_function(route) for route in sa_history]
                        anim.animate(interval=100)
                        
                        print(f"\nSimulated Annealing Results:")
                        print(f"Best fitness: {sa_fitness:.2f}")
                        print(f"Improvement: {((initial_fitness - sa_fitness) / initial_fitness * 100):.2f}%")
                        if optimal_solution:
                            print(f"Gap to optimal: {((sa_fitness - optimal_solution) / optimal_solution * 100):.2f}%")
                        print(f"Time taken: {sa_time:.2f} seconds")
                        last_convergence = sa_convergence
                        last_algorithm = "Simulated Annealing"
                    
                    if algo_choice in ['2', '3']:
                        start_time = time.time()
                        ga_route, ga_fitness, ga_convergence, ga_history = genetic_algorithm(cities)
                        ga_time = time.time() - start_time
                        
                        print("\nGenetic Algorithm Animation:")
                        anim = TSPAnimation(cities, "Genetic Algorithm Progress")
                        anim.routes = ga_history
                        anim.distances = [fitness_function(route) for route in ga_history]
                        anim.animate(interval=100)
                        
                        print(f"\nGenetic Algorithm Results:")
                        print(f"Best fitness: {ga_fitness:.2f}")
                        print(f"Improvement: {((initial_fitness - ga_fitness) / initial_fitness * 100):.2f}%")
                        if optimal_solution:
                            print(f"Gap to optimal: {((ga_fitness - optimal_solution) / optimal_solution * 100):.2f}%")
                        print(f"Time taken: {ga_time:.2f} seconds")
                        last_convergence = ga_convergence
                        last_algorithm = "Genetic Algorithm"
                    
                    if algo_choice == '3':
                        print("\nComparison:")
                        print(f"SA vs GA improvement: {((ga_fitness - sa_fitness) / ga_fitness * 100):.2f}%")
                        print(f"SA vs GA time difference: {(ga_time - sa_time):.2f} seconds")
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
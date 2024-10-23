from city import generate_cities, fitness_function
from annealing import simulated_annealing
from genetic import genetic_algorithm
from animation import TSPAnimation, plot_convergence
import time

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
    initial_fitness = fitness_function(cities)
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
            print(f"\nInitial fitness (distance): {initial_fitness:.2f}")
            
            if choice in ['1', '3']:
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
                print(f"Time taken: {sa_time:.2f} seconds")
                last_convergence = sa_convergence
                last_algorithm = "Simulated Annealing"
            
            if choice in ['2', '3']:
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
                print(f"Time taken: {ga_time:.2f} seconds")
                last_convergence = ga_convergence
                last_algorithm = "Genetic Algorithm"
            
            if choice == '3':
                print("\nComparison:")
                print(f"SA vs GA improvement: {((ga_fitness - sa_fitness) / ga_fitness * 100):.2f}%")
                print(f"SA vs GA time difference: {(ga_time - sa_time):.2f} seconds")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List
from city import City

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
        
        # Text for displaying current fitness
        self.distance_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                        verticalalignment='top')
        
        self.ax.set_title(title)
        self.ax.legend()
        self.ax.grid(True)
        
    def update(self, frame):
        if frame < len(self.routes):
            route = self.routes[frame]
            fitness = self.distances[frame]
            
            # Update route line
            route_x = [city.x for city in route + [route[0]]]
            route_y = [city.y for city in route + [route[0]]]
            self.line.set_data(route_x, route_y)
            
            # Update fitness text
            self.distance_text.set_text(f'Fitness (Distance): {fitness:.2f}')
        
        return self.line, self.distance_text
    
    def animate(self, interval=50):
        anim = FuncAnimation(self.fig, self.update, frames=len(self.routes),
                           interval=interval, blit=True, repeat=False)
        plt.show()

def plot_convergence(fitness_values: List[float], algorithm_name: str):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_values, 'b-')
    plt.title(f'{algorithm_name} Convergence')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness (Distance)')
    plt.grid(True)
    plt.show()

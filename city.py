import random
import numpy as np
from typing import List

class City:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance(self, other: 'City') -> float:
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def generate_cities(n: int, max_coord: int = 100) -> List[City]:
    return [City(random.uniform(0, max_coord), random.uniform(0, max_coord)) for _ in range(n)]

def fitness_function(route: List[City]) -> float:
    """
    Calculate the total circuit distance (fitness) of a route.
    Lower values indicate better fitness.
    The route automatically returns to the starting city.
    """
    return sum(route[i].distance(route[i-1]) for i in range(len(route)))

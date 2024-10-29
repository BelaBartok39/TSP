# Travelling Salesman Problem (TSP) Solver

This repository contains an implementation of the Travelling Salesman Problem (TSP) using two optimization algorithms:
1. **Simulated Annealing (SA)** with adaptive temperature control
2. **Genetic Algorithm (GA)** with tournament selection

The program includes visual animations of the route optimization process, convergence plots, and benchmark problems to evaluate algorithm performance.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset Options](#dataset-options)
- [Algorithm Details](#algorithm-details)
- [Visualization](#visualization)
- [Understanding the Modules](#understanding-the-modules)

## Features

- Multiple dataset options including random cities and TSPLIB benchmarks
- Real-time visualization of route optimization
- Convergence plotting and algorithm comparison
- Performance metrics including:
  - Solution quality
  - Execution time
  - Gap to optimal solution (for benchmark problems)
  - Improvement percentage
- Adaptive optimization parameters
- Early stopping mechanisms

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `numpy`
  - `matplotlib`

Install the required libraries with:

```bash
pip install numpy matplotlib
```

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/tsp-solver.git
cd tsp-solver
```

## Usage

Run the program using:

```bash
python main.py
```

### Program Flow:

1. **Select dataset:**
   - Generate random cities
   - Berlin52 benchmark
   - KroA100 benchmark
   - Exit

2. **Choose algorithm:**
   - Simulated Annealing
   - Genetic Algorithm
   - Compare Both
   - Show Last Convergence Graph
   - Return to Dataset Selection
   - Exit

3. **View Results:**
   - Watch real-time animation
   - See performance metrics
   - Compare algorithm performance
   - Analyze convergence graphs

## Dataset Options

### Random Cities
- Generate a custom number of cities (minimum 4)
- Random placement in 2D space
- Suitable for algorithm testing and comparison

### Benchmark Problems
1. **Berlin52**
   - 52 locations in Berlin, Germany
   - Known optimal solution
   - Classic TSP benchmark problem

2. **KroA100**
   - 100 cities
   - Known optimal solution
   - More challenging benchmark

## Algorithm Details

### Simulated Annealing
- Adaptive temperature control
- 2-opt and swap neighborhood moves
- Reheating mechanism for escaping local optima
- Early stopping based on improvement threshold
- Parameters:
  - Initial temperature: 1000.0
  - Cooling rate: 0.995
  - Minimum temperature: 1e-8

### Genetic Algorithm
- Tournament selection
- Ordered crossover (OX)
- Swap mutation
- Elitism preservation
- Parameters:
  - Population size: 500
  - Generations: 1000
  - Elite size: 20
  - Mutation rate: 0.015
  - Tournament size: 5

## Visualization

The program provides two types of visualization:

1. **Route Animation**
   - Real-time display of current route
   - Updates as algorithm progresses
   - Shows improvement over time

2. **Convergence Plots**
   - Track solution quality over time
   - Compare algorithm performance
   - Analyze convergence behavior

## Understanding the Modules

- **`main.py`**: Program entry point, user interface, and execution flow
- **`city.py`**: City class, benchmark loading, and distance calculations
- **`genetic.py`**: Genetic Algorithm implementation with tournament selection
- **`annealing.py`**: Simulated Annealing with adaptive temperature control
- **`animation.py`**: Route visualization and convergence plotting

### Example Output:

```bash
Select dataset:
1. Generate random cities
2. Berlin52 benchmark
3. KroA100 benchmark
4. Exit

Enter your choice (1-4): 2

Loaded Berlin52 dataset:
Optimal solution: 7542
Number of cities: 52

Initial fitness (distance): 15824.31
Best fitness found: 7892.15
Improvement: 50.13%
Gap to optimal: 4.64%
Time taken: 5.23 seconds
```

## License

This project is licensed under the MIT License.
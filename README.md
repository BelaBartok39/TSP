# Travelling Salesman Problem (TSP) Solver

This repository contains an implementation of the Travelling Salesman Problem (TSP) using two optimization algorithms:
1. **Simulated Annealing (SA)**
2. **Genetic Algorithm (GA)**

The program also includes a visual animation of the route optimization process and convergence plots to compare the performance of both algorithms.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Program](#running-the-program)
- [Understanding the Modules](#understanding-the-modules)

## Requirements

- Python 3.6 or higher
- The following Python libraries:
  - `numpy`
  - `matplotlib`

You can install the required libraries with the following command:

```bash
pip install numpy matplotlib
```

## Installation

To get started with this project, you need to clone the repository to your local machine.

```bash
git clone https://github.com/your-username/tsp-solver.git cd tsp-solver
```


## Usage

Once the repository is cloned and dependencies are installed, you can run the program using the following command:

```bash
python main.py
```


### How to Use the Program:

1. **Choose the number of cities:** You will be prompted to enter the number of cities (minimum 4).
2. **Select the algorithm:**
   - Simulated Annealing
   - Genetic Algorithm
   - Compare both algorithms
   - Show the last convergence graph
3. **Watch the animation:** The program will visualize the progress of the algorithm through an animation of the TSP solution.
4. **View the results:** The best fitness (total distance) and the time taken for the optimization will be displayed after each algorithm finishes.

## Running the Program

1. After cloning the repository and installing the requirements, execute the main program:
   
```bash
python main.py
```


2. Follow the on-screen instructions to:
- Choose the number of cities.
- Select the optimization algorithm you wish to run (Simulated Annealing, Genetic Algorithm, or both).
- View the progress animation.
- Review the best route and fitness value found by the algorithm.

3. If you select the option to "Compare Both", the program will run both Simulated Annealing and Genetic Algorithm sequentially and display a comparison of the results.

### Example:

```bash
Enter the number of cities (minimum 4): 10

Select option:

    Simulated Annealing
    Genetic Algorithm
    Compare Both
    Show Last Convergence Graph
    Exit Enter your choice (1-5): 1

Initial fitness (distance): 295.32

Simulated Annealing Animation: ... Best fitness: 210.45 Improvement: 28.77% Time taken: 3.47 seconds
```


## Understanding the Modules

The program is structured into several modules to keep the code organized:

- **`main.py`**: Contains the main logic for running the program, handling user input, and invoking the algorithms.
- **`city.py`**: Defines the `City` class and includes functions for generating cities and calculating fitness (total distance of a route).
- **`genetic.py`**: Contains the implementation of the Genetic Algorithm for solving the TSP.
- **`annealing.py`**: Contains the implementation of the Simulated Annealing algorithm for solving the TSP.
- **`animation.py`**: Handles the animation of the optimization process and plots convergence graphs.

### Key Files:
- `main.py`: The entry point of the application.
- `city.py`: Contains the `City` class and city-related utilities.
- `genetic.py`: Genetic Algorithm logic.
- `annealing.py`: Simulated Annealing logic.
- `animation.py`: Code for visualizing the TSP solution progress.

---

## License

This project is licensed under the MIT License.

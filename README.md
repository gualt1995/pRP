# pRP : Solving the minimum Steiner tree problem with metaheuristics
## Introduction
The Steiner tree problem : Given a non-directed connected graph with non negative weighted edges composed of G vertices, 
and a subset T (terminals) of these vertices, find a tree of minimum weight that contains all terminals but may include additional vertices.  
**Example :**  
![alt text](https://raw.githubusercontent.com/gualt1995/pRP/master/report/Graph_Example.PNG)
This graph shows an optimal solution for the Steiner tree problem, with v1, v2, v3 and v5 as terminal nodes
## Installation
Runs on python 3, all the files should be in the same folder, the library networkx is used to display the graphs.
## Usage
Two methods were implemented to solve the steiner tree problem, a genetic algorithm and and a local search algorithm, 
you can run each of these independently with genetic_solver.py and localsearch.py. The instances on which the algorithms were tested can be 
found in the B,C,D and E folders.


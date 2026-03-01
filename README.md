This project presents an interactive implementation of heuristic-based pathfinding algorithms in a grid-based environment using Python and Pygame. The application visualizes and compares the behavior of A* (A-Star) and Greedy Best-First Search (GBFS) algorithms under both static and dynamic conditions.
The system provides real-time visualization, performance metrics, and user interaction for experimental analysis of search strategies in Artificial Intelligence.
Objectives
To implement heuristic search algorithms in a grid environment
To compare informed search strategies (A* and GBFS).
To analyze performance using measurable metrics.
To simulate dynamic environments with runtime obstacle generation.
To provide an interactive visualization tool for academic learning.
Implemented Algorithms
1. A* Search Algorithm
Evaluation function:
f(n)=g(n)+h(n)
Where:
g(n) = Cost from start node to current node
h(n) = Heuristic estimate from current node to goal
2. Greedy Best-First Search (GBFS)
Evaluation function:
f(n)=h(n)
Heuristic Functions
Manhattan Distance
Euclidean Distance
The user can toggle between heuristics to observe differences in search behavior and efficiency.
Key Features
Interactive 30 × 30 grid environment
Real-time visualization of:
Visited nodes
Frontier nodes
Final path
Dynamic obstacle generation during execution
Random maze generation
Resizable window interface
Performance metrics display:
Algorithm type
Heuristic type
Nodes visited
Path cost
Execution time
Dynamic mode status
User Controls
Key	Function
Left Mouse Click	Set Start Node, Goal Node, and Obstacles
SPACE	Execute selected algorithm
A	Toggle between A* and GBFS
H	Toggle heuristic (Manhattan / Euclidean)
G	Generate random maze
D	Toggle dynamic obstacle mode
C	Clear grid
System Architecture
Each grid cell is represented as a Node object.
Nodes maintain references to valid neighboring nodes.
A priority queue (heap-based) is used for efficient node selection.
Performance metrics are recorded using high-resolution timing
Dynamic mode introduces probabilistic obstacle generation during runtime.
Technologies Used
Heapq (Priority Queue implementation)
Math module
Random module
Time module

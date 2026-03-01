import pygame
import heapq
import time
import random
import math


pygame.init()
WIDTH, HEIGHT = 1100, 700 
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("AI-2002: Dynamic Pathfinding Agent")


FONT_UI = pygame.font.SysFont("Verdana", 22, bold=True)
FONT_INFO = pygame.font.SysFont("Arial", 16)


WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
RED = (231, 76, 60)      # Visited Nodes
YELLOW = (241, 196, 15)  # Frontier Nodes
GREEN = (46, 204, 113)   # Final Path
BLUE = (52, 152, 219)    # Start Node
PURPLE = (155, 89, 182)  # Goal Node
SIDEBAR_COLOR = (33, 47, 60)

ROWS = 30 

class Node:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.color = WHITE
        self.neighbors = []

    def draw(self, surface, gap):
        pygame.draw.rect(surface, self.color, (self.c * gap, self.r * gap, gap, gap))
        pygame.draw.rect(surface, GRAY, (self.c * gap, self.r * gap, gap, gap), 1)

    def update_neighbors(self, grid):
        self.neighbors = []
      
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = self.r + dr, self.c + dc
            if 0 <= nr < ROWS and 0 <= nc < ROWS and grid[nr][nc].color != BLACK:
                self.neighbors.append(grid[nr][nc])

def get_h(p1, p2, h_type):
    r1, c1, r2, c2 = p1[0], p1[1], p2[0], p2[1]
    if h_type == "Manhattan":
        return abs(r1 - r2) + abs(c1 - c2)
    return math.sqrt((r1 - r2)**2 + (c1 - c2)**2) 

def solve(draw_fn, grid, start, goal, algo, h_type, metrics, dynamic_active):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    start_time = time.perf_counter()
    nodes_visited = 0

    while open_set:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = heapq.heappop(open_set)[2]
        nodes_visited += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
                current.color = GREEN
            goal.color = PURPLE
            metrics["Visited"] = nodes_visited 
            metrics["Cost"] = len(path)
            metrics["Time"] = f"{(time.perf_counter() - start_time)*1000:.1f}ms" # [cite: 263]
            return True

       
        if dynamic_active and random.random() < 0.1:
            obs_r, obs_c = random.randint(0, ROWS-1), random.randint(0, ROWS-1)
            target = grid[obs_r][obs_c]
            if target not in [start, goal, current]:
                target.color = BLACK

        for neighbor in current.neighbors:
            if neighbor.color == BLACK: continue
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                h_val = get_h((neighbor.r, neighbor.c), (goal.r, goal.c), h_type)
                f_val = (temp_g + h_val) if algo == "A*" else h_val
                count += 1
                heapq.heappush(open_set, (f_val, count, neighbor))
                if neighbor != goal: neighbor.color = YELLOW 

  
        if nodes_visited % 2 == 0: 
            draw_fn()
            pygame.time.delay(10) 
        
        if current != start: current.color = RED

    return False

def main():
    curr_w, curr_h = WIDTH, HEIGHT
    grid_side = curr_h
    gap = grid_side // ROWS
    
    grid = [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)]
    start = goal = None
    dynamic_active = False
    metrics = {"Algo": "A*", "Heuristic": "Manhattan", "Visited": 0, "Cost": 0, "Time": "0ms", "Dynamic": "OFF"}

    def draw_all():
        win.fill(WHITE)
        for r in grid:
            for n in r: n.draw(win, gap)
        
        pygame.draw.rect(win, SIDEBAR_COLOR, (grid_side, 0, curr_w - grid_side, curr_h))
        y = 40
        for k, v in metrics.items():
            text = FONT_UI.render(f"{k}: {v}", True, WHITE)
            win.blit(text, (grid_side + 20, y))
            y += 50
        
        instr = ["SPACE: Start Search", "A: Toggle A*/GBFS", "H: Toggle Heuristic", "G: Random Maze", "D: Toggle Dynamic", "C: Clear"]
        y += 20
        for line in instr:
            text = FONT_INFO.render(line, True, GRAY)
            win.blit(text, (grid_side + 20, y))
            y += 25
        pygame.display.flip()

    run = True
    while run:
        draw_all()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            
            if event.type == pygame.VIDEORESIZE:
                curr_w, curr_h = event.w, event.h
                grid_side = curr_h
                gap = grid_side // ROWS

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: metrics["Algo"] = "GBFS" if metrics["Algo"] == "A*" else "A*"
                if event.key == pygame.K_h: metrics["Heuristic"] = "Euclidean" if metrics["Heuristic"] == "Manhattan" else "Manhattan"
                if event.key == pygame.K_d: 
                    dynamic_active = not dynamic_active
                    metrics["Dynamic"] = "ON" if dynamic_active else "OFF"
                if event.key == pygame.K_g:
                    for r in grid:
                        for n in r:
                            if n not in [start, goal]:
                                n.color = BLACK if random.random() < 0.3 else WHITE
                if event.key == pygame.K_SPACE and start and goal:
                    for r in grid: [n.update_neighbors(grid) for n in r]
                    solve(draw_all, grid, start, goal, metrics["Algo"], metrics["Heuristic"], metrics, dynamic_active)
                if event.key == pygame.K_c:
                    start = goal = None
                    grid = [[Node(r, c) for c in range(ROWS)] for r in range(ROWS)]

            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                if mx < grid_side:
                    r, c = my // gap, mx // gap
                    if 0 <= r < ROWS and 0 <= c < ROWS:
                        node = grid[r][c]
                        if not start: start = node; node.color = BLUE
                        elif not goal and node != start: goal = node; goal.color = PURPLE
                        elif node != start and node != goal: node.color = BLACK # [cite: 231]

    pygame.quit()

if __name__ == "__main__":
    main()

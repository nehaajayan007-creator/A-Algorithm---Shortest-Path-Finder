import heapq #Used for priority queue (min-heap) in A* algorithm
import sys #Used to exit the program
import time #Used to measure execution time
# ─────────────────────────────────────────────
#  Node Class
# ─────────────────────────────────────────────
class Node:
    def __init__(self, row, col, parent=None):
        self.row = row #Row position of node
        self.col = col  #Column position of node
        self.parent = parent #Parent node (used to reconstruct path)
        self.g = 0  #Cost from start to this node
        self.h = 0  #Heuristic cost to goal
        self.f = 0  #Total cost (g + h)
    def __lt__(self, other):
        return self.f < other.f #For priority queue (min-heap comparison)
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col #Node equality
    def __hash__(self):
        return hash((self.row, self.col)) #Allows node to be used in sets
# ─────────────────────────────────────────────
#  Heuristic: Manhattan Distance
# ─────────────────────────────────────────────
def heuristic(node, goal):
    return abs(node.row - goal.row) + abs(node.col - goal.col) #Calculates distance between current node and goal
# ─────────────────────────────────────────────
#  A* Algorithm
# ─────────────────────────────────────────────
def astar(grid, start, goal):
    rows = len(grid) #Number of rows in grid 
    cols = len(grid[0]) #Number of columns
    start_node = Node(start[0], start[1]) #Create start node
    goal_node  = Node(goal[0],  goal[1]) #Create goal node
    open_list   = [] #Priority queue (nodes to explore)
    closed_set  = set() #Visited nodes
    nodes_explored = 0 #Counter for explored nodes
    heapq.heappush(open_list, start_node) #Add start node to open list
    while open_list: #Loop until open list is empty
        current = heapq.heappop(open_list) #Get node with lowest f value
        nodes_explored += 1
        if current == goal_node: #If goal reached
            path = []
            while current: #Backtrack to find path
                path.append((current.row, current.col))
                current = current.parent
            return path[::-1], nodes_explored #Return reversed path
        closed_set.add((current.row, current.col)) #Mark node as visited
        # 4-directional movement (up, down, left, right)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current.row + dr, current.col + dc
#Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 1:   # 1 = wall
                    continue
                if (nr, nc) in closed_set: #If already visited
                    continue
                neighbor = Node(nr, nc, parent=current) #Create neighbor node
                neighbor.g = current.g + 1 #Cost from start
                neighbor.h = heuristic(neighbor, goal_node) #Heuristic cost
                neighbor.f = neighbor.g + neighbor.h #Total cost
 # Skip if a better path to this node is already in open list
                skip = False
                for open_node in open_list:
                    if open_node == neighbor and open_node.g <= neighbor.g:
                        skip = True
                        break
                if not skip:
                    heapq.heappush(open_list, neighbor) #Add to open list
    return None, nodes_explored   # No path found
# ─────────────────────────────────────────────
#  Grid Display
# ─────────────────────────────────────────────
def display_grid(grid, path=None, start=None, goal=None, explored=None):
#ANSI color codes
    RESET  = "\033[0m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    GRAY   = "\033[90m"
    path_set     = set(path) if path else set() #Convert path to set
    explored_set = set(explored) if explored else set()
    rows = len(grid)
    cols = len(grid[0])
    # Top border
    print("  +" + "---+" * cols) #Top border
    for r in range(rows):
        row_str = f"{r:2d}|"
        for c in range(cols):
            cell = (r, c)
            if cell == start:
                row_str += f"{GREEN} S {RESET}|"
            elif cell == goal:
                row_str += f"{RED} G {RESET}|"
            elif cell in path_set and cell != start and cell != goal:
                row_str += f"{YELLOW} * {RESET}|"
            elif grid[r][c] == 1:
                row_str += f"{GRAY}███{RESET}|"
            elif cell in explored_set:
                row_str += f"{BLUE} · {RESET}|"
            else:
                row_str += "   |"
        print(row_str)
        print("  +" + "---+" * cols)
# Column labels
    col_label = "    "
    for c in range(cols):
        col_label += f"{c:^4}"
    print(col_label)
# ─────────────────────────────────────────────
#  Preset Grids
# ─────────────────────────────────────────────
GRIDS = {
    "1": {
        "name": "Simple 8x8",
        "grid": [
            [0,0,0,0,0,0,0,0],
            [0,1,1,1,0,0,0,0],
            [0,0,0,1,0,1,1,0],
            [0,0,0,1,0,0,1,0],
            [0,0,0,0,0,0,1,0],
            [0,1,1,1,1,0,1,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0],
        ],
        "start": (0,0),
        "goal":  (7,7),
    },
    "2": {
        "name": "Maze 10x10",
        "grid": [
            [0,0,1,0,0,0,0,0,0,0],
            [0,0,1,0,1,1,1,1,0,0],
            [0,0,1,0,1,0,0,0,0,0],
            [0,0,0,0,1,0,1,1,1,0],
            [1,1,1,0,1,0,0,0,1,0],
            [0,0,1,0,0,0,1,0,1,0],
            [0,0,1,1,1,1,1,0,1,0],
            [0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0],
        ],
        "start": (0,0),
        "goal":  (9,9),
    },
    "3": {
        "name": "No path possible",
        "grid": [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [1,1,1,1,1],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        "start": (0,0),
        "goal":  (4,4),
    },
}
# ─────────────────────────────────────────────
#  Custom Grid Builder
# ─────────────────────────────────────────────
def build_custom_grid():
    print("\n── Custom Grid Builder ──")
    while True:
        try:
            rows = int(input("Enter number of rows (3-15): "))
            cols = int(input("Enter number of cols (3-15): "))
            if 3 <= rows <= 15 and 3 <= cols <= 15:
                break
            print("  Please enter values between 3 and 15.")
        except ValueError:
            print("  Invalid input. Please enter integers.")
    grid = [[0]*cols for _ in range(rows)]
    print(f"\nGrid created ({rows}x{cols}). Now add walls.")
    print("Enter wall positions as  row,col  (e.g. 2,3). Type 'done' when finished.\n")
    # Show empty grid first
    display_grid(grid)
    while True:
        raw = input("Wall position (or 'done'): ").strip()
        if raw.lower() == "done":
            break
        try:
            r, c = map(int, raw.split(","))
            if 0 <= r < rows and 0 <= c < cols:
                grid[r][c] = 1
                display_grid(grid)
            else:
                print(f"  Out of range. Row 0-{rows-1}, Col 0-{cols-1}.")
        except ValueError:
            print("  Format: row,col  (e.g. 2,3)")
 # Start and goal
    while True:
        try:
            sr, sc = map(int, input("\nStart position (row,col): ").split(","))
            gr, gc = map(int, input("Goal  position (row,col): ").split(","))
            if (0 <= sr < rows and 0 <= sc < cols and
                0 <= gr < rows and 0 <= gc < cols):
                if grid[sr][sc] == 1 or grid[gr][gc] == 1:
                    print("  Start or goal cannot be a wall.")
                else:
                    break
            else:
                print("  Positions out of range.")
        except ValueError:
            print("  Format: row,col  (e.g. 0,0)")
    return grid, (sr, sc), (gr, gc)
# ────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────
def main():
    print("\n" + "="*50)
    print("   A* ALGORITHM — SHORTEST PATH FINDER")
    print("   Fundamentals of AI and ML — BYOP")
    print("="*50)
    print("""
Legend:
  S  = Start      G  = Goal
  *  = Path       
██ = Wall
·  = Explored
""")
    while True:
        print("\n── Select a scenario ──")
        for k, v in GRIDS.items():
            print(f"  [{k}] {v['name']}")
        print("  [4] Custom grid")
        print("  [q] Quit")
        choice = input("\nYour choice: ").strip().lower()
        if choice == "q":
            print("\nGoodbye!\n")
            sys.exit(0) #Exit program
        if choice == "4":
            grid, start, goal = build_custom_grid()
            scenario_name = "Custom Grid"
        elif choice in GRIDS:
            scenario = GRIDS[choice]
            grid  = scenario["grid"]
            start = scenario["start"]
            goal  = scenario["goal"]
            scenario_name = scenario["name"]
        else:
            print("  Invalid choice.")
            continue
        print(f"\n── {scenario_name} ──")
        print(f"Start: {start}   Goal: {goal}\n")
        print("Initial grid:\n")
        display_grid(grid, start=start, goal=goal)
        input("\nPress Enter to run A*...")
        t0 = time.perf_counter() #Start timing
        path, nodes_explored = astar(grid, start, goal)
        elapsed = (time.perf_counter() - t0) * 1000 #Time in ms
        print("\n── Result ──\n")
        if path:
            display_grid(grid, path=path, start=start, goal=goal)
            print(f"\n✔ Path found!")
            print(f"   Path length    : {len(path)} steps")
            print(f"   Nodes explored : {nodes_explored}")
            print(f"   Time taken     : {elapsed:.3f} ms")
            print(f"\n   Route: {' → '.join(str(p) for p in path)}")
        else:
            display_grid(grid, start=start, goal=goal)
            print(f"\n✘ No path exists from {start} to {goal}.")
            print(f"   Nodes explored : {nodes_explored}")
            print(f"   Time taken     : {elapsed:.3f} ms")
        input("\nPress Enter to return to menu...")
if __name__ == "__main__":
    main()

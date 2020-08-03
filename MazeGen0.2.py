# Recursive stack based maze generator
from collections import Counter
import pygame
from math import ceil
import random
import time


# --------- Pygame settup --------------

# Board properties
size = (600, 600)
rows = ceil(size[0] / 25)
columns = ceil(size[1] / 25)

screen = pygame.display.set_mode(size)

print('A {} by {} maze created'.format(rows, columns))

# Block properties
width = 20
height = 20
margin = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.display.set_caption("Maze gen")

done = False
clock = pygame.time.Clock()
#---------------------------------------

#------------ Maze logic ---------------

# 2d array for creating the solution, not used during maze construction
grid = [[(0,0) for row in range(rows)] for column in range(columns)]

stack = []
visited = []
solution = []

# Returns a list of all possible non out of bounds neighbors
def getNeighbours(cell):
    top =    (cell[0], cell[1] - 1)
    left =   (cell[0] - 1, cell[1])
    bottom = (cell[0], cell[1] + 1)
    right =  (cell[0] + 1, cell[1])

    result = []
    if top[0] > -1 and top[1] > -1 and top[0] < rows and top[1] < columns:
        result.append(top)
    if left[0] > -1 and left[1] > -1 and left[0] < rows and left[1] < columns:
        result.append(left) 
    if bottom[0] > -1 and bottom[1] > -1 and bottom[0] < rows and bottom[1] < columns:
        result.append(bottom)
    if right[0] > -1 and right[1] > -1 and right[0] < rows and right[1] < columns:
        result.append(right)
    return result

# Returns a list of non visited neighbors
def checkVisited(neighbors):
    not_visited = []
    for neighbor in neighbors:
        if neighbor not in visited:
            not_visited.append(neighbor)
    return not_visited

# If the current cell has no valid neighbors, we go back until we do
def backtrack(cell):
    previous_cell = stack.pop()
    neighbors = getNeighbours(previous_cell)
    valid_neighbors = checkVisited(neighbors)
    while len(valid_neighbors) == 0:
        if len(stack) == 0:
            return 'stack is empty'
        else:
            previous_cell = stack.pop()
            visited.append(previous_cell)
            neighbors = getNeighbours(previous_cell)
            valid_neighbors = checkVisited(neighbors)
    return valid_neighbors

def drawBlock(node_lst, next_cell, color):
    # x and y are block coordinates in pixels
    y = next_cell[0] * margin
    x = next_cell[1] * margin
    c_pos = node_lst[-1]
    ex_pos = node_lst[-2]

    if ex_pos[0] - c_pos[0] > 0: # the previous cell was above the current one
        rect = pygame.draw.rect(screen, color, (x, y, width, height+10))

    elif ex_pos[0] - c_pos[0] < 0: # the previous cell was below the current one
        rect = pygame.draw.rect(screen, color, (x, y-10, width, height+10))

    elif ex_pos[1] - c_pos[1] < 0: # the previous cell was to the right
        rect = pygame.draw.rect(screen, color, (x-10, y, width+10, height))

    elif ex_pos[1] - c_pos[1] > 0: # the previous cell was to the left
        rect = pygame.draw.rect(screen, color, (x, y, width+10, height))

    pygame.display.update(rect)

def createSolution(visited):
    remove_duplicates = list(dict.fromkeys(visited))
    return remove_duplicates

def plotGrid(cell):
    neighbors = getNeighbours(cell)
    valid_neighbors = checkVisited(neighbors)
    if len(valid_neighbors) == 0:
        valid_neighbors = backtrack(cell)
        if valid_neighbors == 'stack is empty':
            return
    pick_random = random.randint(0, len(valid_neighbors)-1)
    next_cell = valid_neighbors[pick_random]
    visited.append(next_cell)
    stack.append(next_cell)
    drawBlock(visited, next_cell, WHITE)
    return next_cell

# Start
start = (0, 0)
rect = pygame.draw.rect(screen, WHITE, (start[0], start[1], width, height))
pygame.display.update(rect)
visited.append(start)
stack.append(start)
next_cell = plotGrid(start)

all_cells = columns * rows

while len(stack) != 0:
    next_cell = plotGrid(next_cell)
    time.sleep(0.01)

# rect = pygame.draw.rect(screen, RED, (start[0], start[1], width, height))
# pygame.display.update(rect)
# index = 1
# for cell in createSolution(visited):
#     if cell == (0, 0):
#         pass
#     else:
#         if cell == (rows-1, columns-1):
#             drawBlock(visited, cell, GREEN)
#             break
#         else:
#             drawBlock(visited, cell, RED)
#             time.sleep(0.1)
        


#---------------------------------------
# Helper function for color toggling <notInUse>

def switchVal(grid):
    val = {
            1 : 0,
            0 : 1,
            }
    return val.get(grid)
#---------------------------------------

# -------- Main Program Loop -----------

while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #mouse_pos = pygame.mouse.get_pos()
            # mouse pos in pixels / margin and rounded up = mouse pos in cols and rows
            #mouse_x = ceil(mouse_pos[1] / margin)
            #mouse_y = ceil(mouse_pos[0] / margin)
            # flips the cell's value (toggles color)
            #grid[mouse_x-1][mouse_y-1] = switchVal(grid[mouse_x-1][mouse_y-1])

            #print('Row: {}, Col: {}'.format(mouse_x-1, mouse_y-1))

    screen.fill(BLACK)

    # --- Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()
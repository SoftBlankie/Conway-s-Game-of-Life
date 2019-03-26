from time import sleep
from random import randint
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def createScreen(fullscreen):
    if (fullscreen):
        screen_width, screen_height = pygame.display.list_modes(0)[0]
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    else:
        screen_width, screen_height = (600,600)
        flags = 0

    screen = pygame.display.set_mode(
            (screen_width, screen_height), flags)
    print("screen size:", screen.get_size())
    return screen

def make_empty_grid(x, y):
    grid = []
    for i in range(x):
        row = []
        for j in range(y):
            row.append(0)
        grid.append(row)
    return grid

def make_random_grid(x, y):
    grid = []
    for i in range(x):
        row = []
        for j in range(y):
            row.append(randint(0,1))
        grid.append(row)
    return grid

# Check if cell should be evolved
def evolve_cell(alive, neighbors):
    return neighbors == 3 or (alive and neighbors == 2)

# Count number of alive neighbor cells
def count_neighbors(grid, position):
    x,y = position
    neighbor_cells = [(x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                      (x + 0, y - 1),                 (x + 0, y + 1),
                      (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)]
    count = 0
    for x,y in neighbor_cells:
        if x >= 0 and y >= 0:
            try:
                count += grid[x][y]
            except:
                pass
    return count

# Create or kill cells 
def evolve(grid):
    x = len(grid)
    y = len(grid[0])
    new_grid = make_empty_grid(x, y)
    for i in range(x):
        for j in range(y):
            cell = grid[i][j]
            neighbors = count_neighbors(grid, (i, j))
            new_grid[i][j] = 1 if evolve_cell(cell, neighbors) else 0
    return new_grid

# Draw cells as small circles
def draw_block(x, y, alive_color):
    block_size = 9
    x *= block_size
    y *= block_size
    center = ((x + block_size // 2)), (y + (block_size // 2))
    pygame.draw.circle(screen, alive_color, center, block_size // 2,0)

# Handle key input
# spacebar : reset simulation
# f        : toggle fullscreen
# esc      : exit
# Change alive cell color
# 1        : Teal
# 2        : Red
# 3        : Blue
# 4        : Yellow
# 5        : Green
def draw_instr():
    text = pygame.font.SysFont("Gill Sans", 14)
    txt_color = WHITE

    pygame.draw.rect(screen, WHITE, (20, 5, 180, 200), 1)

    # Display key inputs
    input_space = text.render("Spacebar : Reset", False, txt_color)
    input_f = text.render("f : Toggle fullscreen", False, txt_color)
    input_esc = text.render("esc : Exit program", False, txt_color)

    screen.blit(input_space, (30, 10))
    screen.blit(input_f, (30, 30))
    screen.blit(input_esc, (30, 50))

    # Display alive cell colors
    input_1 = text.render("1 : Teal", False, txt_color)
    input_2 = text.render("2 : Red", False, txt_color)
    input_3 = text.render("3 : Blue", False, txt_color)
    input_4 = text.render("4 : Yellow", False, txt_color)
    input_5 = text.render("5 : Green", False, txt_color)

    screen.blit(input_1, (30, 100))
    screen.blit(input_2, (30, 120))
    screen.blit(input_3, (30, 140))
    screen.blit(input_4, (30, 160))
    screen.blit(input_5, (30, 180))


def handleInputEvents():
    global grid, screen, h, xlen, ylen

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                grid = make_random_grid(xlen, ylen)
            elif (event.key == pygame.K_f):
                if (screen.get_flags() & pygame.FULLSCREEN):
                    screen = createScreen(False)
                    (xmax,ymax) = screen.get_size()
    
                    xlen = xmax // 9
                    ylen = ymax // 9
    
                    grid = make_random_grid(xlen, ylen)
                else:
                    screen = createScreen(True)
                    (xmax,ymax) = screen.get_size()
    
                    xlen = xmax // 9
                    ylen = ymax // 9
    
                    grid = make_random_grid(xlen, ylen)
            elif (event.key == pygame.K_ESCAPE):
                exit(0)
            elif (event.key == pygame.K_1):
                h = 150
            elif (event.key == pygame.K_2):
                h = 0
            elif (event.key == pygame.K_3):
                h = 250
            elif (event.key == pygame.K_4):
                h = 50
            elif (event.key == pygame.K_5):
                h = 100
            elif (event.type == pygame.QUIT):
                print("quitting")
                exit(0)

def main():
    global grid, screen, h, xlen, ylen
    
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    screen = createScreen(True)
    (xmax,ymax) = screen.get_size()

    h = 0
    alive_color = pygame.Color(0,0,0)
    alive_color.hsva = [h, 100, 100]
    xlen = xmax // 9
    ylen = ymax // 9
    
    grid = make_random_grid(xlen, ylen)
    
    while True:
        handleInputEvents()
        clock.tick(60)
        for x in range(xlen):
            for y in range(ylen):
                alive = grid[x][y]
                cell_color = alive_color if alive else BLACK
                draw_block(x, y, cell_color)
        draw_instr()
        pygame.display.flip()
        h = (h + 2) % 360
        alive_color.hsva = (h, 100, 100)
        grid = evolve(grid)

main()

'''
Python implementation of Conway's Game of Life

Original author: Mahesh Venkitachalam

Slight modifications by me
'''

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def random_grid(size):
    '''Creates a grid with randomly chosen ON/OFF cells'''
    return np.random.choice(vals, size).reshape(size, size)

def update(frame_num, img, grid, size):
    new_grid = grid.copy()

    #Doing rule checks
    for x in range(size):
        for y in range(size):
            #Checking order:  1    2   3
            #                 4  cell  5
            #                 6    7   8
            #We get the sum of all cell values to divide
            #by 255 for finding how many neighbours are there
            total = int((grid[(x-1)%size, (y-1)%size] +
                         grid[x, (y-1)%size] +
                         grid[(x+1)%size, (y-1)%size] +
                         grid[(x-1)%size, y] +
                         grid[(x+1)%size, y] +
                         grid[(x-1)%size, (y+1)%size] +
                         grid[x, (y+1)%size] +
                         grid[(x+1)%size, (y+1)%size]
                        )/255)

            if grid[x, y] == ON:
                if (total < 2) or (total > 3):
                    new_grid[x, y] = OFF
            else:
                if total == 3:
                    new_grid[x, y] = ON

    #Updating the data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

def add_glider(x, y, grid):
    '''Adds a glider with top left cell at (x, y)'''

    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])

    #From x to x+3, get 'glider's x values
    #From y to y+3, get 'glider's y values
    grid[x:x+3, y:y+3] = glider

def add_object(grid, x, y, cell_arr, size):
    '''Adds an object with top left cell at (x,y)'''

    cell = cell_arr
    grid[x:x+size, y:y+size] = cell

def main():
    '''The main program'''

    parser = argparse.ArgumentParser(description="Conway's Game of Life.")
    parser.add_argument('--grid-size', dest='grid_size', required=False)
    parser.add_argument('--movfile-name', dest='movfile_name', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--random', dest='random', required=False)
    args = parser.parse_args()

    #Setting the grid size
    size = 100
    if args.grid_size and int(args.grid_size) > 8:
        size = int(args.grid_size)
    
    #Animation interval
    anim_interval = 50
    if args.interval:
        anim_interval = int(args.interval)

    #Setting the grid
    grid = np.zeros(size*size).reshape(size, size)
    if args.random:
        grid = random_grid(size)

    add_glider(1, 1, grid)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')

    #Animation part
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid, size, ),
                                   frames=60, interval=anim_interval, save_count=50)

    if args.movfile_name:
        anim.save(args.movfile_name, writer='imagemagick', fps=10, extra_args=['-vcodec', 'libx264'])

    plt.show()

if __name__ == "__main__":
    main()

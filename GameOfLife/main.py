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
from multiprocessing import Process, Pool
#from patterns import pattern_list
from patterns import Pattern

ON = 255
OFF = 0
vals = [ON, OFF]
#pattern_path = "./PatternFiles"
pattern_list = []

def load_patterns():
    '''Loads patterns from local .txt files'''
    global pattern_list
    Pattern(auto_load=True, filename="glider.txt", pat_list=pattern_list, to_list=True)
    Pattern(auto_load=True, filename="pentadecathlon.txt", pat_list=pattern_list, to_list=True)
    Pattern(auto_load=True, filename="t_tetromino.txt", pat_list=pattern_list, to_list=True)

def random_grid(size):
    '''Creates a grid with randomly chosen ON/OFF cells'''
    return np.random.choice(vals, size).reshape(size, size)

def update(frame_num, img, grid, size):
    '''Function to check the game's rules and apply them'''
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
                         grid[(x-1)%size, y] +
                         grid[(x-1)%size, (y+1)%size] +
                         grid[x, (y-1)%size] +
                         grid[x, (y+1)%size] +
                         grid[(x+1)%size, (y-1)%size] +
                         grid[(x+1)%size, y] +
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

def find_object(name, object_list):
    '''Finds the pattern in the pattern_list'''
    pass

def add_object(grid, x, y, cell_arr, size_x, size_y):
    '''Adds an object with top left cell at (x,y)'''

    cell_pat = np.zeros(size_x*size_y).reshape(size_y, size_x)

    for cell in cell_arr:
        #print(f"x: {cell[0]}, y: {cell[1]}")
        cell_pat[cell[1]][cell[0]] = 255

    grid[y:y+size_y, x:x+size_x] = cell_pat

def run_anim(grid, size, interval, filename):
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='gray')    

    #Animation part
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid, size, ),
                                   frames=60, interval=interval, save_count=50)

    if filename:
        anim.save(filename, writer='imagemagick', fps=10, extra_args=['-vcodec', 'libx264'])

    #plt.grid(which='both', color='gray')
    #plt.minorticks_on()
    plt.show()

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

    #add_glider(10 , 1, grid)
    add_object(grid, 9, 0, pattern_list[0].cells, pattern_list[0].size_x, pattern_list[0].size_y)
    add_object(grid, 16, 16, pattern_list[1].cells, pattern_list[1].size_x, pattern_list[1].size_y)

    #Stops at proc.join() until the window is closed
    #proc = Process(target=run_anim, args=(grid, size, anim_interval, args.movfile_name))
    #proc.start()
    #Some kind of input
    #add_object(grid, 4, 4, pattern_list[2].cells, pattern_list[2].size_x, pattern_list[2].size_y)
    #Output
    #proc.join()

    run_anim(grid, size, anim_interval, args.movfile_name)

if __name__ == "__main__":
    load_patterns()
    main()

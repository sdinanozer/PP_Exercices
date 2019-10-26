'''
Pattern class for easier use of Conway's Game of Life
'''

import numpy as np

pattern_list = []

class Pattern():
    def __init__(self, name, size_x, size_y, pat_type, cells=[()]):
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.pat_type = pat_type
        self.cells = cells
        pattern_list.append(self)

glider_arr = np.array([(2, 0), (0, 1),
                       (2, 1), (1, 2),
                       (2, 2)])
glider_pat = Pattern(name = "Glider",
                     size_x = 3,
                     size_y = 3,
                     pat_type = "Spaceship",
                     cells = glider_arr)

pen_dec_arr = np.array([(2, 0), (7, 0),
                        (0, 1), (1, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 1), (9, 1),
                        (2, 2), (7, 2)])
pen_dec_pat = Pattern(name = "Pentadecathlon",
                      size_x = 10,
                      size_y = 3,
                      pat_type = "Oscillators",
                      cells = pen_dec_arr)

pattern_list.sort(key = lambda pattern: pattern.name)

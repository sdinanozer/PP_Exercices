'''
Pattern class for easier use of Conway's Game of Life
'''

import os
import numpy as np


class Pattern():
    pattern_path = "./PatternFiles"
    
    def __init__(self, name="", pat_type="", size_x=0, size_y=0, cells=[],
                 pat_list=[], to_list=False, auto_load=False, filename=""):
        if not auto_load:
            self.name = name
            self.pat_type = pat_type
            self.size_x = size_x
            self.size_y = size_y
            self.cells = cells
        else:
            self.get_pattern(filename)

        if to_list:
            pat_list.append(self)

    def get_pattern(self, filename):
        cell_arr = []
        filename = os.path.join(Pattern.pattern_path, filename)

        try:
            with open(filename, "r") as pattern_file:
                self.name = pattern_file.readline().rstrip()
                self.pat_type = pattern_file.readline().rstrip()
                self.size_x = int(pattern_file.readline().rstrip())
                self.size_y = int(pattern_file.readline().rstrip())

                for line in pattern_file:
                    cur_vals = line.split(",")
                    cur_cell = (int(cur_vals[0]), int(cur_vals[1]))
                    cell_arr.append(cur_cell)

            self.cells = cell_arr
        except FileNotFoundError as error:
            print("Failed to load pattern.")
            print(error)
            print("Please enter the correct filename or make sure the file exists...")

    def export_pattern(self, filename):
        filename = os.path.join(Pattern.pattern_path, filename)

        with open(filename, "w") as pattern_file:
            try:
                pattern_file.write(f"{self.name}\n")
                pattern_file.write(f"{self.pat_type}\n")
                pattern_file.write(f"{self.size_x}\n")
                pattern_file.write(f"{self.size_y}\n")

                for ctr in range(len(self.cells)):
                    pat_str = ','.join([str(num) for num in self.cells[ctr]])
                    pattern_file.write(f"{pat_str}\n")
            except AttributeError as error:
                print("Failed to export pattern.")
                print(error)
                print("Please make sure the pattern is loaded correctly...")

#pattern_list.sort(key = lambda pattern: pattern.name)

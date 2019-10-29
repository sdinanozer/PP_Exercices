'''
Pattern class for easier use of Conway's Game of Life
'''

import os
import numpy as np
from PIL import Image

class Pattern():
    pattern_path = "./PatternFiles"
    pattern_list = []
    
    def __init__(self, name="", pat_type="", size_x=0, size_y=0, cells=[],
                 pat_list=[], to_list=True, auto_load=True, filename=""):
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
        filename_txt = ".".join((filename, "txt"))
        filename_txt = os.path.join(Pattern.pattern_path, filename_txt)

        try:
            with open(filename_txt, "r") as pattern_file:
                self.name = pattern_file.readline().rstrip()
                self.pat_type = pattern_file.readline().rstrip()
                self.size_x = int(pattern_file.readline().rstrip())
                self.size_y = int(pattern_file.readline().rstrip())

                for line in pattern_file:
                    cur_vals = line.split(",")
                    cur_cell = (int(cur_vals[0]), int(cur_vals[1]))
                    cell_arr.append(cur_cell)

            if cell_arr:
                self.cells = cell_arr
            else:
                self.pat_from_img(filename)

        except FileNotFoundError as error:
            print("Failed to load pattern.")
            print(error)
            print("Please enter the correct filename or make sure the file exists...")

    def export_pattern(self, filename):
        filename_txt = ".".join((filename, "txt"))
        filename_txt = os.path.join(Pattern.pattern_path, filename_txt)

        print("1- Save as .txt only (cell coordinates are written inside)")
        print("2- Save as .txt and .png")
        answer = int(input("Your choice: "))

        with open(filename_txt, "w") as pattern_file:
            try:
                pattern_file.write(f"{self.name}\n")
                pattern_file.write(f"{self.pat_type}\n")
                pattern_file.write(f"{self.size_x}\n")
                pattern_file.write(f"{self.size_y}\n")

                if answer == 1:
                    for d in range(len(self.cells)):
                        pat_str = ','.join([str(num) for num in self.cells[d]])
                        pattern_file.write(f"{pat_str}\n")
                elif answer == 2:
                    self.pat_to_img(filename)
                else:
                    "Invalid answer, exporting cell coordinates failed."

            except AttributeError as error:
                print("Failed to export pattern.")
                print(error)
                print("Please make sure the pattern is loaded correctly...")

    def pat_from_img(self, filename):
        filename = ".".join((filename, "png"))
        filename = os.path.join(Pattern.pattern_path, filename)

        img = Image.open(filename)
        pix_arr = img.load()
        cell_arr = []

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix_val = pix_arr[x,y]
                total = pix_val[0] + pix_val[1] + pix_val[2]

                if total < 100:
                    cur_cell = (x, y)
                    cell_arr.append(cur_cell)

        self.cells = cell_arr

    def pat_to_img(self, filename):
        filename = ".".join((filename, "png"))
        filename = os.path.join(Pattern.pattern_path, filename)

        img_x = self.size_x
        img_y = self.size_y
        img_size = (img_x, img_y)
        
        pix_arr = [[(255, 255, 255) for d in range(img_y)] for i in range(img_x)]

        for cell in self.cells:
            pix_arr[cell[0]][cell[1]] = (0,0,0)

        new_arr = []
        for x in range(img_x):
            for y in range(img_y):
                new_arr.append(pix_arr[x][y])

        img = Image.new('RGB', img_size)
        print(new_arr)
        img.putdata(new_arr)
        img.save(filename, 'PNG')

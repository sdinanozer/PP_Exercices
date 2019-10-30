'''Python library to import Pattern class'''

import os
from PIL import Image

class Pattern():
    '''Pattern class for easier use of Conway's Game of Life'''
    pattern_path = "./PatternFiles"
    pattern_list = []

    def __init__(self, name="", pat_type="", size_x=0, size_y=0, cells=[],
                 pat_list=[], to_list=True, filename=""):
        '''Sets the values of Pattern object'''
        if not filename:
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
        '''Loads the pattern data from .txt and .png files'''
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
        '''Exports the pattern to .txt or .png files'''
        filename_txt = ".".join((filename, "txt"))
        filename_txt = os.path.join(Pattern.pattern_path, filename_txt)

        print("1- Save as .txt only (cell coordinates are written inside)")
        print("2- Save as .txt and .png (cell coordinates are drawn)")
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
                    print("Invalid answer, exporting to .txt file as default")
                    for d in range(len(self.cells)):
                        pat_str = ','.join([str(num) for num in self.cells[d]])
                        pattern_file.write(f"{pat_str}\n")

            except AttributeError as error:
                print("Failed to export pattern.")
                print(error)
                print("Please make sure the pattern is loaded correctly...")

    def pat_from_img(self, filename):
        '''
        Gets cell coordinates from given .png file.
        Every cell must be one pixel sized.
        '''
        filename = ".".join((filename, "png"))
        filename = os.path.join(Pattern.pattern_path, filename)

        img = Image.open(filename)
        pix_arr = img.load()
        cell_arr = []

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix_val = pix_arr[x, y]
                total = pix_val[0] + pix_val[1] + pix_val[2]

                if total < 100:
                    cur_cell = (x, y)
                    cell_arr.append(cur_cell)

        self.cells = cell_arr

    def pat_to_img(self, filename):
        '''
        Saves a .png version of the pattern.
        Every cell will be drawn as one pixel.
        '''
        filename = ".".join((filename, "png"))
        filename = os.path.join(Pattern.pattern_path, filename)

        img_size = (self.size_x, self.size_y)

        new_img = Image.new('RGB', img_size, (255, 255, 255))

        for cell in self.cells:
            new_img.putpixel(cell, (0, 0, 0))

        new_img.save(filename, 'PNG')

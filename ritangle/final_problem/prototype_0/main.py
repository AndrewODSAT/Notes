import math
import tkinter

""" https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html """
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

class PlaneGUI:
    def __init__(self, cell):
        self.cell = cell

    def run(self):
        self.initialize_gui()

    def initialize_gui(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Ritangle Final Question")

        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect("equal", adjustable="box")

        self.ax.set_xlim(-1, self.cell.width + 1)
        self.ax.set_ylim(-1, self.cell.height + 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.add_circle_frame = tkinter.Frame(self.root)
        tkinter.Button(self.add_circle_frame, text="Add Circle", command=lambda: print("You tried"))

        self.root.after(50, self.update_gui)

        tkinter.mainloop()

    """ This function will draw the disk at its centre but will
        also draw the disk on it opposite side if it goes over the
        cell edge (so it is like there are other cells surrounding it"""
    def draw_disk(self, disk, centre):
        self.ax.add_artist(plt.Circle(centre, disk.r, fill=False))
        all_dx = [0]
        all_dy = [0]

        if centre[0] + disk.r > self.cell.width:
            all_dx.append(-self.cell.width)
        elif centre[0] - disk.r < 0:
            all_dx.append(self.cell.width)
        if centre[1] + disk.r > self.cell.height:
            all_dy.append(-self.cell.height)
        elif centre[1] - disk.r < 0:
            all_dy.append(self.cell.height)

        for dx in all_dx:
            for dy in all_dy:
                self.ax.add_artist(plt.Circle((centre[0]+dx, centre[1]+dy), disk.r, fill=False))

    def update_gui(self):
#        print(f"Points: {self.cell.calc_points_in_disks()}")
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()
        self.ax.clear()
        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)

        self.ax.add_artist(plt.Rectangle((0, 0), width=self.cell.width, height=self.cell.height, fill=False))

        # Drawing integer grid points
        for p in self.cell.grid_points:
            self.ax.plot(p[0], p[1], "o", markersize=2)

        # Drawing disk
        for disk in self.cell.disks:
            for centre in disk.centres:
                self.draw_disk(disk, centre)

        self.root.after(100, self.update_gui)

""" This models the disk, it shouldn't do checking if point in
    itself as the unit cell can have like a cyclic property"""
class Disk:
    def __init__(self, r):
        self.centres = set()
        self.r = r
        self.area = math.pi * r**2

    def add_disk(self,centre):
        self.centres.add(centre)

    def remove_disk(self, centre):
        self.centres.remove(centre)

    def change_r(self, new_r):
        self.r = new_r
        self.area = math.pi * r**2

    def output(self):
        print(f"Radius: {self.r}")
        print(f"    Area: {self.area}")
        print(f"    Centres: ")
        print(f"        ({self.c[0]}, {self.c[1]})")
        print()

# currently square
class UnitCell:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.disks = []

        # test data
        self.disks = [Disk(5), Disk(1), Disk(2)]
        self.add_disk(self.disks[0], (0,0))

        self.grid_points = self.gen_points()
        self.cell_area = self.width * self.height

        self.gui = PlaneGUI(self)

    def output_disks(self):
        for disk in self.disks:
            disk.output()

    def p_fits_in_grid(self, point):
        if point[0] >= 0 and point[0] <= self.width\
        and point[1] >=0 and point[1] <= self.height:
            return True
        return False
    
    """Generates integer points of unit cell"""
    def gen_points(self):
        points = []
        for x in range(self.width):
            for y in range(self.height):
                points.append((x, y))
        return points

    """ Calculates the points in the disk by just checking if
        min distance is <= radius"""
#   def calc_points(self):
#        points = self.get_points_in_disks()
#        for point in points:
#            if point

    def get_points_in_disks(self):
        points = set()
        for disk in self.disks:
            for centre in disk.centres:
                for point in self.grid_points:
                    if self.min_distance(centre, point) <= disk.r:
                        points.add(point)
        return points

    """ If the sum of the radii is greater than min distance then they overlap"""
    def is_disk_overlapping(self, disk_0, centre_0):
        for disk_1 in self.disks:
            for centre_1 in disk_1.centres:
                if self.min_distance(centre_0, centre_1) < (disk_0.r + disk_1.r):
                    return True
        return False

    def add_disk(self, disk, centre):
        if self.p_fits_in_grid(centre) and not self.is_disk_overlapping(disk, centre):
            disk.add_disk(centre)
            return True
        print("Failed to add disk")
        return False

    def min_distance(self, p_0, p_1):
        # because it can wrap around and the distance 
        # from a point to itself is self.width the alternative
        # distance is width - distance
        direct_dist_x = abs(p_0[0] - p_1[0])
        direct_dist_y = abs(p_0[1] - p_1[1])

        cyclic_dist_x = abs(self.width - direct_dist_x)
        cyclic_dist_y = abs(self.height - direct_dist_y)

        if direct_dist_x <= cyclic_dist_x:
            min_x_dist = direct_dist_x
        else:
            min_x_dist = cyclic_dist_x

        if direct_dist_y <= cyclic_dist_y:
            min_y_dist = direct_dist_y
        else:
            min_y_dist = cyclic_dist_y

        total_dist = (min_x_dist**2 + min_y_dist**2)**(1/2)

        return total_dist

# MAIN
cell = UnitCell(10, 10)
cell.gui.run()

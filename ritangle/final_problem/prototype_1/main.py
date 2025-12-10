import tkinter
from tkinter import simpledialog
import math
import cProfile
import pstats

""" https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html """
""" https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py"""
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Polygon, Point, LineString
from shapely.affinity import translate
from shapely.creation import points
from shapely.strtree import STRtree
from shapely.prepared import prep

import numpy as np


class PlaneGUI:
    def __init__(self, unit_cell):
        self.unit_cell = unit_cell

    def run(self):
        self.initialize_gui()

    def initialize_gui(self):
        self.root = tkinter.Tk()
        self.root.title("Ritangle Final Question")

        self.canvas = tkinter.Canvas(self.root)
        self.canvas.pack(side="left", fill="both", anchor='nw')#, expand=True)

        self.panel = tkinter.Frame(self.root)
        self.panel.pack(side="right", fill="y")

        tkinter.Label(self.panel, text="Circles (x y r per line):").pack()

        self.text = tkinter.Text(self.panel, width=25, height=40)
        self.text.pack()

        self.update_btn = tkinter.Button(self.panel, text="Update Circles",
                                    command=self.update_circles)
        self.update_btn.pack(pady=10)

        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlim(-5,5)
        self.ax.set_ylim(-5,5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root) 
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.update_text_box()

        tkinter.mainloop()

    def update_text_box(self):
        self.text.delete(1.0, tkinter.END)
        for vertex in self.unit_cell.polygon.exterior.coords[:-1]:
            self.text.insert(tkinter.END, str(vertex[0])+','+str(vertex[1]) + ' ')
        self.text.insert(tkinter.END, "\n")
        self.text.insert(tkinter.END, str(self.unit_cell.t_vectors[0][0]) + ',' +str(self.unit_cell.t_vectors[0][1]) + ' ')
        self.text.insert(tkinter.END, str(self.unit_cell.t_vectors[1][0]) + ',' +str(self.unit_cell.t_vectors[1][1]) + ' ')

    def update_circles(self):
        raw = self.text.get("1.0", "end").strip()
        self.unit_cell.fundamental_circles = []

        lines = raw.splitlines()
        if len(lines) < 2:
            return None

        #vertices_parts = lines[0].strip().split()
        #vertices = [list(map(float, x_y_pair.split(","))) for x_y_pair in vertices_parts]
        #_vector_parts = lines[1].strip().split()
        #_vectors = [list(map(float, x_y_pair.split(","))) for x_y_pair in t_vector_parts]
        ref_point, angle, side_length = lines[0].strip().split()
        ref_point = ref_point.split(",")
        angle = float(angle)
        side_length = float(side_length)

        self.unit_cell.set_polygon_parallelogram(ref_point, side_length, angle)
#        self.unit_cell.polygon = Polygon(vertices)
        # self.unit_cell.t_vectors = t_vectors

        for line in raw.splitlines()[2:]:
            if line.strip() == "":
                continue
            parts = line.split()
            if len(parts) != 3:
                print("Skipping bad line:", line)
                continue
            x, y, r = float(parts[0]), float(parts[1]), float(parts[2])
            self.unit_cell.fundamental_circles.append(Point(x,y).buffer(r))

        self.unit_cell.update_all_circles()
        self.unit_cell.polygon_grid_points = self.unit_cell.grid_points_covered_by_polygon()
        self.update_gui()
        print("Updated circles")
        print(f"P: {self.unit_cell.calculate_p()}")

    def get_circle_radius(circle):
        cx, cy = circle.x, circle.y
        px, py = circle.exterior.coords[0]
        return ((px-cx)**2 + (py-cy)**2)**0.5

    def draw_polygon(self, polygon):
        polygon_patch = MplPolygon(list(polygon.exterior.coords),
                                   closed=True, fill=False, edgecolor="red", linewidth=4)
        self.ax.add_patch(polygon_patch)

    def draw_circle(self, circle):
        patch = MplPolygon(list(circle.exterior.coords),
                                   closed=True, fill=False, edgecolor="red")
        self.ax.add_patch(patch)

    def update_gui(self):
        self.ax.clear()
        self.draw_polygon(self.unit_cell.polygon)
        for circle in self.unit_cell.all_circles:
            self.draw_circle(circle)
        for point in self.unit_cell.polygon_grid_points:
            self.ax.plot(point.x, point.y, 'o', color="red")

        for point in self.unit_cell.grid_points_covered_by_circles():
            self.ax.plot(point.x, point.y, 'o', color="green")

        self.ax.grid(True)
        #self.ax.autoscale_view()
        self.ax.set_aspect("equal", adjustable="box")

        plt.show()
        self.canvas.draw()
        self.root.update()

class UnitCell:
    def __init__(self, polygon, translation_vectors, radii):
        self.polygon = polygon

        self.t_vectors = translation_vectors
        self.fundamental_circles = []
        self.radii = radii

        self.set_polygon_parallelogram((0,0), 6, math.pi/3)
        self.polygon_grid_points = self.grid_points_covered_by_polygon()

        self.update_all_circles()

    def set_polygon_parallelogram(self, reference_point, s, angle_deg):
        angle_rad = math.radians(angle_deg)
        vertices = [(0,0), 
                    (s*math.cos(angle_rad), s*math.sin(angle_rad)),
                    (s+s*math.cos(angle_rad), s*math.sin(angle_rad)),
                    (s, 0)]
        self.polygon = Polygon(vertices)
        self.t_vectors = [(s*math.cos(angle_rad),s*math.sin(angle_rad)), (s, 0)]

    def grid_points_covered_by_polygon(self):
        min_x, min_y, max_x, max_y = self.polygon.bounds
        preped_polygon = prep(self.polygon)

        integer_points = []
        for x in range(math.floor(min_x), math.ceil(max_x)+1):
            for y in range(math.floor(min_y), math.ceil(max_y)+1):
                p = Point(x,y)
                if preped_polygon.contains(p) or preped_polygon.touches(p):
        #                or (x,y) in list(self.polygon.exterior.coords):
                    integer_points.append(p)
        return integer_points

    def calculate_p(self):
        for p_0 in self.grid_points_covered_by_polygon():
            found = False
            for p_1 in self.polygon_grid_points:
                if p_0.x==p_1.x and p_0.y==p_1.y:
                    found = True
            if not found:
                return -1

        tolerance = 1*10**(-8)
        p_score = 0
        uncovered = 0
        for p in self.polygon_grid_points:
            found = False
            for vertex in self.polygon.exterior.coords[:-1]:
                # if on vertex
                if abs(vertex[0]-p.x) < tolerance and abs(vertex[1]-p.y) < tolerance:
                # internal angle = 180(num_sides-2)/num_sides
                #                = 180 - 360/num_sides
                # num vertex meeting = 360/internal angle
                #                    = 360/(180 - 360/num_sides)
                #                    = 360*num_sides/(180*num_sides - 360)
                #                    = 2*num_sides/(num_sides - 2)
                    n = len(self.polygon.exterior.coords) - 1 # includes the last one
                    p_score += 1 / (2*n/(n-2))
                    found = True
                    break
            if found:
                continue
            # this is needed and not touches because of floating point precision
            elif self.polygon.exterior.distance(p) < tolerance:
                p_score += 1/2
            elif p.within(self.polygon):
                p_score += 1
            else:
                uncovered += 1

        p_score = p_score / (len(self.fundamental_circles) + uncovered)

        return p_score

    def grid_points_covered_by_circles(self):
        tolerance = 1*10**(-8)
        integer_points = []
        for p in self.polygon_grid_points:
            circles = self.circle_index.query(p)
            for c in circles:
                if p.within(c)\
                or c.exterior.distance(p) < tolerance:
                    integer_points.append(p)
                    break
        return integer_points

    def update_all_circles(self):
        self.all_circles = list(self.fundamental_circles)
        for circle in self.fundamental_circles:
            self.all_circles.extend(self.gen_wrapped_copies(circle))

        self.circle_index = STRtree(self.all_circles)

    def gen_wrapped_copies(self, circle):
        copies = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue  # skip the original

                dx = i * self.t_vectors[0][0] + j * self.t_vectors[1][0]
                dy = i * self.t_vectors[0][1] + j * self.t_vectors[1][1]

                new_circle = translate(circle, xoff=dx, yoff=dy)
                if self.polygon.intersects(new_circle):
                    copies.append(new_circle)
        return copies

# test shapes
polygon = Polygon([[0,0], [0,10], [10,10], [10,0]])
translation_vectors = np.array([(10,0), (0,10)])

unit_cell = UnitCell(polygon, translation_vectors, [1, 1, 1])
gui = PlaneGUI(unit_cell)
gui.run()

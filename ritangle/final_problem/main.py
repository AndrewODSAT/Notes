import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import math

# -------------------------------------------------------------
# Human-ish lattice packing exploration tool
# -------------------------------------------------------------
# This script lets you experiment with translation lattices and disc
# positions. It isn’t optimized, but it’s meant to feel like something
# a human would reasonably write in a week while exploring ideas.
# -------------------------------------------------------------

class PackingExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lattice Packing Explorer")

        # Default parameters
        self.num_points = tk.IntVar(value=15)
        self.radius = tk.DoubleVar(value=0.2)
        self.v1x = tk.DoubleVar(value=1.0)
        self.v1y = tk.DoubleVar(value=0.0)
        self.v2x = tk.DoubleVar(value=0.5)
        self.v2y = tk.DoubleVar(value=math.sqrt(3)/2)

        self.points = []

        self._build_ui()
        self._build_plot()

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Number of random points:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.num_points, width=10).grid(row=0, column=1)

        ttk.Label(frame, text="Disc radius:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.radius, width=10).grid(row=1, column=1)

        ttk.Label(frame, text="v1 (x, y):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.v1x, width=7).grid(row=2, column=1, sticky="w")
        ttk.Entry(frame, textvariable=self.v1y, width=7).grid(row=2, column=2, sticky="w")

        ttk.Label(frame, text="v2 (x, y):").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.v2x, width=7).grid(row=3, column=1, sticky="w")
        ttk.Entry(frame, textvariable=self.v2y, width=7).grid(row=3, column=2, sticky="w")

        ttk.Button(frame, text="Generate points", command=self.generate_points).grid(row=4, column=0, pady=5)
        ttk.Button(frame, text="Plot", command=self.update_plot).grid(row=4, column=1, pady=5)

    def _build_plot(self):
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1)

    def generate_points(self):
        self.points = [(random.random(), random.random()) for _ in range(self.num_points.get())]
        self.update_plot()

    def update_plot(self):
        self.ax.clear()

        # Draw unit cell parallelogram
        v1 = (self.v1x.get(), self.v1y.get())
        v2 = (self.v2x.get(), self.v2y.get())

        cell = [(0,0), v1, (v1[0]+v2[0], v1[1]+v2[1]), v2]
        cx = [p[0] for p in cell] + [cell[0][0]]
        cy = [p[1] for p in cell] + [cell[0][1]]
        self.ax.plot(cx, cy)

        # Helper: wrap point into torus-like coordinates
        def wrap_point(x, y):
            # Solve for coordinates in lattice basis to wrap into unit cell
            # Based on solving a * v1 + b * v2 = (x, y)
            det = v1[0]*v2[1] - v1[1]*v2[0]
            if abs(det) < 1e-12:
                return x, y  # Degenerate lattice
            a = (x*v2[1] - y*v2[0]) / det
            b = (-x*v1[1] + y*v1[0]) / det
            # Wrap into [0,1)
            a = a % 1
            b = b % 1
            # Convert back to real coords
            rx = a*v1[0] + b*v2[0]
            ry = a*v1[1] + b*v2[1]
            return rx, ry

        # Plot points & discs plus wrapped copies in 8 surrounding tiles
        r = self.radius.get()
        shifts = [(i, j) for i in (-1,0,1) for j in (-1,0,1)]

        for (x, y) in self.points:
            # plot wraps
            for (i, j) in shifts:
                sx = x + i*v1[0] + j*v2[0]
                sy = y + i*v1[1] + j*v2[1]
                wx, wy = wrap_point(sx, sy)
                circ = matplotlib.patches.Circle((wx, wy), r, fill=False)
                self.ax.add_patch(circ)
                self.ax.plot(wx, wy, 'o')

        self.ax.set_xlim(-0.2, 1.2)
        self.ax.set_ylim(-0.2, 1.2)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = PackingExplorer(root)
    root.mainloop()


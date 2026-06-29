# How to Generate Mesh in Python with Gmsh Module?

Generated from [Bomberbot](https://www.bomberbot.com/python/generating-complex-3d-meshes-in-python-with-gmsh-a-comprehensive-guide/)

**Last Updated:** 23 Nov, 2022

In this article, we will cover how to Generate meshes using the Gmsh module in Python.

## What is Mesh?

A connected 2D, 3D, or multi-dimension structure that is made up of points, lines, and curves is called a mesh. In real-world meshes are made up of many different materials such as metals, fibers, and ductile materials.

## Gmsh Module Functions

The Gmsh module provides several functions to define and generate mesh elements:

| Method | Description |
| :--- | :--- |
| `initialize()` | Initialize the gmsh API. |
| `add_point(x, y, z, lc)` | Create a point at (x, y, z) with the target mesh size (lc). |
| `add_line(pointA, pointB)` | Create a line from pointA to pointB. |
| `add_curve_loop(list of lines)` | Create a face that is formed by lines (a closed loop). |
| `add_plane_surface(list of faces)` | Create a surface on the faces and connect them. |
| `synchronize()` | Create the relevant Gmsh data structures from the Gmsh model. |
| `generate()` | Generate the mesh. |
| `write(model_name)` | Create a mesh of given model name (e.g., "GFG.msh"). |
| `run()` | Creates the graphical user interface. |
| `finalize()` | Finalizes the Gmsh API. |

After understanding mesh and functions, let’s jump right in.

## Module Required

To use the Gmsh module in Python, you need the following libraries installed:

```bash
pip install gmsh
pip install sys
```

---

## Step 1: Import modules, initialize gmsh

This step sets up the environment and initializes the Gmsh API.

```python
# Import modules:
import gmsh
import sys

# Initialize gmsh:
gmsh.initialize()
```

## Step 2: Create Cube Points

We start by defining the coordinates for the 8 points of the cube.

```python
# Import modules:
import gmsh
import sys

# Initialize gmsh:
gmsh.initialize()

# Cube points (with target mesh size lc = 1e-2):
lc = 1e-2
point1 = gmsh.model.geo.add_point(0, 0, 0, lc)
point2 = gmsh.model.geo.add_point(1, 0, 0, lc)
point3 = gmsh.model.geo.add_point(1, 1, 0, lc)
point4 = gmsh.model.geo.add_point(0, 1, 0, lc)
point5 = gmsh.model.geo.add_point(0, 1, 1, lc)
point6 = gmsh.model.geo.add_point(0, 0, 1, lc)
point7 = gmsh.model.geo.add_point(1, 0, 1, lc)
point8 = gmsh.model.geo.add_point(1, 1, 1, lc)

# Create the relevant Gmsh data structures from Gmsh model.
gmsh.model.geo.synchronize()

# Generate mesh:
gmsh.model.mesh.generate()

# Write mesh data:
gmsh.write("GFG.msh")

# Creates graphical user interface
if 'close' not in sys.argv:
    gmsh.fltk.run()

# It finalize the Gmsh API
gmsh.finalize()
```

## Step 3: Create Lines (Edges)

Next, we create the 12 edges of the cube by connecting the points using the `add_line()` method.

```python
# Import modules:
import gmsh
import sys

# Initialize gmsh:
gmsh.initialize()

# Cube points (redefined):
lc = 1e-2
point1 = gmsh.model.geo.add_point(0, 0, 0, lc)
point2 = gmsh.model.geo.add_point(1, 0, 0, lc)
point3 = gmsh.model.geo.add_point(1, 1, 0, lc)
point4 = gmsh.model.geo.add_point(0, 1, 0, lc)
point5 = gmsh.model.geo.add_point(0, 1, 1, lc)
point6 = gmsh.model.geo.add_point(0, 0, 1, lc)
point7 = gmsh.model.geo.add_point(1, 0, 1, lc)
point8 = gmsh.model.geo.add_point(1, 1, 1, lc)

# Edges of the cube:
line1 = gmsh.model.geo.add_line(point1, point2)
line2 = gmsh.model.geo.add_line(point2, point3)
line3 = gmsh.model.geo.add_line(point3, point4)
line4 = gmsh.model.geo.add_line(point4, point1)
line5 = gmsh.model.geo.add_line(point5, point6)
line6 = gmsh.model.geo.add_line(point6, point7)
line7 = gmsh.model.geo.add_line(point7, point8)
line8 = gmsh.model.geo.add_line(point8, point5)
line9 = gmsh.model.geo.add_line(point4, point5)
line10 = gmsh.model.geo.add_line(point6, point1)
line11 = gmsh.model.geo.add_line(point7, point2)
line12 = gmsh.model.geo.add_line(point3, point8)

# Create the relevant Gmsh data structures from Gmsh model.
gmsh.model.geo.synchronize()

# Generate mesh:
gmsh.model.mesh.generate()

# Write mesh data:
gmsh.write("GFG.msh")

# Creates graphical user interface
if 'close' not in sys.argv:
    gmsh.fltk.run()

# It finalize the Gmsh API
gmsh.finalize()
```

## Step 4: Create Faces and Surfaces

To create solid faces, we use `add_curve_loop()` to define the boundary (the loop of lines) and then `add_plane_surface()` to define the actual surface.

*   **`add_curve_loop([line1, line2, line3, line4])`**: Requires a list of lines in a closed loop format. It connects the start point of the first line to the end point of the last line, forming a face.
*   **`add_plane_surface([face])`**: Creates a surface based on the defined face. If multiple faces are passed, it attempts to connect them if they lie in the same plane.

```python
# Import modules:
import gmsh
import sys

# Initialize gmsh:
gmsh.initialize()

# Cube points and lines (as defined in previous steps)...
lc = 1e-2
point1 = gmsh.model.geo.add_point(0, 0, 0, lc)
# ... (lines 1 through 12 created here) ...
# (For brevity, assume all points and lines are defined)

# Edges of cube:
line1 = gmsh.model.geo.add_line(point1, point2)
# ... (lines 2 through 12 created here) ...

# Faces of the cube (defined by curve loops):
face1 = gmsh.model.geo.add_curve_loop([line1, line2, line3, line4]) # Bottom face
face2 = gmsh.model.geo.add_curve_loop([line5, line6, line7, line8]) # Top face
face3 = gmsh.model.geo.add_curve_loop([line9, line5, line10, -line4]) # Front face
face4 = gmsh.model.geo.add_curve_loop([line9, -line8, -line12, line3]) # Back face
face5 = gmsh.model.geo.add_curve_loop([line6, line11, -line1, -line10]) # Left face
face6 = gmsh.model.geo.add_curve_loop([line11, line2, line12, -line7]) # Right face

# Surfaces of the cube (creating the actual faces):
gmsh.model.geo.add_plane_surface([face1])
gmsh.model.geo.add_plane_surface([face2])
gmsh.model.geo.add_plane_surface([face3])
gmsh.model.geo.add_plane_surface([face4])
gmsh.model.geo.add_plane_surface([face5])
gmsh.model.geo.add_plane_surface([face6])

# Create the relevant Gmsh data structures from Gmsh model.
gmsh.model.geo.synchronize()

# Generate mesh:
gmsh.model.mesh.generate()

# Write mesh data:
gmsh.write("GFG.msh")

# Creates graphical user interface
if 'close' not in sys.argv:
    gmsh.fltk.run()

# It finalize the Gmsh API
gmsh.finalize()
```

## Step 5: Create Pentagons and Connect Them

In the final step, we introduce two pentagons and connect them to the cube faces.

1.  Define points and lines for the two pentagons.
2.  Define the faces of the pentagons using `add_curve_loop()`.
3.  Use `add_plane_surface()` to connect the pentagon faces with the cube faces and with each other.

```python
# Import modules:
import gmsh
import sys

# Initialize gmsh:
gmsh.initialize()

# --- Cube Setup (Points and Lines) ---
lc = 1e-2
point1 = gmsh.model.geo.add_point(0, 0, 0, lc)
# ... (All 8 cube points and 12 cube lines defined here) ...
# (See Step 3 for the full definitions)

# --- Bigger Pentagon Setup ---
# Points of bigger pentagon (example coordinates):
point9 = gmsh.model.geo.add_point(0.3, 0.3, -2, lc)
point10 = gmsh.model.geo.add_point(0.7, 0.3, -2, lc)
point11 = gmsh.model.geo.add_point(0.7, 0.5, -2, lc)
point12 = gmsh.model.geo.add_point(0.5, 0.7, -2, lc)
point13 = gmsh.model.geo.add_point(0.3, 0.5, -2, lc)

# Lines of bigger pentagon:
line13 = gmsh.model.geo.add_line(point9, point10)
line14 = gmsh.model.geo.add_line(point10, point11)
line15 = gmsh.model.geo.add_line(point11, point12)
line16 = gmsh.model.geo.add_line(point12, point13)
line17 = gmsh.model.geo.add_line(point13, point9)

# --- Smaller Pentagon Setup ---
# Points of smaller pentagon (example coordinates):
point14 = gmsh.model.geo.add_point(0.4, 0.4, 2, lc)
point15 = gmsh.model.geo.add_point(0.6, 0.4, 2, lc)
point16 = gmsh.model.geo.add_point(0.6, 0.5, 2, lc)
point17 = gmsh.model.geo.add_point(0.5, 0.6, 2, lc)
point18 = gmsh.model.geo.add_point(0.4, 0.5, 2, lc)

# Lines of smaller pentagon:
line18 = gmsh.model.geo.add_line(point14, point15)
line19 = gmsh.model.geo.add_line(point15, point16)
line20 = gmsh.model.geo.add_line(point16, point17)
line21 = gmsh.model.geo.add_line(point17, point18)
line22 = gmsh.model.geo.add_line(point18, point14)

# --- Face Definitions ---
# Face of bigger pentagon:
face7 = gmsh.model.geo.add_curve_loop([line13, line14, line15, line16, line17])

# Face of smaller pentagon:
face8 = gmsh.model.geo.add_curve_loop([line18, line19, line20, line21, line22])

# --- Connections ---
# Connect bigger pentagon face with cube faces (e.g., face1)
gmsh.model.geo.add_plane_surface([face1, face7])
gmsh.model.geo.add_plane_surface([face2, face8])
gmsh.model.geo.add_plane_surface([face7, face8])

# Create the relevant Gmsh data structures from Gmsh model.
gmsh.model.geo.synchronize()

# Generate mesh:
gmsh.model.mesh.generate()

# Write mesh data:
gmsh.write("GFG.msh")

# Creates graphical user interface
if 'close' not in sys.argv:
    gmsh.fltk.run()

# It finalize the Gmsh API
gmsh.finalize()
```
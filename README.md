# MyCFD

An investigation into the PISO algorithm for solving the incompressible Navier-Stokes equations, by Jean Carlos Matter Thomasio.

This is a tutorial implementation meant for learning the basic concepts of Computational Fluid Dynamics. The code was written to be legible and easy to follow, for clarity over performance.

![Flow evolution over a NACA 0012 airfoil](figs/flow_evolution.gif)

## What it does

Solves the 2D incompressible viscous Navier-Stokes equations with the Finite Volume Method, using the PISO algorithm for the pressure-velocity coupling. 

This is the same approach used by the `icoFoam` solver from OpenFOAM. 

Works on unstructured meshes and can handle both simple cases like the lid-driven cavity and external flow over an airfoil.

## Files

- `FiniteVolumes.ipynb` — Contains the full solver, from the mesh handling to the PISO loop, with the theory explained along the way.
- `FiniteDiferences.ipynb` — Earlier version of the solver using the Finite Difference Method on a structured grid.
- `mesh/` — Geometry (`.geo`) and mesh files, including the NACA 0012 airfoil.

## How it works

The notebook follows the usual steps of a finite volume solver, one per section:

1. **Mesh** — generate a structured mesh or import a `.geo`/`.msh` file with gmsh. The geometry is stored as a list of cells and faces.
2. **Boundary conditions** — each patch is defined per field as either a fixed value (Dirichlet) or a zero gradient (Neumann).
3. **Discretization** — assemble the matrices for the time derivative, convection, diffusion and pressure terms.
4. **PISO loop** — solve the momentum equations, then correct the pressure and velocity until the fields converge, and advance in time.
5. **Results** — plot the pressure and velocity fields, the surface pressure coefficient (Cp), and the evolution of the flow.

## Running it

Open `FiniteVolumes.ipynb` and run the cells from top to bottom. The configuration (Reynolds number, mesh, boundary conditions, advection scheme and under-relaxation) is all set in the first cells.

You will need `numpy`, `scipy`, `matplotlib` and `gmsh`.

## Notes

- This is a laminar solver, so it is meant for low Reynolds number cases.
- The airfoil mesh is kept intentionally simple and does not represent good meshing practice.
- The goal is clarity, not speed: the operators are written as plain loops over the faces so they stay easy to read.

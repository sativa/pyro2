![pyro logo]
(https://raw.githubusercontent.com/zingale/pyro2/master/www/pyro.png)

*A simple python-based tutorial on computational methods for hydrodynamics*


pyro is a computational hydrodynamics code that presents
two-dimensional solvers for advection, compressible hydrodynamics,
diffusion, incompressible hydrodynamics, and multigrid, all in a
finite-volume framework.  The code is mainly written in python and is
designed with simplicity in mind.  The algorithms are written to
encourage experimentation and allow for self-learning of these code
methods.

The latest version of pyro is always available at:

https://github.com/zingale/pyro2

The project webpage, where you'll find documentation, plots, notes,
etc. is here:

http://bender.astro.sunysb.edu/hydro_by_example/


## Getting Started

  - There are a few steps to take to get things running. You need to
     make sure you have numpy, f2py, and matplotlib installed. On a
     Fedora system, this can be accomplished by doing:

       `yum install numpy numpy-f2py python-matplotlib python-matplotlib-tk`

  - You also need to make sure gfortran is present on you system. On
     a Fedora system, it can be installed as: 

       `yum install gcc-gfortran` 

  - Not all matplotlib backends allow for the interactive plotting as
     pyro is run. One that does is the TkAgg backend. This can be made
     the default by creating a file `~/.matplotlib/matplotlibrc` with
     the content:

       `backend: TkAgg`

     You can check what backend is your current default in python via: 

       ```python
       import matplotlib.pyplot 
       print matplotlib.pyplot.get_backend() 
       ```

  - The remaining steps are: 

      * Set the `PYTHONPATH` environment variable to point to the `pyro2/`
        directory.

      * Build the Fortran source. In `pyro2/` type 

          `./mk.sh` 

      * Run a quick test of the advection solver: 

          `./pyro.py advection smooth inputs.smooth` 

        you should see a graphing window pop up with a smooth pulse
        advecting diagonally through the periodic domain.


## Solvers

pyro provides the following solvers (all in 2-d):

  - `advection`: a second-order unsplit linear advection solver.  This
    is the basic method to understand hydrodynamics.

  - `compressible`: a second-order unsplit solver for the Euler
    equations of compressible hydrodynamics.  This uses a 2-shock
    approximate Riemann solver.

  - `incompressible`: a second-order cell-centered approximate
    projection method for the incompressible equations of
    hydrodynamics.

  - `diffusion`: a Crank-Nicolson time-discretized solver for the
    constant-coefficient diffusion equation.

  - `multigrid`: a cell-centered multigrid solver for a
    constant-coefficient Helmholtz equation, as well as a
    variable-coefficient Poisson equation (which inherits from the
    constant-coefficient solver).

  - `lm_atm`: (mostly complete) a solver for the equations of 
    low Mach number hydrodynamics for atmospheric flows.

  - `lm_combustion`: (in development) a solver for the equations of
    low Mach number hydrodynamics for smallscale combustion.


## Working With Data

In addition to the main pyro program, there are many analysis tools
that we describe here. Note: some problems write a report at the end
of the simulation specifying the analysis routines that can be used
with their data.

  - `compare.py`: this takes two simulation output files as input and
    compares zone-by-zone for exact agreement. This is used as part of
    the regression testing.

      usage: `./compare.py file1 file2`

  - `plot.py`: this takes the solver name and an output file as input
    and plots the data using the solver's dovis method.

      usage: `./plot.py solvername file`

  - `analysis/`

      * `gauss_diffusion_compare.py`: this is for the diffusion solver's
        Gaussian diffusion problem. It takes a sequence of output
        files as arguments, computes the angle-average, and the plots
        the resulting points over the analytic solution for comparison
        with the exact result.

          usage: `./gauss_diffusion_compare.py file*`

      * `incomp_converge_error.py`: this is for the incompressible
        solver's converge problem. This takes a single output file as
        input and compares the velocity field to the analytic
        solution, reporting the L2 norm of the error.

          usage: `./incomp_converge_error.py file`

      * `plotvar.py`: this takes a single output file and a variable
        name and plots the data for that variable.

          usage: `./plotvar.py file variable`

      * `sedov_compare.py`: this takes an output file from the
        compressible Sedov problem, computes the angle-average profile
        of the solution and plots it together with the analytic data
        (read in from `cylindrical-sedov.out`).

          usage: `./sedov_compare.py file`

      * `smooth_error.py`: this takes an output file from the advection
        solver's smooth problem and compares to the analytic solution,
        outputting the L2 norm of the error.

          usage: `./smooth_error.py file`

      * `sod_compare.py`: this takes an output file from the
        compressible Sod problem and plots a slice through the domain
        over the analytic solution (read in from `sod-exact.out`).

          usage: `./sod_compare.py file`


## Understanding the algorithms

  There is a set of notes that describe the background and details of the
  algorithms that pyro implements:

  http://bender.astro.sunysb.edu/hydro_by_example/CompHydroTutorial.pdf

  The source for these notes is also available on github:

  https://github.com/zingale/numerical_exercises


## Getting Help

  Join the mailing list to say up-to-date:

  http://bender.astro.sunysb.edu/mailman/listinfo/pyro-help


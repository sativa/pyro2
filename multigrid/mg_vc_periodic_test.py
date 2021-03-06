#!/usr/bin/env python

"""
Test the variable-coefficient MG solver with periodic data.

Here we solve:

   div . ( alpha grad phi ) = f

with

   alpha = 2.0 + cos(2.0*pi*x)*cos(2.0*pi*y)

   f = -16.0*pi**2*(cos(2*pi*x)*cos(2*pi*y) + 1)*sin(2*pi*x)*sin(2*pi*y)

This has the exact solution:

   phi = sin(2.0*pi*x)*sin(2.0*pi*y)

on [0,1] x [0,1]

We use Dirichlet BCs on phi.  For alpha, we do not have to impose the
same BCs, since that may represent a different physical quantity.
Here we take alpha to have Neumann BCs.  (Dirichlet BCs for alpha will
force it to 0 on the boundary, which is not correct here)

"""

from __future__ import print_function

import numpy as np
import mesh.patch as patch
import variable_coeff_MG as MG
import matplotlib.pyplot as plt

pi = np.pi
sin = np.sin
cos = np.cos
exp = np.exp

# the analytic solution
def true(x,y):
    return sin(2.0*pi*x)*sin(2.0*pi*y)


# the coefficients
def alpha(x,y):
    return 2.0 + cos(2.0*pi*x)*cos(2.0*pi*y)


# the L2 error norm
def error(myg, r):

    # L2 norm of elements in r, multiplied by dx to
    # normalize
    return np.sqrt(myg.dx*myg.dy*np.sum((r[myg.ilo:myg.ihi+1,
                                                 myg.jlo:myg.jhi+1]**2).flat))


# the righthand side
def f(x,y):
    return -16.0*pi**2*(cos(2*pi*x)*cos(2*pi*y) + 1)*sin(2*pi*x)*sin(2*pi*y)



N = [16, 32, 64, 128, 256, 512]
err = []

for nx in N:

    # test the multigrid solver
    ny = nx


    # create the coefficient variable
    g = patch.Grid2d(nx, ny, ng=1)
    d = patch.CellCenterData2d(g)
    bc_c = patch.BCObject(xlb="periodic", xrb="periodic",
                          ylb="periodic", yrb="periodic")
    d.register_var("c", bc_c)
    d.create()

    c = d.get_var("c")
    c[:,:] = alpha(g.x2d, g.y2d)

    # check whether the RHS sums to zero (necessary for periodic data)
    rhs = f(g.x2d, g.y2d)
    print("rhs sum: {}".format(np.sum(rhs[g.ilo:g.ihi+1,g.jlo:g.jhi+1])))


    # create the multigrid object
    a = MG.VarCoeffCCMG2d(nx, ny,
                          xl_BC_type="periodic", yl_BC_type="periodic",
                          xr_BC_type="periodic", yr_BC_type="periodic",
                          nsmooth=10,
                          nsmooth_bottom=50,
                          coeffs=c, coeffs_bc=bc_c,
                          verbose=1, vis=0, true_function=true)

    # initialize the solution to 0
    a.init_zeros()

    # initialize the RHS using the function f
    rhs = f(a.x2d, a.y2d)
    a.init_RHS(rhs)

    # solve to a relative tolerance of 1.e-11
    a.solve(rtol=1.e-11)

    # alternately, we can just use smoothing by uncommenting the following
    #a.smooth(a.nlevels-1,10000)

    # get the solution
    v = a.get_solution()

    # get the true solution
    b = true(a.x2d,a.y2d)

    # compute the error from the analytic solution -- note that with
    # periodic BCs all around, there is nothing to normalize the
    # solution.  We subtract off the average of phi from the MG
    # solution (we do the same for the true solution to put them on
    # the same footing)
    e = v - np.sum(v)/(nx*ny) - (b - np.sum(b)/(nx*ny))

    enorm = error(a.soln_grid, e)
    print(" L2 error from true solution = %g\n rel. err from previous cycle = %g\n num. cycles = %d" % \
          (enorm, a.relative_error, a.num_cycles))

    err.append(enorm)


#---------------------------------------------------------------------------
# plot the solution
plt.clf()

plt.figure(figsize=(10.0,4.0), dpi=100, facecolor='w')


plt.subplot(121)

plt.imshow(np.transpose(v[a.ilo:a.ihi+1,a.jlo:a.jhi+1]),
          interpolation="nearest", origin="lower",
          extent=[a.xmin, a.xmax, a.ymin, a.ymax])

plt.xlabel("x")
plt.ylabel("y")

plt.title("nx = {}".format(nx))

plt.colorbar()


plt.subplot(122)

plt.imshow(np.transpose(e[a.ilo:a.ihi+1,a.jlo:a.jhi+1]),
          interpolation="nearest", origin="lower",
          extent=[a.xmin, a.xmax, a.ymin, a.ymax])

plt.xlabel("x")
plt.ylabel("y")

plt.title("error")

plt.colorbar()

plt.tight_layout()

plt.savefig("mg_vc_periodic_test.png")
plt.savefig("mg_vc_periodic_test.eps", bbox_inches="tight")


#---------------------------------------------------------------------------
# plot the convergence

N = np.array(N, dtype=np.float64)
err = np.array(err)

print(N)
print(err)

plt.clf()
plt.loglog(N, err, "x", color="r")
plt.loglog(N, err[0]*(N[0]/N)**2, "--", color="k")


plt.xlabel("N")
plt.ylabel("error")

f = plt.gcf()
f.set_size_inches(7.0,6.0)

plt.tight_layout()

plt.savefig("mg_vc_converge.png")
plt.savefig("mg_vc_converge.eps", bbox_inches="tight")

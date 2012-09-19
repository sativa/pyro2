from util import runparams

def pres(dens, eint):
    """ given the density and the specific internal energy, return the
        pressure """

    gamma = runparams.getParam("eos.gamma")

    p = dens*eint*(gamma - 1.0)

    return p



def dens(pres, eint):
    """ given the pressure and the specific internal energy, return
        the density """

    gamma = runparams.getParam("eos.gamma")

    dens = p/(eint*(gamma - 1.0))

    return dens



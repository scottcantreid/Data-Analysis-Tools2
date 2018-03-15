import numpy as np

def resistivity(v, i, bridge):
    #Returns resistivity in micro Ohm m
    return v/i/bridge

def conductivity(v, i, bridge):
    return 1 / resistivity(v,i,bridge)

def E_field(io, i, v, l):
#length given in micron, returns efield in V/cm
#bridge is l/(w*z)
    l = l * 1e-4
    ef = np.zeros(len(io))
    r = v/i
    di = io[1] - io[0]
    for j in np.arange(1, len(io)):
        ef[j] = ef[j-1] + di*r[j]
    if(len(ef[io == 0]) == 1):
        ef = ef - ef[io == 0]
    else:
        ef = ef + io[0] * r[0]
    return ef/l

def interpolate(xo, x, y):
    j = np.argmin(np.fabs(x - xo))
    jm = max(0, j-4)
    jp = min(len(x)-1, j + 4)
    po = np.polyfit(x[jm:jp], y[jm:jp], 1)
    return po[1] + po[0]*xo

def extraconductivity(to, tc, sigo, sigc):
    sigcdw = np.ndarray(len(to))
    for i in range(len(to)):
        sigcdw[i] = interpolate(to[i], tc, sigc) - sigo[i]
    return sigcdw

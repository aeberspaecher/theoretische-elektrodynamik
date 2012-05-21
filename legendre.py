from sympy import *
from scipy.integrate import quad
from scipy.special import legendre as legScipy
import itertools
import matplotlib.pyplot as plt
import numpy as np

def legAnalytical(f, var, n, verbose=False):
    """Expand function f(var) as a Legendre series of order n.

    Use Sympy for anayltical calculations.
    """

    ret = 0 # TODO: do this more elegantly?

    for i in range(n+1):
        coeff = Rational(2*i+1, 2)*integrate(f(var)*legendre(i, var), (var, -1 , +1))
        contrib = coeff*legendre(i, var)
        ret = ret + contrib
        if(verbose):
            print("Contribution from i=%s: %s"%(i, contrib))

    return ret

def legNumerical(f, n):
    """Numerically compute the Legendre expansion of a function f.

    Return a NumPy polynomial.
    """

    ret = np.poly1d(np.array([0]))

    for i in range(n+1):
        leg = legScipy(i)
        coeff, coefferr = quad(lambda x: f(x)*leg(x), -1, +1)
        coeff *= (2.0*i+1.0)/2.0
        ret += coeff*legScipy(i)

    return ret

def plotLegendreExpansion(f, n):
    """Plot function and its Legendre expansion.
    """

    # create cycling linestyles and colors:
    linestyles = itertools.cycle(["-", "--"])
    colors = itertools.cycle(["blue", "red", "#014421", "#FF00FF", "gray"])

    numSamples = 2001

    # plot function
    xVals = np.linspace(-1, +1, numSamples)
    yVals = f(xVals)
    plt.plot(xVals, yVals, ls="-", c="black", lw=2, label="Function")

    # plot expansions in a loop
    for i in range(2, order+1):
        expansion = legNumerical(f, i)
        yVals = expansion(xVals)
        plt.plot(xVals, yVals, linestyles.next(), lw=2, label="Order %s"%i)

    plt.legend()
    #plt.savefig("LegendreExpansion.png")
    plt.show()


if(__name__ == '__main__'):

    x = Symbol("x")

    # define function:
    f = tanh(10*x) # Piecewise((-x, x<0), (x, x>=0)) # note: Piecewise does not work in the plotting routine!

    # create a function that can takes arrays as argument with NumPy functions
    fCallable = lambdify(x, f, modules="numpy")

    # define order of expansion:
    order = 5

    # compute the Legendre expansion analytically
    # then, plot expansion of various orders (these are computed numerically)
    pretty_print("Legendre expansion (order %s) of %s in [-1; +1]:\n%s"
                 %(order, f, legAnalytical(f, x, order))) # comment this out in case the script hangs
    plotLegendreExpansion(fCallable, order)


# Series for Abs(x):
# n=3: 15*x**2/16 + 3/16
# n=5: -105*x**4/128 + 105*x**2/64 + 15/128
# n=7: 3003*x**6/2048 - 5775*x**4/2048 + 4725*x**2/2048 + 175/2048
# n=9: -109395*x**8/32768 + 63063*x**6/8192 - 105105*x**4/16384 + 24255*x**2/8192 + 2205/32768
# n=11: 2263261*x**10/262144 - 6235515*x**8/262144 + 3216213*x**6/131072 - 1576575*x**4/131072 + 945945*x**2/262144 + 14553/262144

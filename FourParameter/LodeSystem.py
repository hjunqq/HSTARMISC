#!/usr/bin/env python

# Do a check for python version and print a helpful message
import sys

if sys.version_info < (2, 6):
    sys.exit("Upgrade python to at lest version 2.6")

# If the numpy module is not present, print a helpful message
try:
    import numpy as np
except:
    sys.exit("Could not find required module 'numpy.\n"
             "See numpy.scipy.org for more information.")

import math


#
# Helper functions for uniform printing throughout the script.
#

def headerprint(string):
    """ Prints a centered string to divide output sections. """
    mywidth = 64
    mychar = "="
    numspaces = mywidth - len(string)
    before = int(math.ceil(float(mywidth - len(string)) / 2))
    after = int(math.floor(float(mywidth - len(string)) / 2))
    print("\n" + before * mychar + string + after * mychar + "\n")


def valprint(string, value):
    """ Ensure uniform formatting of scalar value outputs. """
    print("{0:>30}: {1: .10e}".format(string, value))


def matprint(string, value):
    """ Ensure uniform formatting of matrix value outputs. """
    print("{0}:".format(string))
    print(value)


def usage():
    """ When the user needs help, print the script usage. """
    headerprint(" Analyze Stress State ")
    s = "      > ./script sig11 sig22 sig33 sig12 sig13 sig23\n"
    sys.exit(s)


if __name__ == '__main__':
    if (len(sys.argv) != 4 and len(sys.argv) != 7) or \
            ("--help" in sys.argv or "-h" in sys.argv):
        usage()
    dum = np.zeros(9)

    for idx in range(1, len(sys.argv)):
        try:
            dum[idx - 1] = float(sys.argv[idx])
        except:
            sys.exit("Argument '{0}' is not a valid float". \
                     format(sys.argv[idx]))

    epsilon = dum.reshape((3, 3))
    epsilon_iso = 1.0 / 3.0 * np.trace(epsilon) * np.eye(3)
    epsilon_dev = epsilon - epsilon_iso

    # Compute principal stresses
    eigvals = list(np.linalg.eigvalsh(epsilon))
    eigvals.sort()
    eigvals.reverse()

    maxsheer = (max(eigvals) - min(eigvals)) / 2.0

    I1 = np.trace(epsilon)
    J2 = 1.0 / 2.0 * np.trace(np.dot(epsilon_dev, epsilon_iso))
    J3 = 1.0 / 3.0 * np.trace( \
        np.dot(epsilon_dev, np.dot(epsilon_dev, epsilon_dev)))

    mean_strain = 1.0 / 3.0 * I1
    lode_r = math.sqrt(2.0 * J2)
    lode_z = I1 / math.sqrt(3.0)

    dum = 3.0 * math.sqrt(6.0) * np.linalg.det(epsilon_dev / lode_r)
    lode_theta = 1.0 / 3.0 * math.asin(dum)

    headerprint(" Strain State Anslysis ")
    matprint(" Input Strain ", epsilon)
    headerprint(" Component Matricies ")
    matprint(" Isotropic Strain ", epsilon_iso)
    matprint(" Deviatoric Strain ", epsilon_dev)
    headerprint(" Scalar Values ")
    valprint(" P1 ", eigvals[0])
    valprint(" P2 ", eigvals[1])
    valprint(" P3 ", eigvals[2])
    valprint(" Max Shear ", maxsheer)
    valprint("Lode z", lode_z)
    valprint("Lode r", lode_r)
    valprint("Lode theta (rad)", lode_theta)
    valprint("Lode theta (deg)", math.degrees(lode_theta))
    headerprint(" End Output ")

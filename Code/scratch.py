import numpy as np
from prob_gen_helper_funcs import *

def nPolyBowl_cond(n, p, k):
    n_plus_epsilon = n + 10**(-p)
    epsilon = n_plus_epsilon - n
    if epsilon == 0:
      print("epsilon cannot be represented for RHS=npe, n=%d, p=%d, k=%d" % (n, p, k))
    else:
        A = np.ones((n, n))
        A = A + np.eye(n)*epsilon

        for i in range(2,k+1):
            Atmp = np.ones((n, n))
            Atmp = Atmp + np.eye(n)*i*epsilon

            A = np.vstack((A, Atmp))

    tmp = np.zeros((n, n*(k-1)))
    tmp = np.vstack((tmp, np.eye(n*(k-1))))
    A = np.hstack((A, tmp))
    # Calculate the condition numer
    print(np.linalg.cond(A, p=1))

nPolyBowl_cond(n=3, p=3, k=3)

# N = [3, 5, 10, 100, 500, 1000, 2000, 4000]
# P = [8, 9, 10, 11, 12, 13, 14, 15, 16]
# K = [2, 4, 6, 8]
#
# for n in N:
#   for p in P:
#     for k in K:
#       nPolyBowl(n, p, k, "npe", "../Problem_Files/")
#
# for n in N:
#   for p in P:
#     for k in K:
#       nPolyBowl(n, p, k, "1pe", "../Problem_Files/")
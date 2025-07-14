import numpy as np
from prob_gen_helper_funcs import *

def nPolyBowl(n, p, k, RHS, folder):
  if RHS == "npe":
    # This problem is of the form [(1 1^T) + diag(epsilon)][x] <= [1 (n+epsilon)]
    # The RHS of n+epsilon is the limiting factor on the written data
    n_plus_epsilon = add_min_value(n, "sci", p)
    epsilon = n_plus_epsilon - n

    A = np.ones((n, n))
    A = A + np.eye(n)*epsilon

    b = np.ones((n, 1))
    b = b*(n+epsilon)

    for i in range(2,k+1):
      Atmp = np.ones((n, n))
      Atmp = Atmp + np.eye(n)*i*epsilon

      tmp = n + i*epsilon + tri_num(i-1)*epsilon
      btmp = np.ones((n,1))*tmp

      A = np.vstack((A, Atmp))
      b = np.vstack((b, btmp))

    c = -np.ones((n,1))
    write_mpsV2(A, b, c, 53, folder+"nPolyBowl_npe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
    # Digits available in the 25 character limit MPS filetype
    # {sign} + {ones digit} + {decimal point} + {18 digits after decimal} + {e} + {sign} + {2 digit exponent}
    # = 1 + 1 + 1 + 18 + 1 + 1 + 2 = 25
  elif RHS == "1pe":
    # This problem is of the form [(1 1^T) + diag(epsilon)][x] <= [1 (1+epsilon)]
    # The value 1+epsilon is the limiting factor on the written data
    # However, the final solution is (1+epsilon)/(n+epsilon) will become very small
    one_plus_epsilon = add_min_value(1, "sci", p)
    epsilon = one_plus_epsilon - 1

    A = np.ones((n, n))
    A = A + np.eye(n) * epsilon

    b = np.ones((n, 1)) * (1 + epsilon)

    for i in range(2, k+1):
      Atmp = np.ones((n, n))
      Atmp = Atmp + np.eye(n) * i * epsilon

      tmp = 1 + (tri_num(i-1)+1) * epsilon
      btmp = np.ones((n, 1)) * tmp

      A = np.vstack((A, Atmp))
      b = np.vstack((b, btmp))

    c = -np.ones((n, 1))
    write_mpsV2(A, b, c, 53, folder + "nPolyBowl_1pe_" + str(n) + "_" + str(p) + "_" + str(k) + ".mps")


# nPolyBowl(n=32, p=1, k=2, folder="../Problem_Files/")

N = [15000]
P = [14, 15]
K = [2]

for n in N:
  for p in P:
    for k in K:
      nPolyBowl(n, p, k, "1pe", "../Problem_Files/")
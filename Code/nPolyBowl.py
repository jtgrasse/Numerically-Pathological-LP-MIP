import numpy as np
from prob_gen_helper_funcs import *

def nPolyBowl(n, p, k, folder):
  n_plus_epsilon = add_min_value(n, "sci", p)
  epsilon = n_plus_epsilon - n

  A = np.ones((n, n))
  A = A + np.eye(n)*epsilon

  b = np.ones((n, 1))
  b = b*(n+epsilon)

  for i in range(2,k):
    Atmp = np.ones((n, n))
    Atmp = Atmp + np.eye(n)*i*epsilon

    tmp = n + i*epsilon + tri_num(i-1)*epsilon
    btmp = np.ones((n, 1))
    btmp = np.ones((n,1))*tmp

    A = np.vstack((A, Atmp))
    b = np.vstack((b, btmp))

  c = -np.ones((n,1))
  write_mps(A, b, c, 51, folder+"nPolyBowl_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  # Digits available in the 25 character limit MPS filetype
  # {sign} + {ones digit} + {decimal point} + {18 digits after decimal} + {e} + {sign} + {2 digit exponent}
  # = 1 + 1 + 1 + 18 + 1 + 1 + 2 = 25

# nPolyBowl(n=32, p=1, k=2, folder="../Problem_Files/")

N = [8, 16]
P = [11, 8, 4]
K = [2, 3, 4]

for n in N:
  for p in P:
    for k in K:
      nPolyBowl(n, p, k, "../Problem_Files/")
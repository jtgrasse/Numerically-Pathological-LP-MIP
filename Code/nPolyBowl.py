import numpy as np
from fractions import Fraction

from helper_funcs import *

def nPolyBowl(type, RHS, n, p, k):
  '''
  Generates a nPolyBowl using arbitrary precision rationals via Python's Fraction class.
  Stores all coefficients as Fraction objects for exact arithmetic.
  
  Parameters:
  type: "rational" or "double"
  RHS: "npe" or "1pe"
  n: number of variables
  p: the exponent of epsilon, where epsilon = 2^(-p)
  k: number of blocks of constraints
  '''
  #First check if epsilon can be represented in double precision
  if type == "double":
    if RHS == "npe":
      n_plus_epsilon = n + 2**(-p)
      if n_plus_epsilon == n:
        raise ValueError("epsilon cannot be represented for RHS=npe, n=%d, p=%d, k=%d" % (n, p, k))
    elif RHS == "1pe":
      one_plus_epsilon = 1 + 2**(-p)
      if one_plus_epsilon == 1:
        raise ValueError("epsilon cannot be represented for RHS=1pe, n=%d, p=%d, k=%d" % (n, p, k))
  epsilon = Fraction(1, 2**p)
  
  # A is a matrix of 1s with the diagonal having epsilon added to it.
  # A[i,i] = 1 + epsilon
  A = [[Fraction(1) for _ in range(n)] for _ in range(n)]
  for d in range(n):
    A[d][d] = Fraction(1) + epsilon
  
  for i in range(2, k+1):
    # Atmp is a matrix of 1s with the diagonal having i*epsilon added to it.
    # Atmp[d,d] = 1 + i*epsilon
    Atmp = [[Fraction(1) for _ in range(n)] for _ in range(n)]
    for d in range(n):
      Atmp[d][d] = Fraction(1) + i * epsilon
    
    A.extend(Atmp)

  # # We have the main A, now add the identity to the right of A for the slack variables.
  # A = [row + [Fraction(1) if i == j else Fraction(0) for j in range(len(A))] for i, row in enumerate(A)]

  # c is objective vector of n -1s (associated with x vairables) and kn 0s (associated with slack variables)
  c = [Fraction(-1) for _ in range(n)]
  # c.extend([Fraction(0) for _ in range(n*k)])

  # The RHS b is a vector of n+epsilon or 1+epsilon depending on the RHS parameter.
  if RHS == "npe":
    # b is a vector of n+epsilon
    b = [Fraction(n) + epsilon for _ in range(n)]
    for i in range(2, k+1):
      # b is a vector of n + i*epsilon + tri_num(i-1)*epsilon
      btmp = [Fraction(n) + (i + tri_num(i-1)) * epsilon for _ in range(n)]
      b.extend(btmp)

  elif RHS == "1pe":
    # b is a vector of 1+epsilon
    b = [Fraction(1) + epsilon for _ in range(n)]
    for i in range(2, k+1):
      # b is a vector of 1 + i*epsilon + tri_num(i-1)*epsilon
      btmp = [Fraction(1) + (i + tri_num(i-1)) * epsilon for _ in range(n)]
      b.extend(btmp)
    
  if type == "rational":
    return A, b, c
  elif type == "double":
    # Convert A, b, c to float
    A_float = np.array(A, dtype=float)
    b_float = np.array(b, dtype=float)
    c_float = np.array(c, dtype=float)
    return A_float, b_float, c_float

def generate_nPolyBowl_mps(type, RHS, n, p, k, folder):
  if type == "rational":
    A, b, c = nPolyBowl("rational", RHS, n, p, k)
    write_mps_rational(A, b, c, folder+"nPolyBowl_rational_"+RHS+"_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  elif type == "double":
    try:
      A, b, c = nPolyBowl("double", RHS, n, p, k)
      write_mps_double(A, b, c, folder+"nPolyBowl_double_"+RHS+"_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
    except ValueError as e:
      print(f"{e}")

if __name__ == "__main__":
  types = ["double"]
  RHSs = ["npe", "1pe"]
  N = [3, 10, 50, 100, 200, 250, 500, 750, 1000]
  P = [15, 20, 25, 30, 35, 40, 45, 50]
  K = [2, 4, 6, 8]

  print("Generating nPolyBowl_double problem instances...")
  for type in types:
    for RHS in RHSs:
      for n in N:
        for p in P:
          for k in K:
            generate_nPolyBowl_mps(type, RHS, n, p, k, "Problem_Files/")

  print("\nDone generating all problem instances!")
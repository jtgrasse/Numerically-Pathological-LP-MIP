import numpy as np
from fractions import Fraction

from Code.helper_funcs import *

def nPolyBowl_double(RHS, n, p, k):
  '''
  Generates a nPolyBowl using the following parameters:
  n: number of variables
  p: the exponent of epsilon, where epsilon = 2^(-p)
  k: number of blocks of constraints
  '''
  if RHS == "npe":
    # This problem is of the form [(1 1^T) + diag(epsilon)][x] <= [1 (n+epsilon)]
    # The RHS of n+epsilon is the limiting factor on the written data
    n_plus_epsilon = n + 2**(-p)
    epsilon = n_plus_epsilon - n
    if epsilon == 0:
      raise ValueError("epsilon cannot be represented for RHS=npe, n=%d, p=%d, k=%d" % (n, p, k))
    else:
      A = np.ones((n, n))
      A = A + np.eye(n)*epsilon

      b = np.ones((n, 1))
      b = b*(n+epsilon)

      for i in range(2,k+1):
        Atmp = np.ones((n, n))
        Atmp = Atmp + np.eye(n)*i*epsilon

        tmp = n + (i + tri_num(i-1))*epsilon
        btmp = np.ones((n,1))*tmp

        A = np.vstack((A, Atmp))
        b = np.vstack((b, btmp))

      c = -np.ones((n,1))
  elif RHS == "1pe":
    one_plus_epsilon = 1 + 2**(-p)
    epsilon = one_plus_epsilon - 1

    if epsilon == 0:
      raise ValueError("epsilon cannot be represented for RHS=1pe, n=%d, p=%d, k=%d" % (n, p, k))
    else:
      A = np.ones((n, n))
      A = A + np.eye(n) * epsilon

      b = np.ones((n, 1)) * (1 + epsilon)

      for i in range(2, k+1):
        Atmp = np.ones((n, n))
        Atmp = Atmp + np.eye(n) * i * epsilon

        tmp = 1 + (i + tri_num(i-1)) * epsilon
        btmp = np.ones((n, 1)) * tmp

        A = np.vstack((A, Atmp))
        b = np.vstack((b, btmp))

      c = -np.ones((n, 1))
  return A, b, c

def nPolyBowl_rational(RHS, n, p, k):
  '''
  Generates a nPolyBowl using arbitrary precision rationals via Python's Fraction class.
  Stores all coefficients as Fraction objects for exact arithmetic.
  
  Parameters:
  n: number of variables
  p: the exponent of epsilon, where epsilon = 2^(-p)
  k: number of blocks of constraints
  '''
  if RHS == "npe":
    epsilon = Fraction(1, 2**p)
    
    # A is a matrix of 1s with the diagonal having epsilon added to it.
    # A[i,i] = 1 + epsilon
    A = [[Fraction(1) for _ in range(n)] for _ in range(n)]
    for d in range(n):
      A[d][d] = Fraction(1) + epsilon
    
    # b is a vector of n+epsilon
    b = [Fraction(n) + epsilon for _ in range(n)]
    
    for i in range(2, k+1):
      # Atmp is a matrix of 1s with the diagonal having i*epsilon added to it.
      # Atmp[d,d] = 1 + i*epsilon
      Atmp = [[Fraction(1) for _ in range(n)] for _ in range(n)]
      for d in range(n):
        Atmp[d][d] = Fraction(1) + i * epsilon
      
      # b is a vector of n + i*epsilon + tri_num(i-1)*epsilon
      btmp = [Fraction(n) + (i + tri_num(i-1)) * epsilon for _ in range(n)]
      
      A.extend(Atmp)
      b.extend(btmp)
    
    # c is objective vector of -1s
    c = [Fraction(-1) for _ in range(n)]
  
  elif RHS == "1pe":
    epsilon = Fraction(1, 2**p)
    
    # A is a matrix of 1s with the diagonal having epsilon added to it.
    # A[i,i] = 1 + epsilon
    A = [[Fraction(1) for _ in range(n)] for _ in range(n)]
    for d in range(n):
      A[d][d] = Fraction(1) + epsilon
    
    # b is a vector of 1+epsilon
    b = [Fraction(1) + epsilon for _ in range(n)]
    
    for i in range(2, k+1):
      # Atmp is a matrix of 1s with the diagonal having i*epsilon added to it.
      # Atmp[d,d] = 1 + i*epsilon
      Atmp = [[Fraction(1) for _ in range(n)] for _ in range(n)]
      for d in range(n):
        Atmp[d][d] = Fraction(1) + i * epsilon
      
      # b is a vector of 1 + i*epsilon + tri_num(i-1)*epsilon
      btmp = [Fraction(1) + (i + tri_num(i-1)) * epsilon for _ in range(n)]
      
      A.extend(Atmp)
      b.extend(btmp)
    
    # c is objective vector of -1s
    c = [Fraction(-1) for _ in range(n)]
  return A, b, c

def generate_nPolyBowl_rational_mps(RHS, n, p, k, folder):
  A, b, c = nPolyBowl_rational(RHS, n, p, k)
  write_mps_rational(A, b, c, folder+"nPolyBowl_rational_"+RHS+"_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")

def generate_nPolyBowl_double_mps(RHS, n, p, k, folder):
  try:
    A, b, c = nPolyBowl_double(RHS, n, p, k)
    write_mps_double(A, b, c, folder+"nPolyBowl_double_"+RHS+"_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  except ValueError as e:
    print(f"{e}")

if __name__ == "__main__":
  RHSs = ["npe", "1pe"]
  N = [3, 10, 50]
  P = [50, 51, 52, 53]
  K = [4]

  print("Generating nPolyBowl_double problem instances...")
  for RHS in RHSs:
    for n in N:
      for p in P:
        for k in K:
          generate_nPolyBowl_double_mps(RHS, n, p, k, "Problem_Files/")

  print("Generating nPolyBowl_rational problem instances...")
  for RHS in RHSs:
    for n in N:
      for p in P:
        for k in K:
          generate_nPolyBowl_rational_mps(RHS, n, p, k, "Problem_Files/")

  print("\nDone generating all problem instances!")
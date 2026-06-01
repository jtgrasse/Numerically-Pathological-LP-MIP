import numpy as np
from fractions import Fraction

from prob_gen_helper_funcs import *

def nPolyBowl_double(RHS, n, p, k, folder):
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
      print("epsilon cannot be represented for RHS=npe, n=%d, p=%d, k=%d" % (n, p, k))
    else:
      A = np.ones((n, n))
      A = A + np.eye(n)*epsilon

      b = np.ones((n, 1))
      b = b*(n+epsilon)

      for i in range(2,k+1):
        Atmp = np.ones((n, n))
        Atmp = Atmp + np.eye(n)*i*epsilon

        # tmp = n + i*epsilon + tri_num(i-1)*epsilon
        tmp = n + (i + tri_num(i-1))*epsilon
        btmp = np.ones((n,1))*tmp

        A = np.vstack((A, Atmp))
        b = np.vstack((b, btmp))

      c = -np.ones((n,1))
      write_mps_double(A, b, c, 60, folder+"nPolyBowl_double_npe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  elif RHS == "1pe":
    one_plus_epsilon = 1 + 2**(-p)
    epsilon = one_plus_epsilon - 1

    if epsilon == 0:
      print("epsilon cannot be represented for RHS=1pe, n=%d, p=%d, k=%d" % (n, p, k))
    else:
      A = np.ones((n, n))
      A = A + np.eye(n) * epsilon

      b = np.ones((n, 1)) * (1 + epsilon)

      for i in range(2, k+1):
        Atmp = np.ones((n, n))
        Atmp = Atmp + np.eye(n) * i * epsilon

        # tmp = 1 + (tri_num(i-1)+1) * epsilon
        tmp = 1 + (i + tri_num(i-1)) * epsilon
        btmp = np.ones((n, 1)) * tmp

        A = np.vstack((A, Atmp))
        b = np.vstack((b, btmp))

      c = -np.ones((n, 1))
      write_mps_double(A, b, c, 60, folder + "nPolyBowl_double_1pe_" + str(n) + "_" + str(p) + "_" + str(k) + ".mps")

def nPolyBowl_rational(RHS, n, p, k, folder):
  '''
  Generates a nPolyBowl using the following parameters:
  n: number of variables
  p: the exponent of epsilon, where epsilon = 2^(-p)
  k: number of blocks of constraints
  '''
  if RHS == "npe":
    epsilon = [[],[]]
    epsilon[0] = int(1)
    epsilon[1] = int(2**p)

    # A is a matrix of 1s with the diagonl having epsilon added to it.
    # A[i,i] = 1 + epsilon = 1 + 1/2^p = (2^p + 1)/2^p = epsilon[1]+1 / epsilon[1]
    A = [[],[]]
    A[0] = np.ones((n,n), dtype=int)
    A[0] = A[0] + np.eye(n, dtype=int)*epsilon[1]

    A[1] = np.ones((n,n), dtype=int)
    for d in range(n): A[1][d,d] = epsilon[1]

    # B is a vector of n+epsilon
    # n+epsilon = n + 1/2^p = (n*2^p + 1)/2^p = (n*epsilon[1] + 1) / epsilon[1]
    # watch out for n*(2^p) overflowing
    b = [[],[]]
    b[0] = np.ones((n, 1), dtype=int)
    b[0] = b[0]*(n*epsilon[1]+1)

    b[1] = np.ones((n, 1), dtype=int)
    b[1] = b[1]*epsilon[1]

    for i in range(2,k+1):
      # Atmp is a matrix of 1s with the diagonl having i*epsilon added to it.
      # Atmp[i,i] = 1 + i*epsilon = 1 + i/2^p = (2^p + i)/2^p = (epsilon[1]+i) / epsilon[1]
      Atmp = [[],[]]
      Atmp[0] = np.ones((n,n), dtype=int)
      for d in range(n): Atmp[0][d,d] = epsilon[1]+i

      Atmp[1] = np.ones((n,n), dtype=int)
      for d in range(n): Atmp[1][d,d] = epsilon[1]

      # b is a vector of n + i*epsilon + tri_num(i-1)*epsilon
      # n + i*epsilon + tri_num(i-1)*epsilon = n + i/2^p + tri_num(i-1)/2^p
      # = (n*2^p + i + tri_num(i-1)) / 2^p = (n*epsilon[1] + i + tri_num(i-1)) / epsilon[1]
      btmp = [[],[]]
      btmp[0] = np.ones((n,1), dtype=int)
      btmp[0] = btmp[0]*(n*epsilon[1] + i + tri_num(i-1))
      btmp[1] = np.ones((n,1), dtype=int)
      btmp[1] = btmp[1]*epsilon[1]

      A[0] = np.vstack((A[0], Atmp[0]))
      A[1] = np.vstack((A[1], Atmp[1]))
      b[0] = np.vstack((b[0], btmp[0]))
      b[1] = np.vstack((b[1], btmp[1]))

    c = [[],[]]
    c[0] = -np.ones((n,1), dtype=int)
    c[1] = np.ones((n,1), dtype=int)
    write_mps_rational(A, b, c, folder+"nPolyBowl_rational_npe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  
  elif RHS == "1pe":
    epsilon = [[],[]]
    epsilon[0] = int(1)
    epsilon[1] = int(2**p)

    # A is a matrix of 1s with the diagonl having epsilon added to it.
    # A[i,i] = 1 + epsilon = 1 + 1/2^p = (2^p + 1)/2^p = epsilon[1]+1 / epsilon[1]
    A = [[],[]]
    A[0] = np.ones((n,n), dtype=int)
    A[0] = A[0] + np.eye(n, dtype=int)*epsilon[1]

    A[1] = np.ones((n,n), dtype=int)
    for d in range(n): A[1][d,d] = epsilon[1]

    # B is a vector of 1+epsilon
    # 1+epsilon = 1 + 1/2^p = (2^p + 1)/2^p = (epsilon[1] + 1) / epsilon[1]
    b = [[],[]]
    b[0] = np.ones((n, 1), dtype=int)
    b[0] = b[0]*(epsilon[1]+1)

    b[1] = np.ones((n, 1), dtype=int)
    b[1] = b[1]*epsilon[1]

    for i in range(2,k+1):
      # Atmp is a matrix of 1s with the diagonl having i*epsilon added to it.
      # Atmp[i,i] = 1 + i*epsilon = 1 + i/2^p = (2^p + i)/2^p = (epsilon[1]+i) / epsilon[1]
      Atmp = [[],[]]
      Atmp[0] = np.ones((n,n), dtype=int)
      for d in range(n): Atmp[0][d,d] = epsilon[1]+i

      Atmp[1] = np.ones((n,n), dtype=int)
      for d in range(n): Atmp[1][d,d] = epsilon[1]

      # b is a vector of 1 + epsilon + tri_num(i-1)*epsilon
      # 1 + i*epsilon + tri_num(i-1)*epsilon = 1 + i/2^p + tri_num(i-1)/2^p
      # = (2^p + i + tri_num(i-1)) / 2^p = (epsilon[1] + i + tri_num(i-1)) / epsilon[1]
      btmp = [[],[]]
      btmp[0] = np.ones((n,1), dtype=int)
      btmp[0] = btmp[0]*(epsilon[1] + i + tri_num(i-1))
      btmp[1] = np.ones((n,1), dtype=int)
      btmp[1] = btmp[1]*epsilon[1]

      A[0] = np.vstack((A[0], Atmp[0]))
      A[1] = np.vstack((A[1], Atmp[1]))
      b[0] = np.vstack((b[0], btmp[0]))
      b[1] = np.vstack((b[1], btmp[1]))

    c = [[],[]]
    c[0] = -np.ones((n,1), dtype=int)
    c[1] = np.ones((n,1), dtype=int)
    write_mps_rational(A, b, c, folder+"nPolyBowl_rational_1pe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")

def nPolyBowl_integer_rational(RHS, n, p, k, folder):
  '''
  Generates a nPolyBowl using infinite precision rationals via Python's Fraction class.
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
    
    write_mps_integer_rational(A, b, c, folder+"nPolyBowl_integer_rational_npe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")
  
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
    
    write_mps_integer_rational(A, b, c, folder+"nPolyBowl_integer_rational_1pe_"+str(n)+"_"+str(p)+"_"+str(k)+".mps")

RHSs = ["npe", "1pe"]
N = [10]
P = [80]
K = [4]

# print("Generating nPolyBowl_double problem instances...")
# for RHS in RHSs:
#   for n in N:
#     for p in P:
#       for k in K:
#         nPolyBowl_double(RHS, n, p, k, "Problem_Files/")

# print("Generating nPolyBowl_rational problem instances...")
# for RHS in RHSs:
#   for n in N:
#     for p in P:
#       for k in K:
#         nPolyBowl_rational(RHS, n, p, k, "Problem_Files/")

print("\nGenerating nPolyBowl_integer_rational problem instances...")
for RHS in RHSs:
  for n in N:
    for p in P:
      for k in K:
        nPolyBowl_integer_rational(RHS, n, p, k, "Problem_Files/")

print("\nDone generating all problem instances!")
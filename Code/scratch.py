import numpy as np
from prob_gen_helper_funcs import *

p = 14
n = 32

one_plus_epsilon = add_min_value(1, "sci", p)
epsilon = one_plus_epsilon - 1

sol = (one_plus_epsilon)/(n+epsilon)

LHS1 = one_plus_epsilon
RHS1 = one_plus_epsilon

LHS2 = 1+2*epsilon
RHS2 = (one_plus_epsilon)*(n + 2*epsilon)/(n+epsilon)

LHS3 = 1+3*epsilon
RHS3 = (one_plus_epsilon)*(n + 3*epsilon)/(n+epsilon)

LHS4 = 1+4*epsilon
RHS4 = (one_plus_epsilon)*(n + 4*epsilon)/(n+epsilon)

print(epsilon)
print(sol)
print(LHS1)
print(RHS1)
print(LHS2)
print(RHS2)
print(LHS3)
print(RHS3)
print(LHS4)
print(RHS4)

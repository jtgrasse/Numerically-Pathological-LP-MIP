import numpy as np
import os
import pandas as pd
from fractions import Fraction

from nPolyBowl import *
from helper_funcs import *

# def gurobi_get_sol_vec(file):
#   f = open(file, "r")
#   lines = f.readlines()
#   lines = lines[2:]
#   for i in range(len(lines)):
#     index = lines[i].find(' ')
#     lines[i] = lines[i][index:]
#     lines[i] = lines[i][:-1]
#   sol_vec = np.array(lines, dtype=float)
#   return sol_vec

# def optimality_diff(rhs, n, p, k, sol_vec):
#   if rhs == "npe":
#     opt = Fraction(1)
#   elif rhs == "1pe":
#     epsilon = Fraction(1, 2**p)
#     opt = Fraction(1+epsilon, n+epsilon)
#   opt_val = n*opt
#   sol_val = sum(sol_vec)
#   return sol_val - opt_val

# def gurobi_analyze_sol(rhs, n, p, k, sol_vec):
#   # check for primal feasibility and optimality
#   A, b, c = nPolyBowl_rational(rhs, n, p, k)
#   # Primal feasibility is simply if Ax <= b
#   # Use the Fraction class to compute Ax-b exactly, then report the maximum violation
#   Ax = matvec(A, sol_vec)
#   primal_violation = max(Ax[i] - b[i] for i in range(len(b)))
#   primal_violation = max(primal_violation, 0)  # If the maximum violation is negative, then the solution is feasible
#   # Find the difference between the objective value of the solution and the optimal objective value
#   # Assuming maximization, so if the diff > 0 then the solution is super-optimal, if diff < 0 then the solution is sub-optimal
#   optimality_diff_val = optimality_diff(rhs, n, p, k, sol_vec)
#   return primal_violation, optimality_diff_val

def get_primal_dual_vio(file):
  f = open(file, "r")
  lines = f.readlines()
  primal_vio = Fraction(0)
  dual_vio = Fraction(0)
  for i in range(len(lines)):
    if lines[i].startswith("  max primal feasibility violation = "):
      index = lines[i].find("=")
      primal_vio_str = lines[i][index+2:-1]
      primal_vio = Fraction(primal_vio_str)
      continue
    if lines[i].startswith("  max dual feasibility violation   = "):
      index = lines[i].find("=")
      dual_vio_str = lines[i][index+2:-1]
      dual_vio = Fraction(dual_vio_str)
      continue
  return float(primal_vio), float(dual_vio)

def gurobi_file_to_vec(file):
  print(file)
  tmp = file.split("/")
  tmp = tmp[-1]
  gen_params = tmp.split("_")
  rhs, n, p, k = gen_params[2], gen_params[3], gen_params[4], gen_params[5]
  n, p, k = int(n), int(p), int(k)
  primal_vio, dual_vio = get_primal_dual_vio(file)
  return rhs, n, p, k, primal_vio, dual_vio

# def gurobi_analyze_sol(rhs, n, p, k, primal_basis):
#   # check for primal feasibility
#   A, b, c = nPolyBowl("rational", rhs, n, p, k)
#   # Primal feasibility is simply if [A I] [x s] = b
#   # So with the basis we need to solve for Bx = b for x
#   # Use the Fraction class to compute Ax-b exactly, then report the maximum violation (negative is feasible)
#   B = [A[i] for i in primal_basis]

gurobi_file_to_vec("Solver_Results/Gurobi/nPolyBowl_double_1pe_3_51_4_default_VIO.log")

def gurobi_log_to_vec(file):
  f = open(file, "r")
  lines = f.readlines()
  presolve_time = -1
  solve_iterations = -1
  solve_time = -1
  param_presolve = -1
  param_feasTol = 1e-6
  param_quad = -1
  param_method = -1
  param_concurrentmethod = -1
  param_numericfocus = -1
  for r in lines:
    if r.startswith("Presolve time: "):
      presolve_time = r[15:-2]
      presolve_time = float(presolve_time)
    elif r.startswith("Solved in "):
      solve_times = r.split(" ")
      solve_iterations = solve_times[2]
      solve_iterations = int(solve_iterations)
      solve_time = solve_times[5]
      solve_time = float(solve_time)
    elif r.startswith("FeasibilityTol "):
      param_feasTol = r[15:-1]
      param_feasTol = float(param_feasTol)
    elif r.startswith("Quad "):
      param_quad = r[6:-1]
      param_quad = int(param_quad)
    elif r.startswith("Presolve  "):
      param_presolve = r[10:-1]
      param_presolve = int(param_presolve)
    elif r.startswith("Set parameter Method "):
      param_method = r[29:-1]
      param_method = int(param_method)
    elif r.startswith("Set parameter ConcurrentMethod "):
      param_concurrentmethod = r[39:-1]
      param_concurrentmethod = int(param_concurrentmethod)
    elif r.startswith("Set parameter NumericFocus "):
      param_numericfocus = r[35:-1]
      param_numericfocus = int(param_numericfocus)
  return presolve_time, solve_iterations, solve_time, param_presolve, param_feasTol, param_quad, param_method, param_concurrentmethod, param_numericfocus

gresults_dir = "Solver_Results/Gurobi/"

results_array = np.array([])
for file in os.listdir(gresults_dir):
  file_path = os.path.join(gresults_dir, file)
  if file_path.endswith("_VIO.log"):
    results = gurobi_file_to_vec(file_path)
    results_array = np.append(results_array, results)
    log_file = file_path.replace("_VIO.log", ".log")
    log_results = gurobi_log_to_vec(log_file)
    results_array = np.append(results_array, log_results)

results_array = results_array.reshape(int(len(results_array)/15), 15)
print(results_array)

gurobi_results_df = pd.DataFrame(results_array, columns = ['rhs', 'n', 'p', 'k', 'primal_vio', 'dual_vio', 'presolve_time', 'solve_iterations', 'solve_time', 'presolve', 'feasTol', 'quad', 'method', 'concurrentmethod', 'numericfocus'])
print(gurobi_results_df)

gurobi_results_df.to_csv(gresults_dir+'gurobi_results.csv')
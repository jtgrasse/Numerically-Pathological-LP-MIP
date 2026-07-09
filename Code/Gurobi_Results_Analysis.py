import numpy as np
import os
import pandas as pd
from fractions import Fraction

from nPolyBowl import nPolyBowl_rational, nPolyBowl_double
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

def get_primal_dual_sol(file):
  f = open(file, "r")
  lines = f.readlines()
  primal_sol = []
  dual_sol = []
  primal_section = False
  dual_section = False
  for i in range(len(lines)):
    if lines[i].startswith("SECTION SOLUTION"):
      primal_section = True
      dual_section = False
    if lines[i].startswith("SECTION PI"):
      dual_section = True
      primal_section = False
    if lines[i].startswith("SECTION BASIS"):
      dual_section = False
      primal_section = False

    if primal_section and lines[i].startswith("X"):
      val = lines[i].split(" ")
      primal_sol.append(float(val[-1]))
    if dual_section and lines[i].startswith("R"):
      val = lines[i].split(" ")
      dual_sol.append(float(val[-1]))
  return np.array(primal_sol, dtype=float), np.array(dual_sol, dtype=float)

def gurobi_file_to_vec(file):
  print(file)
  tmp = file.split("/")
  tmp = tmp[-1]
  gen_params = tmp.split("_")
  rhs, n, p, k = gen_params[2], gen_params[3], gen_params[4], gen_params[5]
  n, p, k = int(n), int(p), int(k)
  primal_sol, dual_sol = get_primal_dual_sol(file)
  gurobi_analyze_sol(rhs, n, p, k, primal_sol, dual_sol)
  return rhs, n, p, k

def gurobi_analyze_sol(rhs, n, p, k, primal_sol, dual_sol):
  rat_primal_sol = np.array([Fraction(x) for x in primal_sol])
  rat_dual_sol = np.array([Fraction(x) for x in dual_sol])
  # check for primal feasibility
  A, b, c = nPolyBowl_rational(rhs, n, p, k)
  # Primal feasibility is simply if Ax <= b
  # Use the Fraction class to compute Ax-b exactly, then report the maximum violation (negative is feasible)
  Ax = matvec(A, rat_primal_sol)
  primal_violation = max(Ax[i] - b[i] for i in range(len(b)))
  primal_violation = max(float(primal_violation), 0) 
  print(f"Primal violation: {primal_violation}")
  # Check dual feasibility
  # -A^T y = c
  Aty = matvec(np.transpose(A), rat_dual_sol)
  dual_violation = max(abs(Aty[i] - c[i]) for i in range(len(c)))
  dual_violation = max(float(dual_violation), 0)
  print(f"Dual violation: {dual_violation}")

gurobi_file_to_vec("Solver_Results/Gurobi/nPolyBowl_double_npe_3_15_4_primalquad.attr")

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

# gresults_dir = "Solver_Results/Gurobi/"

# results_array = np.array([])
# for file in os.listdir(gresults_dir):
#   file_path = os.path.join(gresults_dir, file)
#   if file_path.endswith(".attr"):
#     results = gurobi_file_to_vec(file_path)
#     results_array = np.append(results_array, results)
#     log_file = file_path.replace(".attr", ".log")
#     log_results = gurobi_log_to_vec(log_file)
#     results_array = np.append(results_array, log_results)

# results_array = results_array.reshape(int(len(results_array)/15), 15)
# print(results_array)

# gurobi_results_df = pd.DataFrame(results_array, columns = ['rhs', 'n', 'p', 'k', 'primal_violation', 'optimality_diff_val', 'presolve_time', 'solve_iterations', 'solve_time', 'presolve', 'feasTol', 'quad', 'method', 'concurrentmethod', 'numericfocus'])
# print(gurobi_results_df)

# gurobi_results_df.to_csv(gresults_dir+'gurobi_results.csv')
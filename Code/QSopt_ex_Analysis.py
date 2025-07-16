import numpy as np
import os
import pandas as pd

qsresults_dir = "../Solver_Results/QSopt_ex/"
prob_name = "nPolyBowl_1pe_100_12_2"
test_file = qsresults_dir + prob_name + ".log"

def QSopt_ex_log_times(file):
    total_time = -1
    dbl_time = -1
    mpf_times = []
    exact_time = 0


    f = open(file, "r")
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]

        # Check for total time
        s = "Total testing time "
        e = " seconds"
        index=line.find(s)
        if index != -1:
            index_start = index+len(s)
            index_end = line.find(e)
            total_time = float(line[index_start:index_end])

        # Check for dbl time
        s = "DBL solve took "
        e = " seconds"
        index = line.find(s)
        if index != -1:
            index_start = index + len(s)
            index_end = line.find(e)
            dbl_time = float(line[index_start:index_end])

        # Check for mpf times
        s = "MPF solve at "
        e = " bits"
        index = line.find(s)
        if index != -1:
            index_start = index + len(s)
            index_end = line.find(e)
            mpf_precision = int(line[index_start:index_end])
            s = "bits took "
            e = " seconds"
            index = line.find(s)
            index_start = index + len(s)
            index_end = line.find(e)
            mpf_time = float(line[index_start:index_end])
            mpf_times = (mpf_precision, mpf_time)

        # Check for exact time
        s = "QSexact_"
        index = line.find(s)
        if index != -1:
            print(line)
            s = " took "
            e = " seconds"
            index = line.find(s)
            index_start = index + len(s)
            index_end = line.find(e)
            exact_time += float(line[index_start:index_end])

    print("total_time = " + str(total_time))
    print("dbl_time = " + str(dbl_time))
    print(mpf_times)
    print("exact_time = " + str(exact_time))



QSopt_ex_log_times(test_file)

# results_array = np.array([])
# for file in os.listdir(qsresults_dir):
#   file_path = os.path.join(qsresults_dir, file)
#   if file_path.endswith(".log"):
#     results = gurobi_file_to_vec(file_path)
#     results_array = np.append(results_array, results)
#     log_filt = file_path.replace(".sol", ".log")
#     log_results = gurobi_log_to_vec(log_filt)
#     results_array = np.append(results_array, log_results)
#
# results_array = results_array.reshape(int(len(results_array)/13), 13)
# print(results_array)
#
# gurobi_results_df = pd.DataFrame(results_array, columns = ['rhs', 'n', 'p', 'k', 'sol_norm2dist', 'presolve_time', 'solve_iterations', 'solve_time', 'presolve', 'feasTol', 'quad', 'method', 'concurrentmethod'])
# print(gurobi_results_df)
#
# gurobi_results_df.to_csv(gresults_dir+'gurobi_results.csv')

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
#
# def gurobi_analyze_sol(rhs, n, p, k, sol_vec):
#   # is_opt = (sol_vec == np.ones(n)).all()
#   if rhs == "npe":
#     sol_norm2dist = np.linalg.norm(sol_vec - np.ones(n), 2)
#   elif rhs == "1pe":
#     one_plus_epsilon = add_min_value(1, 'sci', p)
#     epsilon = 1-one_plus_epsilon
#     opt_val = one_plus_epsilon/(n+epsilon)
#     opt_vec = np.ones(n)*opt_val
#     sol_norm2dist = np.linalg.norm(sol_vec - opt_vec, 2)
#   else:
#     "error, not a valid rhs"
#
#   return sol_norm2dist
#
# def gurobi_file_to_vec(file):
#   print(file)
#   tmp = file.split("/")
#   tmp = tmp[-1]
#   gen_params = tmp.split("_")
#   rhs, n, p, k = gen_params[1], gen_params[2], gen_params[3], gen_params[4]
#   n, p, k = int(n), int(p), int(k)
#   print("n="+str(n)+", p="+str(p)+", k="+str(k))
#   sol_vec = gurobi_get_sol_vec(file)
#   np.set_printoptions(precision=15)
#   print(sol_vec)
#   sol_norm2dist = gurobi_analyze_sol(rhs, n, p, k, sol_vec)
#   print("sol_norm2dist: "+str(sol_norm2dist))
#   return rhs, n, p, k, sol_norm2dist
#
# gresults_dir = "../Solver_Results/Gurobi/"
#
# # print(gurobi_file_to_vec(gresults_dir+"nPolyBowl_8_11_4_gurobi.sol"))
#
# def gurobi_log_to_vec(file):
#   f = open(file, "r")
#   lines = f.readlines()
#   presolve_time = -1
#   solve_iterations = -1
#   solve_time = -1
#   param_presolve = -1
#   param_feasTol = 1e-6
#   param_quad = -1
#   param_method = -1
#   param_concurrentmethod = -1
#   for r in lines:
#     if r.startswith("Presolve time: "):
#       presolve_time = r[15:-2]
#       presolve_time = float(presolve_time)
#     elif r.startswith("Solved in "):
#       solve_times = r.split(" ")
#       solve_iterations = solve_times[2]
#       solve_iterations = int(solve_iterations)
#       solve_time = solve_times[5]
#       solve_time = float(solve_time)
#     elif r.startswith("FeasibilityTol "):
#       param_feasTol = r[15:-1]
#       param_feasTol = float(param_feasTol)
#     elif r.startswith("Quad "):
#       param_quad = r[6:-1]
#       param_quad = int(param_quad)
#     elif r.startswith("Presolve  "):
#       param_presolve = r[10:-1]
#       param_presolve = int(param_presolve)
#     elif r.startswith("Set parameter Method "):
#       param_method = r[29:-1]
#       param_method = int(param_method)
#     elif r.startswith("Set parameter ConcurrentMethod "):
#       param_concurrentmethod = r[39:-1]
#       param_concurrentmethod = int(param_concurrentmethod)
#   return presolve_time, solve_iterations, solve_time, param_presolve, param_feasTol, param_quad, param_method, param_concurrentmethod
#
# # print("\n\n")
# # print(gurobi_log_to_vec(gresults_dir+"nPolyBowl_8_11_4_gurobi.log"))
#
# results_array = np.array([])
# for file in os.listdir(gresults_dir):
#   file_path = os.path.join(gresults_dir, file)
#   if file_path.endswith(".sol"):
#     results = gurobi_file_to_vec(file_path)
#     results_array = np.append(results_array, results)
#     log_filt = file_path.replace(".sol", ".log")
#     log_results = gurobi_log_to_vec(log_filt)
#     results_array = np.append(results_array, log_results)
#
# results_array = results_array.reshape(int(len(results_array)/13), 13)
# print(results_array)
#
# gurobi_results_df = pd.DataFrame(results_array, columns = ['rhs', 'n', 'p', 'k', 'sol_norm2dist', 'presolve_time', 'solve_iterations', 'solve_time', 'presolve', 'feasTol', 'quad', 'method', 'concurrentmethod'])
# print(gurobi_results_df)
#
# gurobi_results_df.to_csv(gresults_dir+'gurobi_results.csv')
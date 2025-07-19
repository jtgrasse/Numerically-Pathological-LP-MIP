import numpy as np
import os
import pandas as pd

qsresults_dir = "../Solver_Results/QSopt_ex/"

def QSopt_ex_log_times(file, results_dict):
    prob_name = file.split("/")[-1]
    prob_name = prob_name.split(".")[0]

    results_dict[prob_name] = {}

    total_time = -1
    dbl_time = -1
    exact_time = 0
    mpf_times = {}

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
            results_dict[prob_name]["total_time"] = total_time

        # Check for dbl time
        s = "DBL solve took "
        e = " seconds"
        index = line.find(s)
        if index != -1:
            index_start = index + len(s)
            index_end = line.find(e)
            dbl_time = float(line[index_start:index_end])
            results_dict[prob_name]["dbl_time"] = dbl_time

        # Check for mpf times
        s = "MPF solve at "
        e = " bits"
        index = line.find(s)
        if index != -1:
            index_start = index + len(s)
            index_end = line.find(e)
            mpf_precision = line[index_start:index_end]
            mpf_precision = "mpf"+mpf_precision
            s = "bits took "
            e = " seconds"
            index = line.find(s)
            index_start = index + len(s)
            index_end = line.find(e)
            mpf_time = float(line[index_start:index_end])
            results_dict[prob_name][mpf_precision] = mpf_time

        # Check for exact time
        # Save as simple sum of exact functions
        c = "QSexact_"
        index = line.find(c)
        if index != -1:
            s = " took "
            e = " seconds"
            index = line.find(s)
            index_start = index + len(s)
            index_end = line.find(e)
            exact_time += float(line[index_start:index_end])

    results_dict[prob_name]["exact_time"] = exact_time

results_dict = {}
for file in os.listdir(qsresults_dir):
  file_path = os.path.join(qsresults_dir, file)
  if file_path.endswith(".log"):
      print("reading: " + file_path)
      QSopt_ex_log_times(file_path, results_dict)


print(results_dict)
results_df = pd.DataFrame.from_dict(results_dict, orient='index')
print(results_df)
pd.DataFrame.to_csv(results_df, "qsopt_ex_results.csv")
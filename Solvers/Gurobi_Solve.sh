#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi/"
SUFFIX1="_default"
SUFFIX2="_pre0_primal_feas4"
SUFFIX3="_pre0_primal_feas6"
SUFFIX4="_pre0_primal_feas9"
SUFFIX5="_pre0_primal_feas9_quad"
SUFFIX6="_pre0_dual_feas9_quad"
SUFFIX7="_pre0_primaldual_feas9_quad"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	gurobi_cl ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-4 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-6 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-9 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-9 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.txt"
	gurobi_cl Presolve=0 Method=1 FeasibilityTol=1e-9 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.txt"
	gurobi_cl Presolve=0 Method=3 ConcurrentMethod=3 FeasibilityTol=1e-9 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.txt"
done
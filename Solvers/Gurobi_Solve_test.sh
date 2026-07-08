#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi_Test/"
SUFFIX1="_test"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	gurobi_cl Presolve=0 Method=0 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.txt"
	gurobi_cl Presolve=0 Method=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-9 NumericFocus=3 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.txt"
done
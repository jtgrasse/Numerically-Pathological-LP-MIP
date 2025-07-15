#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi/"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	gurobi_cl Presolve=0 Method=3 ConcurrentMethod=3 FeasibilityTol=1e-9 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}_gurobi.sol" LogFile="${SOL_DIR}${PROBLEM_NAME}_gurobi.log" $PROBLEM
done
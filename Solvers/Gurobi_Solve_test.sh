#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi/"
SUFFIX1="_test"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	gurobi_cl Presolve=0 Method=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.dua" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.attr" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.prm" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.txt"
done
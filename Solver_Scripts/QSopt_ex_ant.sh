#!/bin/bash
PROB_DIR="../../../../Problems/"
SOL_DIR="../../../../Solver_Results/QSopt_ex_ant/"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	esolver -O "${SOL_DIR}${PROBLEM_NAME}.sol" -b "${SOL_DIR}${PROBLEM_NAME}.bas" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}_stdout.log"
done
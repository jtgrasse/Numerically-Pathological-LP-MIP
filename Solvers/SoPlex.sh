#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/SoPlex/"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	soplex --real:feastol=0 --real:opttol=0 --int:solvemode=2 --int:syncmode=1 --int:readmode=1 --int:checkmode=2 --writebas="${SOL_DIR}${PROBLEM_NAME}.bas" -X="${SOL_DIR}${PROBLEM_NAME}.sol" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}.txt"
done
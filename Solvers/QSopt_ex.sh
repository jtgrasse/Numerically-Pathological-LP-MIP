#!/bin/bash
PROB_DIR="../Problem_Files/rational/"
SOL_DIR="../Solver_Results/QSopt_ex/rational/"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	./QSopt_ex/build/esolver/esolver -R 10800 -N "${SOL_DIR}${PROBLEM_NAME}" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}.txt"
done

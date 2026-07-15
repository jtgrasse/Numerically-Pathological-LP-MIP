#!/bin/bash
PROBLEM_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi/"
for SOLUTION in "$SOL_DIR"*.bas
do
	echo "############## CHECKING BASIS $SOLUTION ##############"
	# extract the problem name from the solution file name
	PROBLEM_NAME="${SOLUTION##*/}"
	PROBLEM_NAME="${PROBLEM_NAME%_*}"
	# make the violation log file name
	VIOLATION_LOG="${SOLUTION%.bas}"
	./QSopt_ex/build/check_violation/check_violation "$PROBLEM_DIR/$PROBLEM_NAME.mps" "$SOLUTION" &> "${VIOLATION_LOG}_VIO.log"
done
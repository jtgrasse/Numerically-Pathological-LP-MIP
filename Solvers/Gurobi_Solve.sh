#!/bin/bash
PROB_DIR="../Problem_Files/"
SOL_DIR="../Solver_Results/Gurobi/"
SUFFIX1="_default"
SUFFIX2="_primalloose"
SUFFIX3="_primalmod"
SUFFIX4="_primaltight"
SUFFIX5="_dualtight"
SUFFIX6="_primalquad"
SUFFIX7="_dualquad"
for PROBLEM in $PROB_DIR*
do
	PROBLEM_NAME=$(basename "${PROBLEM%.*}")
	echo "############## SOLVING $PROBLEM_NAME ##############"
	echo $PROBLEM
	echo $PROBLEM_NAME
	gurobi_cl ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.attr" ResultFile="${SOL_DIR}${PROBLEM_NAME}.dua" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX1}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-4 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX2}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-6 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX3}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-9 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX4}.txt"
	gurobi_cl Presolve=0 Method=1 FeasibilityTol=1e-9 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX5}.txt"
	gurobi_cl Presolve=0 Method=0 FeasibilityTol=1e-9 NumericFocus=3 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX6}.txt"
	gurobi_cl Presolve=0 Method=1 FeasibilityTol=1e-9 NumericFocus=3 Quad=1 ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.prm" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.bas" ResultFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.attr" LogFile="${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.log" $PROBLEM &> "${SOL_DIR}${PROBLEM_NAME}${SUFFIX7}.txt"
done
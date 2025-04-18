import numpy as np

def write_mps(A, b, c, p, filename="output.mps"):
    """
    Write an LP problem in MPS format.
    Assumes the Ax <= b and -inf < x < inf
    Arguments:
    A -- Coefficient matrix for the constraints.
    b -- Right-hand side vector.
    c -- Objective coefficients vector.
    p -- Precision of what is written to the file
         specified as the number of digits after the decimal point.
         The output is written in scientific notation.
    filename -- Name of the output MPS file.
    """

    num_constraints, num_vars = A.shape

    # Open the file
    with open(filename, "w") as f:
        # Name section
        f.write("NAME          LP_PROBLEM\n")

        # Rows section
        f.write("ROWS\n")
        f.write(" N  OBJ\n")  # Objective row
        for i in range(num_constraints):
            f.write(f" L  R{i+1}\n")  # Less-than constraint rows

        # Columns section
        f.write("COLUMNS\n")
        for j in range(num_vars):
            # Add the objective coefficient for this variable
            f.write(f"    X{j+1}    OBJ     {c[j,0]:.{p}e}\n")

            # Add each constraint coefficient for this variable
            for i in range(num_constraints):
                if A[i, j] != 0:  # Only non-zero entries are included
                    f.write(f"    X{j+1}    R{i+1}   {A[i, j]:.{p}e}\n")

        # RHS section
        f.write("RHS\n")
        for i in range(num_constraints):
            f.write(f"    RHS1    R{i+1}   {b[i,0]:.{p}e}\n")

        # Bounds section (unrestricted variables, so none are specified)
        f.write("BOUNDS\n")
        for j in range(num_vars):
            # Free Variables
            f.write(f" FR BND1    X{j+1}\n")  # "FR" denotes free/unrestricted
            # Integers
            # f.write(f" LI BND1    X{j+1}   -10\n")

        # End the file
        f.write("ENDATA\n")
    print(f"MPS file '{filename}' has been written.")

# Example usage with random A, b, and c
A = np.array([[1, 2, 0], [0, -1, 3]])
b = np.array([[20], [30]])
c = np.array([[3.2], [-1.5], [4.0]])

write_mps(A, b, c, 16, "../Problem_Files/example.mps")
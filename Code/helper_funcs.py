from decimal import Decimal

def float_to_exact_str(x):
    return str(Decimal.from_float(float(x)))

def tri_num(k):
  """
  Generates triangular numbers
  i.e. 0, 1, 3, 6, 10, 15, ...
  """
  return int((k*(k+1))/2)

####################### Output Functions ##########################

def write_mps_double(A, b, c, filename="output.mps"):
    """
    Write an LP problem in MPS format.
    Assumes the Ax <= b and -inf < x < inf
    And minimizes c^T x
    Arguments:
    A -- Coefficient matrix for the constraints.
    b -- Right-hand side vector.
    c -- Objective coefficients vector.
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
            f.write(f" L  R{i + 1}\n")  # Less-than constraint rows

        # Columns section
        f.write("COLUMNS\n")
        for j in range(num_vars):
            # Add the objective coefficient for this variable
            f.write(f"    X{j + 1}    OBJ     {float_to_exact_str(c[j, 0])}\n")

            # Add each constraint coefficient for this variable
            for i in range(num_constraints):
                if A[i, j] != 0:  # Only non-zero entries are included
                    f.write(f"    X{j + 1}    R{i + 1}   {float_to_exact_str(A[i, j])}\n")

        # RHS section
        f.write("RHS\n")
        for i in range(num_constraints):
            f.write(f"    RHS1    R{i + 1}   {float_to_exact_str(b[i, 0])}\n")

        # Bounds section (unrestricted variables, so none are specified)
        f.write("BOUNDS\n")
        for j in range(num_vars):
            # Free Variables
            f.write(f" FR BND1    X{j + 1}\n")  # "FR" denotes free/unrestricted
            # Integers
            # f.write(f" LI BND1    X{j+1}   -10\n")

        # End the file
        f.write("ENDATA\n")
    print(f"MPS file '{filename}' has been written.")

def write_mps_rational(A, b, c, filename="output.mps"):
    """
    Write an LP problem in MPS format using infinite-precision integers via Fraction objects.
    Assumes the Ax <= b and -inf < x < inf
    And minimizes c^T x
    Arguments:
    A -- Coefficient matrix for the constraints (list of lists of Fraction objects)
    b -- Right-hand side vector (list of Fraction objects)
    c -- Objective coefficients vector (list of Fraction objects)
    filename -- Name of the output MPS file.
    """
    num_constraints = len(A)
    num_vars = len(A[0])

    # Open the file
    with open(filename, "w") as f:
        # Name section
        f.write("NAME          LP_PROBLEM\n")

        # Rows section
        f.write("ROWS\n")
        f.write(" N  OBJ\n")  # Objective row
        for i in range(num_constraints):
            f.write(f" L  R{i + 1}\n")  # Less-than constraint rows

        # Columns section
        f.write("COLUMNS\n")
        for j in range(num_vars):
            # Add the objective coefficient for this variable
            f.write(f"    X{j + 1}    OBJ     {c[j].numerator}/{c[j].denominator}\n")

            # Add each constraint coefficient for this variable
            for i in range(num_constraints):
                if A[i][j] != 0:  # Only non-zero entries are included
                    f.write(f"    X{j + 1}    R{i + 1}   {A[i][j].numerator}/{A[i][j].denominator}\n")

        # RHS section
        f.write("RHS\n")
        for i in range(num_constraints):
            f.write(f"    RHS1    R{i + 1}   {b[i].numerator}/{b[i].denominator}\n")

        # Bounds section (unrestricted variables, so none are specified)
        f.write("BOUNDS\n")
        for j in range(num_vars):
            # Free Variables
            f.write(f" FR BND1    X{j + 1}\n")  # "FR" denotes free/unrestricted

        # End the file
        f.write("ENDATA\n")
    print(f"MPS file '{filename}' has been written.")
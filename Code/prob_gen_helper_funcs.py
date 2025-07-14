import numpy as np
from os import error
import scipy as sp
from codecs import decode
import struct
from math import log10, floor


####################### Output Functions ##########################
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

def write_mpsV2(A, b, c, p, filename="output.mps"):
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
            f.write(f" L  R{i + 1}\n")  # Less-than constraint rows

        # Columns section
        f.write("COLUMNS\n")
        for j in range(num_vars):
            # Add the objective coefficient for this variable
            f.write(f"    X{j + 1}    OBJ     {c[j, 0]:.{p}g}\n")

            # Add each constraint coefficient for this variable
            for i in range(num_constraints):
                if A[i, j] != 0:  # Only non-zero entries are included
                    f.write(f"    X{j + 1}    R{i + 1}   {A[i, j]:.{p}g}\n")

        # RHS section
        f.write("RHS\n")
        for i in range(num_constraints):
            f.write(f"    RHS1    R{i + 1}   {b[i, 0]:.{p}g}\n")

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

    # # Example usage with random A, b, and c
    # A = np.array([[1, 2, 0], [0, -1, 3]])
    # b = np.array([[20], [30]])
    # c = np.array([[3.2], [-1.5], [4.0]])
    #
    # write_mps(A, b, c, 16, "../Problem_Files/example.mps")


def tri_num(k):
  """
  Generates triangular numbers
  """
  if k == 0:
    return 0
  else:
    return (k*(k+1))/2

####################### Manipulating Epsilon ##########################
def int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.
        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]

def bin_to_float_64(b):
    """ Convert binary string to a float. """
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>d', bf)[0]

def float_to_bin_64(value):  # For testing.
    """ Convert float to 64-bit binary string. """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)

def bin_add_1(b):
  """ Add the minimum amount to a binary 64bit float """
  flag = 0
  bu = ''
  for i in range(len(b)-1, -1, -1):
    if flag == 0:
      if b[i] == '0':
        bu = '1' + bu
        flag = 1
      else:
        bu = '0' + bu
    else:
      bu = b[i] + bu
  return bu

def find_exp(number) -> int:
    base10 = log10(abs(number))
    return abs(floor(base10))

def add_min_value(value, type, p):
  """
  - sci: scientific notation with n digits after the decimal point.
         Adds 1 to the pth digit
  """
  if type == "sci":
    exp = find_exp(value)
    value = value + 10**(exp-p)
    return value
  else:
    error("Invalid type")
    return None
  # if precision == "double":
  #   return bin_to_float_64(bin_add_1(float_to_bin_64(value)))
  # if precision == "single":
  #   error("Single precision not supported")
  # else:
  #   return value + 1*(10**(-precision))
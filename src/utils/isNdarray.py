import numpy as np

def isNdarray(arr):
  """Check if it is a Ndarray.
  Args:
      arr (any): Value to be checked.
  Returns:
      bool: Returns Returns True if the value is Ndarray, False otherwise.
  """
  return isinstance(arr, np.ndarray)
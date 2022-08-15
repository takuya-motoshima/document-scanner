import numpy as np

def isNdarray(arr):
  """Check if it is a Ndarray.
  Args:
    arr: Value to be checked.
  Returns:
    Returns Returns True if the value is Ndarray, False otherwise.
  """
  return isinstance(arr, np.ndarray)
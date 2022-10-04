import os
from dotenv import dotenv_values
from dotmap import DotMap

def load_env(env_path):
  """Load env.
  Args:
      env_path (str): Path of the .env file.
  Returns:
      DotMap: .env contents.
  """
  if not os.path.exists(env_path):
    raise RuntimeError(f'{env_path} not found')
  return DotMap(dotenv_values(env_path))
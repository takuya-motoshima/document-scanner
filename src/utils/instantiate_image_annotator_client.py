import json
from google.cloud import vision
from google.oauth2 import service_account
from .load_env import load_env

def instantiate_image_annotator_client(env_path):
  """Instantiate ImageAnnotatorClient.
  Args:
      env_path (str): Path of the .env file.
  Returns:
      google.cloud.vision.ImageAnnotatorClient: ImageAnnotatorClient instance.
  """
  env = load_env(env_path)
  if 'GOOGLE_APPLICATION_CREDENTIALS' not in env:
    raise RuntimeError('GOOGLE_APPLICATION_CREDENTIALS not found in .env')
  service_account_creds = json.loads(env['GOOGLE_APPLICATION_CREDENTIALS'])

  # Loading private key (which contains line terminators like '\n') as an environment variable is tricky. Most shells would pad the terminator and treat it as a literal -- i.e. '\\n'. You will have to inspect how that value gets fed into your Python code, and preprocess/unpad accordingly.
  service_account_creds['private_key'] = service_account_creds['private_key'].replace('\\n', '\n')
  return vision.ImageAnnotatorClient(credentials = service_account.Credentials.from_service_account_info(service_account_creds))

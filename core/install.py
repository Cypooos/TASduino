import os

def installModule(module_name):
  """ Ask for the auto instalation of a module
  """

  print("Module ["+module_name+'] is needed to continue. Do you wish to install it automatically ?')
  while True:
    ans = input("(Y)es or (N)o => ").lower()
    if ans in ["n","no"]:
      print("Please install python module called ["+module_name+"]."
      exit()
    elif ans in ["y","yes","ye"]:
      os.system("python3 -m pip install "+module_name)
      print("\n\nIf this work, please restartd.\nIf not, please install it properly.")
      exit()

try:
  import numpy 
except ImportError:
  installModule("numpy")
  
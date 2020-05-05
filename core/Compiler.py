import os


class Compiler():

  def __init__(self,**kwargs):
    self.options = kwargs
    self.path = kwargs.get("compiler_path","core/compiler/")

  def sendProgram(self):
    pass

  def compileProgram(self,program):
    os.system("make -C core/LUFA")
    os.system("make -C core/compiler")
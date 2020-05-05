import os
import subprocess

class Compiler():

  def __init__(self,**kwargs):
    self.options = kwargs

  def sendProgram(self,name):
    model = self.options.get("dfu-model","atmega16u2")
    # atmega16u2 for arduino UNO
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash core/compiler/"+name+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def compileProgram(self,program):
    # change makefile with configuration

    # building LUFA
    if not os.path.exists('/LUFA/LUFA/'): # not sure yet
      subprocess.run("make all -C /LUFA", shell=True)

    # building program
    subprocess.run("make -C /compiler")

    # moving program to /compiled
    os.rename("compiler/"+program+".hex", "compiler/compiled/"+program+".hex")

    # deleting useless out files
    for x in [".bin",".eep",".elf",".lss",".map",".sym"]
      os.remove("compiler/"+program+x)

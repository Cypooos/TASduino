import os
import subprocess

class Compiler():

  def __init__(self,**kwargs):
    self.options = kwargs
    self.makefileDict = {
      "MCU":self.options.get("dfu-model","atmega16u2"),
      "ARCH":self.options.get("arch","AVR8"),
      "F_CPU":self.options.get("f-cpu","16000000"),
      "F_USB":self.options.get("f-usb","16000000"),
      "OPTIMIZATION":self.options.get("optimization","s"),
      "INCLUDE_DIR":self.options.get("include-dir","include"),
      "SRC_DIR":self.options.get("src-dir","src"),
      "PROGRAM":None,
      "SRC":self.options.get("src",["$(SRC_DIR)/Joystick.c","$(SRC_DIR)/Descriptors.c","$(SRC_DIR)/custom/$(PROGRAM).c","$(LUFA_SRC_USB)"]),
      "LUFA_PATH":self.options.get("lufa-dir","../LUFA/LUFA"),
      "CC_FLAGS":self.options.get("cc flags","-DUSE_LUFA_CONFIG_HEADER -Iinclude/"),
      "LD_FLAGS":self.options.get("ld-flags",""),
    }
  
  def resetFirmware(self):
    model = self.options.get("dfu-model","atmega16u2")
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash compiler/compiled/firmwares/"+model+".hex")
    os.system("sudo dfu-programmer "+model+" reset")



  def sendProgram(self,name):
    model = self.options.get("dfu-model","atmega16u2")
    # atmega16u2 for arduino UNO
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash core/compiler/"+name+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def assembleProgram(self,program):
    makefileDict["PROGRAM"] = program
    file = open('makefile', 'w')
    data = ""
    # read value for makefile
    for key, value in self.makefileDict:
      data.append(key+" = "+value+"\n")
    
    data.append(self.options["makefile"])
    
    # change makefile with configuration
    file.writelines( data )

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

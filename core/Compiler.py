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
      "SRC":self.options.get("src","$(SRC_DIR)/Joystick.c $(SRC_DIR)/Descriptors.c $(SRC_DIR)/custom/$(PROGRAM).c $(LUFA_SRC_USB)"),
      "LUFA_PATH":self.options.get("lufa-dir","LUFA/LUFA"),
      "CC_FLAGS":self.options.get("cc flags","-DUSE_LUFA_CONFIG_HEADER -Iinclude/"),
      "LD_FLAGS":self.options.get("ld-flags",""),
    }
    self.reloadFirmwares()
  
  def reloadFirmwares(self):
    returning = []
    for file in os.listdir("core/compiler/compiled/firmwares/"):
      if file.endswith(".hex"):
        returning.append(file.split("/")[-1].split(".")[0])
    self.options["Valid Firmwares"] = returning
  
  def resetFirmware(self):
    model = self.options.get("dfu-model","atmega16u2")
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash compiler/compiled/firmwares/"+model+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def compileProgram(self):
    pass


  def sendProgram(self,name):
    model = self.options.get("dfu-model","atmega16u2")
    # atmega16u2 for arduino UNO
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash core/compiler/compiled/"+name+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def assembleProgram(self,program):
    self.makefileDict["PROGRAM"] = program
    file_w = open('core/makefile', 'w')
    file_r = open('core/compiler/base.mk', 'r')
    data = ""
    # read value for makefile
    for key, value in self.makefileDict.items():
      data += key+" = "+value+"\n"
    
    data +=file_r.read()
    
    # change makefile with configuration
    file_w.writelines( data )
    
    file_r.close()
    file_w.close()

    # building LUFA
    os.system("make all -C core/LUFA/")

    print("making...")

    # building program
    os.system("make -C core/compiler")

    # moving program to /compiled
    os.rename("core/compiler/"+program+".hex", "core/compiler/compiled/"+program+".hex")

    # deleting useless out files
    for x in [".bin",".eep",".elf",".lss",".map",".sym"]:
      os.remove("core/compiler/"+program+x)

import os
import subprocess
import importlib

class Compiler():

  def __init__(self,**kwargs):
    self.options = kwargs
    self.makefileDict = {
      "MCU":None,
      "ARCH":self.options.get("arch","AVR8"),
      "F_CPU":self.options.get("f-cpu","16000000"),
      "F_USB":self.options.get("f-usb","16000000"),
      "OPTIMIZATION":self.options.get("optimization","s"),
      "DIR":None,
      "TAS_DATA":None,
      "SRC":None,
      "LUFA_PATH":self.options.get("lufa-dir","LUFA/LUFA"),
      "CC_FLAGS":self.options.get("cc-flags","-DUSE_LUFA_CONFIG_HEADER -Iinclude/"),
      "LD_FLAGS":self.options.get("ld-flags",""),
    }
    self.reloadFirmwares()
    self.reloadBasicFirmwares()
    self.reloadJoysticks()
  
  def reloadFirmwares(self):
    returning = []
    for file in os.listdir("core/compiler/firmwares/"):
      if file.endswith(".hex"):
        returning.append(file.split("/")[-1].split(".")[0])
    self.options["Firmwares"] = returning

  def reloadBasicFirmwares(self):
    returning = []
    for file in os.listdir("core/compiler/basic_firmwares/"):
      if file.endswith(".hex"):
        returning.append(file.split("/")[-1].split(".")[0])
    self.options["Basic Firmwares"] = returning
    
  def reloadJoysticks(self):
    returning = []
    for file in os.listdir("core/compiler/joysticks/"):
      if os.path.isdir("core/compiler/joysticks/"+file):
        returning.append(file.split("/"))
    self.options["Joysticks"] = returning
  
  def resetFirmware(self):
    try:
      model = self.options["dfu-model"]
    except KeyError: raise AssertionError("Please select a DFU card !")
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash compiler/firmwares/"+model+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def sendFirmware(self,name):
    try:
      model = self.options["dfu-model"]
    except KeyError: raise AssertionError("Please select a DFU card !")
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash core/compiler/firmwares/"+name+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def getJoystickInfoArg(self,prog,arg):
    with open("core/compiler/joystick/"+prog+"/info.txt","r") as prog_f:
      for x in prog_f.readlines():
        if x.split(":")[0] == arg: return ":".join(x.split(":")[1:])
    return None

  def compileJoystick(self,program,tas_file):
    assembly = importlib.import_module("core.compiler.joysticks."+program+".assembly")
    try:model = self.options["dfu-model"]
    except KeyError: raise AssertionError("Please select a DFU card !")
    if not model in self.getJoystickInfoArg(program,"compatibility").split(","): raise AssertionError("Joystick not compatible with the selected dfu card")
    
    self.makefileDict["DIR"] = program+"/"
    assembly.assembly(tas_file,"core/compiler/joysticks/"+program+"/")
    self.makefileDict["MCU"] = model

    file_w = open('core/makefile', 'w')
    data = ""
    print("Writing...")

    # use write options and basic makefile
    if self.getJoystickInfoArg(program,"makefile") == "":
      self.makefileDict["SRC"] = self.getJoystickInfoArg(program,"makefile_src")
      file_r = open('core/compiler/base.mk', 'r')
      for key, value in self.makefileDict.items():
        data += key+" = "+value+"\n"
    else:
      # write options and custom makefile
      for key, value in self.makefileDict.items():
        data += key+" = "+value+"\n"
      file_r = open('core/compiler/'+program+"/"+self.getJoystickInfoArg(program,"makefile"), 'r')
    
    # add the makefile main content
    data +=file_r.read()
    
    # change makefile with configuration
    file_w.writelines( data )
    
    file_r.close()
    file_w.close()

    # building LUFA
    os.system("make all -C core/LUFA/")

    # building Joystick
    os.system("make -C core/compiler")

    # moving Joystick to /firmwares
    os.rename("core/compiler/"+program+".hex", "core/compiler/firmwares/"+program+".hex")

    # deleting useless out files
    for x in [".bin",".eep",".elf",".lss",".map",".sym"]:
      os.remove("core/compiler/"+program+x)

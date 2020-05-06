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
      "DIR":None,
      "TAS_DATA":None,
      "SRC":None,
      "LUFA_PATH":self.options.get("lufa-dir","LUFA/LUFA"),
      "CC_FLAGS":self.options.get("cc flags","-DUSE_LUFA_CONFIG_HEADER -Iinclude/"),
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
      if os.path.isdir(file):
        returning.append(file.split("/"))
    self.options["Joysticks"] = returning
  
  def resetFirmware(self):
    model = self.options.get("dfu-model","atmega16u2")
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash compiler/firmwares/"+model+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def assembleProgram(self):
    pass

  def sendFirmware(self,name):
    model = self.options.get("dfu-model","atmega16u2")
    # atmega16u2 for arduino UNO
    os.system("sudo dfu-programmer "+model+" erase") # changing param. 
    os.system("sudo dfu-programmer "+model+" flash core/compiler/firmwares/"+name+".hex")
    os.system("sudo dfu-programmer "+model+" reset")

  def getJoystickInfoArg(self,prog,arg):
    with open("core/compiler/joystick/"+prog+"/info.txt","r") as prog_f:
      for x in prog_f.readlines():
        if x.split(":")[0] == arg: return ":".join(x.split(":")[1:])
    return None

  def compileJoystick(self,program,tas_data):
    if not self.options.get("dfu-model","atmega16u2") in self.getProgArg(program,"compatibility").split(","): raise AssertionError("Joystick not compatible with selected dfu card")
    self.makefileDict["DIR"] = program+"/"
    self.makefileDict["TAS_DATA"] = tas_data
    self.makefileDict["SRC"] = self.getProgArg(program,"makefile_src")
    file_w = open('core/makefile', 'w')
    data = ""

    # use basic makefile and options
    if self.getProgArg(program,"makefile") == "":
      file_r = open('core/compiler/base.mk', 'r')
      for key, value in self.makefileDict.items():
        data += key+" = "+value+"\n"
    else:
      # only write dir, MCU & tasdata option and custom makefile
      data+="DIR = "+self.makefileDict["DIR"]+"\n"
      data+="TAS_DATA = "+self.makefileDict["TAS_DATA"]+"\n"
      data+="MCU = "+self.options.get("dfu-model","atmega16u2")
      file_r = open('core/compiler/'+program+"/"+self.getProgArg(program,"makefile"), 'r')
    
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

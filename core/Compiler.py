import os


class Compiler():

  def __init__(self,**kwargs):
    self.options = kwargs

  def sendProgram(self,name):
    os.system("sudo dfu-programmer atmega16u2 erase") # changing param. 
    os.system("sudo dfu-programmer atmega16u2 flash core/compiler/"+name+".hex")
    os.system("sudo dfu-programmer atmega16u2 reset")

  def compileProgram(self,program):
    # change makefile with configuration
    os.system("make -C core/LUFA") # if not already build. Silence the shell
    os.system("make -C core/compiler") # Silence the shell. 
    # move and rename output file (.hex) to compiled/
    # delete .bin .eep .elf .lss .map .sym

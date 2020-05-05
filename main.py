from TAS import TAS
from core import Compiler
from GUI import GUI

TASmanager = TAS.TASmanager()
compiler = Compiler.Compiler()

gui = GUI.GraphicalUserInterface(TASmanager,compiler)
gui.start()
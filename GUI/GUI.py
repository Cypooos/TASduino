import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as scrolledtext
import traceback
import sys, os
import webbrowser



def alert():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be created.")
def link():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be linked.")

class GraphicalUserInterface():

  def __init__(self,tasManager,compiler):
    self.debugmode = False
    self.windows = tk.Tk()
    self.windows.geometry("500x300")
    self.windows.minsize(250, 150) 
    self.tasManager = tasManager
    self.compiler = compiler

    self.tasFrame = None
    self.menubar = None
  
  def openTAS(self):
    filepath = filedialog.askopenfilename(title="Ouvrir une TAS",filetypes=[('TAS absolute format','.tas'),('TAS relative format','.rtas'),('all files','.*')])
    self.tasManager.openTAS(filepath)
    alert()
    return
  
  def setupMenu(self):

    self.menubar = tk.Menu(self.windows)

    self.menu_file = tk.Menu(self.menubar, tearoff=0)
    self.menu_file.add_command(label="Create", command=link)
    self.menu_file.add_command(label="Open", command=link)
    self.menu_file.add_command(label="Save", command=link)
    self.menu_file.add_command(label="Save as", command=link)
    self.menu_file.add_separator()
    self.menu_file.add_command(label="Convert", command=link) # cascade
    self.menu_file.add_command(label="Quit", command=self.windows.quit)
    self.menubar.add_cascade(label="File", menu=self.menu_file)

    
    self.menubar.add_cascade(label="Loading...", menu=self.menu_file)
    self.refreshMenuCompiler()


    menu_info = tk.Menu(self.menubar, tearoff=0)
    menu_info.add_command(label="Informations", command=lambda : messagebox.showinfo("Informations","Go to the GitHub for more information about the project !\nhttps://github.com/Discursif/TASduino"))
    menu_info.add_command(label="Credits", command=lambda : messagebox.showinfo("Credits","TASduino is created by </Discursif>\nWith the help of the TASbot discord\nThanks to MonsterDruide1#7702 for his Joystick's script <3"))
    menu_info.add_command(label="Help", command=lambda : messagebox.showinfo("Help","TASduino have a wiki !\nhttps://github.com/Discursif/TASduino/wiki"))
    self.menubar.add_cascade(label="More", menu=menu_info)

    self.windows.config(menu=self.menubar)

  def setupMainFrame(self):
    self.tasFrame = tk.LabelFrame(self.windows, text="Tas file", width=60)
    self.metaFrame = tk.LabelFrame(self.windows, text="META data")
    self.tasFrame.pack(side = tk.LEFT, fill = tk.Y, padx = 5, pady = 5)
    self.metaFrame.pack(side = tk.RIGHT, fill = tk.Y, padx = 5, pady = 5)
    tasFrame_entry = scrolledtext.ScrolledText(self.tasFrame)
    tasFrame_entry.pack(expand = True, fill = tk.BOTH)

  def showError(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Error', err[-1])
    print("\n".join(err))

  def start(self):
    self.setupMenu()
    tk.Tk.report_callback_exception = self.showError
    self.setupMainFrame()
    self.windows.mainloop()

    self.windows.bind('<Button-2>', self.event)
  
  def event(self,event):
    self.refreshMenuCompiler()
  
  def refreshMenuCompiler(self):
    self.menu_compiler = tk.Menu(self.menubar, tearoff=0)
    self.menu_compiler.add_command(label="Compile", command=lambda:self.compiler.compileJoystick(self.compiler.options["Joysticks"],self.tasManager.activeTas.path))
    

    self.menu_compiler_models = tk.Menu(self.menubar, tearoff=0)
    def setFirm(firm):
      self.compiler.options["dfu-model"] = firm
    for x in self.compiler.options["Basic Firmwares"]:
      self.menu_compiler_models.add_radiobutton(label=x, command=lambda:setFirm(x))
    self.menu_compiler_models.add_separator()
    self.menu_compiler_models.add_command(label="Reload", command=lambda : self.compiler.reloadBasicFirmwares)
    self.menu_compiler_models.add_command(label="Reset Firmware", command=lambda : self.compiler.resetFirmware())
    self.menu_compiler.add_cascade(label="Set dfu model",menu=self.menu_compiler_models)
    
    self.menu_compiler_send = tk.Menu(self.menubar, tearoff=0)
    def sendFirm(firm):
      self.compiler.sendFirmware(firm)
    for x in self.compiler.options["Firmwares"]:
      self.menu_compiler_send.add_radiobutton(label=x, command=lambda:sendFirm(x))
    self.menu_compiler_send.add_separator()
    self.menu_compiler_send.add_command(label="Reload", command=lambda : self.compiler.reloadFirmwares())
    self.menu_compiler.add_cascade(label="Send Firmware",menu=self.menu_compiler_send)
    
    self.menu_compiler_joystick = tk.Menu(self.menubar, tearoff=0)
    def setJoy(joy):
      self.tasManager.activeTas.metadata["joystick"] = joy # put in metadata of TAS file the joy connected
    for x in self.compiler.options["Joysticks"]:
      self.menu_compiler_joystick.add_radiobutton(label=x, command=lambda:setJoy(x))
    self.menu_compiler_joystick.add_separator()
    self.menu_compiler_joystick.add_command(label="Reload", command=lambda : self.compiler.reloadJoysticks())
    self.menu_compiler.add_cascade(label="Joysticks",menu=self.menu_compiler_joystick)

    self.menu_compiler.add_command(label="Options", command=lambda:self.setCompilerOptions())

    self.menubar.entryconfigure(2,label="Compiler", menu=self.menu_compiler)
    
  def askInputs(self,inputs):
    askWin = tk.Tk()
    values = {}
    count = 0
    for key in inputs:
      tk.Label(askWin, text=key).grid(row=count, sticky=tk.W)
      en = tk.Entry(askWin)
      values[key] = en
      en.grid(row=count, column=1)
      count +=1
    tk.Button(askWin, text = "Send", command = lambda: askWin.destroy()).grid(row=count,column=2)
    askWin.mainloop()
    return [y.get() for y in values.values()]

  def setCompilerOptions(self):
    def saveConf():
      self.compiler.makefileDict = {x:y.get() for x,y in entrys.items()}
      print(self.compiler.makefileDict)
      self.compiler.reloadBasicFirmwares()
      self.compiler.reloadFirmwares()
      self.compiler.reloadJoysticks()
      self.refreshMenuCompiler()
      OptWindow.destroy()
    def openMake():
      print("Opening:"+ os.path.dirname(os.path.realpath(__file__))+"/../core/compiler/base.mk")
      webbrowser.open('file:///' +os.path.dirname(os.path.realpath(__file__))+"/../core/compiler/base.mk")
    def addOpt():
      vals = self.askInputs(["Key :","Value :"])
      self.compiler.makefileDict = {x:y.get() for x,y in entrys.items()}
      self.compiler.makefileDict[vals[0]] = vals[1]
      print(self.compiler.makefileDict)
      self.compiler.reloadBasicFirmwares()
      self.compiler.reloadFirmwares()
      self.compiler.reloadJoysticks()
      self.refreshMenuCompiler()
      OptWindow.destroy()
    OptWindow = tk.Tk()
    count = 1
    entrys = {}
    tk.Label(OptWindow,text="Makefile entries :").grid(row=0)
    for key,value in self.compiler.makefileDict.items():
      tk.Label(OptWindow, text=key).grid(row=count, sticky=tk.W)
      if not key in ["MCU","TAS_DATA","SRC","DIR"]:val = tk.StringVar(OptWindow, value=value)
      else: val = tk.StringVar(OptWindow, value="--Preset--")
      en = tk.Entry(OptWindow, textvariable=val)
      entrys[key] = en
      en.grid(row=count, column=1)
      count +=1
    tk.Button(OptWindow, text ="Save", command = lambda: saveConf()).grid(row=count)
    tk.Button(OptWindow, text ="Exit", command = lambda: OptWindow.destroy()).grid(row=count,column=1)
    tk.Button(OptWindow, text ="Add", command = lambda: addOpt()).grid(row=count+1)
    tk.Button(OptWindow, text ="Open Makefile", command = lambda: openMake()).grid(row=count+1,column=1)
    OptWindow.mainloop()

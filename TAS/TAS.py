class TAS():

  def __init__(self,path,metadata={}):
    self.path = path
    self.metadata = metadata
    self.isRelativeMode = False

  def read(self):
    if self.path is None:
      return "# Nothing yet as been written !\n#\n# Add your first TAS intructions,\n# Choose the format,\n# Add credits\n# and you're set !"
    else:
      f = open(self.path,"r")
      data = "\n".join(f.readlines())
      f.close()
      return data





class TASmanager():

  def __init__(self):
    self.Tases = {}
    self.reloadTases()
    self.activeTas = TAS(None) # new
    self.data = self.activeTas.read()
  
  def saveAsTas(self,path):
    self.activeTas.path = path
    self.saveTas()
    
  def saveTas(self):
    if self.activeTas.path is None: raise AssertionError("No path attached to this TAS file.")
    # save data
    f = open(self.activeTas.path,"w")
    f.write(self.data)
    f.close()
    # remove the metadata
    f_read = open("TAS/tases.txt","r")
    content = f_read.read().replace("\n","").split(";")
    f_read.close()
    newfile = []
    for x in content:
      if not x.split(":")[0] == self.activeTas.path:
        newfile.append(x)
    # write new metadata
    tell = {x+":"+y+"," for x,y in metadata.items()}
    newfile.append(path+","+tell+";")
    f_write = open("TAS/tases.txt","w")
    f_write.write(";\n".join(newfile))
    f_write.close()
    self.reloadTases()

  def newTas(self):
    self.activeTas = Tas(None)
  
  def reloadTases(self):
    f_read = open("TAS/tases.txt","r")
    content = f_read.read().replace("\n","").split(";")
    f_read.close()
    for x in content:
      self.loadTas(x.split(",")[0],{x.split(":")[0]:y.split(":")[1] for x in x.split(",")[1:]})
  
  def loadTas(self,path,metadata):
    self.Tases[path.split("/")[-1].split(".")[0]] = TAS(path,metadata)
  
  


    





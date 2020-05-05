
class TASinputs():
  def __init__(self,buttons,timeWait):
    self.buttons = buttons
    self.timeWait = timeWait # time before playing next TASinputs()

class TASsection():

  def __init__(self,absoluteTime=None):
    self.inputs = []
    self.abosluteTime # fix the section to a certain position

  def add(self,element):
    self.inputs.append(element)


class TAS():

  def __init__(self):
    self.sections = []
  
  def add_section(self,section):
    self.sections.append(section)
  
  def add_inputs(self,element):
    self.sections[-1].append(element)



class TASmanager():

  def __init__(self):
    self.tases = []
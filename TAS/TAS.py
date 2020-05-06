
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
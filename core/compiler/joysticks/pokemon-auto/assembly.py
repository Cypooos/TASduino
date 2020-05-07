def assembly(tasPath,JoystickPath):
  tasFile = open(tasPath,"r")
  content = tasFile.readlines() # read tas data
  tasFile.close()

  outputpath = open(JoystickPath+"src/tas.c","w")
  for x in ct:
    outputpath.write(content)
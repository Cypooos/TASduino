
def convert(fileToConvert,fileOutput):
  print("-- Converting the Relative TAS file in absolute TAS file --")
  file_r = open(fileToConvert,"r")
  file_w = open(fileOutput,"w")
  position = 0
  while True:
    content = file_r.readline()
    if content == "":break;
    nb_frame = int(content.split(" ")[0])
    for x in range(nb_frame):
      file_w.write(str(position)+" "+" ".join(content.split(" ")[1:]))
      position +=1

  file_r.close()
  file_w.close()


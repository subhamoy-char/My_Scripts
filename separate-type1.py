NUM_OF_LINES=424
filename = '../XDATCAR'
with open(filename) as fin:
    fout = open("output1.txt","wb")
    for i,line in enumerate(fin,1):
      fout.write(line)
      if i%NUM_OF_LINES == 0:
        fout.close()
        fout = open("output%d.txt"%(i/NUM_OF_LINES+1),"wb")

    fout.close()

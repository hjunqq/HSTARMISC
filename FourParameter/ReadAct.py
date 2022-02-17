import numpy as np
import matplotlib.pyplot as plt

actfile = open("D:\\HSTAR_Q\\HSTAR_Q\\Example\\ToumiBeam\\Whole\\TwoGroup\\1.act",'r')

react = []

lines = actfile.readlines()
jline = 0
iline = lines[jline]
var = iline.split()
noutfix = len(var)-1
for iline in range(len(lines)):
	if jline>len(lines)-1:
		break
	iline = jline
	line = lines[iline]
	var = line.split()
	react.append(list(map(float,var[1:])))
	jline += 3
	jline += noutfix*3
	jline += 1

print("Read Finish")

# coding:utf-8
import sys
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [
       '\\usepackage{CJK}',
       r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
       r'\AtEndDocument{\end{CJK}}',
]

def ParseCtr(path):
	times = 0
	isParse = False
	stepStat = []
	bodyStat = []
	with open(path+'\\1.ctr','r') as f:
		lines = f.readlines()
		for line in lines:
			# if times>1:
			# 	break
			if line[0:29]==' igaps,ipairs,,state,,ctforce':
				isParse = False
			if line[0:24]==" *****CONTACT GAPS******":
				times +=1
				if times > 1 :
					stepStat.append(bodyStat)
					# Opened,Closed,Slided = Statics(bodyStat)
					# print(Opened,'\t',Closed,'\t',Slided)
					bodyStat = []
				isParse = False
			if isParse:
				data = line.split()
				bodyStat.append([int(data[0]),list(map(float,data[1:]))])
			if line[0:21]==' BLOCK RIGID MOVEMENT':
				isParse = True
	nbody = len(stepStat[0])
	nstep = len(stepStat)
	print('Numbers of Body is ',nbody)


	for ibody in range(nbody):
		for istep in range(nstep):
			if ibody+1==stepStat[istep][ibody][0]:
				print(ibody+1,stepStat[istep][ibody][1])

	return stepStat

def PlotStepStat(stepStat):
	nbody = len(stepStat[0])
	nstep = len(stepStat)
	timeTag = []
	for istep in range(8):
			timeTag.append(1.0)
	for istep in range(9,29):
			timeTag.append((10.0-1.0)/20*(istep-8)+1.0)
	
	plotStep = 15
	plt.figure(figsize=(4,3.75))
	plt.xlim(0,11)
	for ibody in range(nbody):
		y = []
		for istep in range(plotStep):
			y.append(stepStat[istep][ibody][1][1])
		plt.plot(timeTag[0:plotStep],y,'-',linewidth=0.5,  markersize=2,label=r"Body-"+str(ibody+1))
		
	plt.legend(loc='upper right')
	plt.show()

if __name__=='__main__':
	path = ""

	if(len(sys.argv)>1):
		path =sys.argv[1]

	if path=="":
		path="D:\\ShaPai\\NewModel\\23Deploy\\DD"

	stepStat = ParseCtr(path)
	#print("共有点对数为：",len(GapStat))	
	
	# Opened,Closed,Slided = Statics(GapStat)
	# print(len(GapStat),Opened,Closed,Slided)
	PlotStepStat(stepStat)

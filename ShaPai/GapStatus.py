# coding:utf-8
import sys

def ParseCtr(path):
	times = 0
	isParse = False
	StepStat = []
	GapStat = []
	AllStat = []
	with open(path+'.ctr','r') as f:
		lines = f.readlines()
		for line in lines:
			# if times>1:
			# 	break
			if line[0:24]==" *****CONTACT GAPS******":
				times +=1
				if times > 1 :
					StepStat.append(GapStat)
					Opened,Closed,Slided = Statics(GapStat)
					print(Opened,'\t',Closed,'\t',Slided)
					GapStat = []
					AllStat.append([Opened,Closed,Slided])
				isParse = False
			if isParse:
				GapStat.append(int(line.split()[4]))
			if line[0:29]==' igaps,ipairs,,state,,ctforce':
				isParse = True
	with open(path+".sctr",'w') as f:
		for listi in AllStat:
			f.write(','.join(str(j) for j in listi)+"\n")

	print(len(StepStat))
	return StepStat

def ParseChk(path):
	k = []
	with open(path+'.chk','r') as f:
		lines = f.readlines()
		for line in lines:
			if line[0:9] == " k_safety":
				k.append(float(line.split()[1]))
	
	with open(path+'.k','w') as f:
		for ik in k:
			f.write(str(ik)+'\n')

def Statics(GapStat):
	Opened = 0
	Closed = 0
	Slided = 0
	for istat in GapStat:
		if istat==0:
			Opened +=1
		elif istat==1:
			Closed +=1
		elif istat==2:
			Slided +=1
		else:
			print("Undeterminated State")
	return Opened,Closed,Slided

if __name__=='__main__':
	path = ""

	if(len(sys.argv)>1):
		path =sys.argv[1]
	else:
		exit();

	# if path=="":
	# 	path="D:\\ShaPai\\NewModel\\SL1.0"

	GapStat = ParseCtr(path)
	#print("共有点对数为：",len(GapStat))	
	
	# Opened,Closed,Slided = Statics(GapStat)
	# print(len(GapStat),Opened,Closed,Slided)

	KStat = ParseChk(path)


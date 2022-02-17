#coding:utf-8
import numpy as np
from progressbar import *


def distance(c1,c2):
	d = 0
	for p1,p2 in zip(c1,c2):
		d+=(p1-p2)*(p1-p2)
	return np.sqrt(d)

def find_closed_nodes(nodes,elems,tol):
	progress = ProgressBar()
	pair = []
	nnodes = len(nodes)
	nelems = len(elems)
	#for inodes in range(0,nnodes):
	#	c1 = nodes[inodes]
	#	for jnodes in range(inodes+1,nnodes):
	#		c2 = nodes[jnodes]
	#		d = distance(c1,c2)
	#		if(d<tol):
	#			pair.append([inodes,jnodes])
	#			print(inodes,jnodes)
	ndtag = [0 for i in range(nnodes)]
	print('Find Gaps')
	for ielem in progress(range(nelems)):
		enode = elems[ielem][0]
		nlist = elems[ielem][1:enode+1]
		for inode in range(enode):
			ndindi = nlist[inode]
			c1 = nodes[nlist[inode]-1]  #0 based to 1 based
			for jnode in range(inode+1,enode):
				ndindj = nlist[jnode]
				c2 = nodes[nlist[jnode]-1]  #0 based to 1 based
				if(ndindi!=ndindj):
					if(distance(c1,c2)<tol):
						ndtag[ndindi-1] = ndindj-1
						ndtag[ndindj-1] = ndindi-1
						# print(ielem+1,ndindi,ndindj)
	progress.finish()
	progress = ProgressBar()
	print('Gathering Pairs')
	with open('D:\\ShaPai\\02Model\\1.pair','w') as f:
		for inode in progress(range(nnodes)):
			if(ndtag[inode]>inode):
				pair.append([inode+1,ndtag[inode]+1])
				f.write(str(inode+1)+'\t'+str(ndtag[inode]+1)+'\n')
			#print(inode+1,ndtag[inode]+1)
	progress.finish()
	return pair

def gen_map(pair,nnodes):
	ndmp = [i+1 for i in range(0,nnodes)]
	for ipair in pair:
		imaster = min(ipair)
		islaver = max(ipair)
		ndmp[islaver-1] = imaster   # Pair is 1 based
	with open('D:\\ShaPai\\02Model\\1.ndmp','w') as f:
		for inode in range(nnodes):
			f.write(str(ndmp[inode])+'\n')
	return ndmp

def replace_nodes(elems,ndmp):
	newelem = []
	nelem = len(elems)
	for ielem in elems:
		nnode = ielem[0]
		for inode in range(0,nnode):
			ndind = ielem[inode+1]
			if(ndmp[ndind-1]!=ndind):
				ielem[inode+1] = ndmp[ndind-1]
		newelem.append(ielem)
	return newelem

def isFourInPlane(nodes,nlist):
	enodes = len(nlist)
	ndcor = []
	for inodes in range(enodes):
		ndcor.append(nodes[nlist[inodes]-1])   # 0 based
	a21 = ndcor[1][0]-ndcor[0][0]
	a22 = ndcor[1][1]-ndcor[0][1]
	a23 = ndcor[1][2]-ndcor[0][2]
	a31 = ndcor[2][0]-ndcor[0][0]
	a32 = ndcor[2][1]-ndcor[0][1]
	a33 = ndcor[2][2]-ndcor[0][2]
	a = a22*a33-a32*a23
	b = a23*a31-a33*a21
	c = a21*a32-a31*a22
	d = -a*ndcor[0][0]-b*ndcor[0][1]-c*ndcor[0][2]
	ret = a*ndcor[3][0]+b*ndcor[3][1]+c*ndcor[3][2]+d
	#print(ret)
	if(abs(ret)<0.5):
		return True
	else:
		return False

def remove_elems(nodes,elems):
	nelem = len(elems)
	etag = [0 for i in range(nelem)]
	for ielem in range(nelem):
		nnode = elems[ielem][0]
		tnode = nnode
		nlist = elems[ielem][1:nnode+1]
		for inode in range(nnode,0,-1):
			ndindi = nlist[inode-1]
			for jnode in range(inode-1,0,-1):
				ndindj = nlist[jnode-1]
				if(ndindi==ndindj):
					tnode-=1
					nlist[inode-1]=-1
					break
		newlist = []
		for inode in nlist:
			if(inode>0):
				newlist.append(inode)
		if(tnode<4): #plane element
			etag[ielem] = 1
		if(tnode==4):  #
			if(isFourInPlane(nodes,newlist)):
				etag[ielem] = 1
			else:
				print(ielem+1)
	newelem = []
	for ielem in range(nelem):
		if(etag[ielem]==0):
			newelem.append(elems[ielem])
	return newelem

def renumber(nodes,elems):
	nnode = len(nodes)
	nelem = len(elems)

	newelem = remove_elems(nodes,elems)

	ntag = [0 for i in range(nnode)]
	for ielem in elems:
		enode = ielem[0]
		for inode in range(enode):
			ndind = ielem[inode+1]
			ntag[ndind-1] = 1

	newnode = []
	ndmp = [0 for i in range(nnode)]
	tnode = 0

	for inode in range(nnode):
		if(ntag[inode]==1):
			tnode +=1
			ndmp[inode] = tnode
			newnode.append(nodes[inode])

	newelem = replace_nodes(elems,ndmp)

	return newnode,newelem

if __name__=='__main__':
	# Open Coordinate File
	nodes = []
	elems = []
	# Read Nodes
	with open('D:\\ShaPai\\02Model\\1.cor','r') as f:
		lines = f.readlines()
		for line in lines:
			data = list(map(float,line.split()))
			nodes.append(data[1:])

	# ReadElems
	with open('D:\\ShaPai\\02Model\\1.ele','r') as f:
		lines = f.readlines()
		for line in lines:
			data = list(map(int,line.split()))
			elems.append(data[1:])


	# Find Nodes of Gaps
	pair = find_closed_nodes(nodes,elems,0.1)
	# Generate New Point Map
	ndmp = gen_map(pair,len(nodes))

	# Map Nodes in Elements
	elems = replace_nodes(elems,ndmp)
	#
	elems = remove_elems(nodes,elems)
	#
	nodes,elems = renumber(nodes,elems)
	progress = ProgressBar()
	print('Writing Files')
	with open('D:\\ShaPai\\02Model\\1.new.cor','w') as f:
		nnode = len(nodes)
		for inode in progress(range(nnode)):
			ndind = inode+1
			coord = nodes[inode]
			f.write(str(ndind)+'\t')
			for icor in coord:
				f.write(str(icor)+'\t')
			f.write('\n')
	progress.finish()
	progress = ProgressBar()
	with open('D:\\ShaPai\\02Model\\1.new.ele','w') as f:
		nelem = len(elems)
		for ielem in progress(range(nelem)):
			eind = ielem+1
			enode = elems[ielem][0]
			f.write(str(eind)+'\t'+str(enode)+'\t')
			for inode in range(enode):
				ndind = elems[ielem][inode+1]
				f.write(str(ndind)+'\t')
			f.write(str(elems[ielem][enode+1])+'\n')
	print('finished')

# coding:utf-8
import numpy as np
from progressbar import *
import networkx as nx
import matplotlib.pyplot as plt
from numba import jit

class Block:
	def __init__(self,index):
		self.index = index
		self.ngroup = 0
		self.grouplist = []
		self.ngap = 0
		self.gaplist  = []
		self.xnode = [0,0]
		self.ynode = [0,0]
		self.znode = [0,0]
		self.xvec = [0,0,0]
		self.yvec = [0,0,0]
		self.zvec = [0,0,0]
	def add_group(self,igroup,adjlist):
		self.grouplist.append(igroup)
		for igroup in adjlist:
			if igroup not in self.gaplist:
				self.gaplist.append(igroup)
	def get_group(self):
		self.grouplist.sort()
		return self.grouplist
	def get_gap(self):
		self.gaplist.sort()
		return self.gaplist
	def get_xnode(self):
		return self.xnode
	def get_ynode(self):
		return self.ynode
	def get_znode(self):
		return self.znode


class Gap:
	def __init__(self,index,igroup):
		self.index = index
		self.group = 0
		self.group = igroup

	def set_group(self,index,igroup):
		self.index = index
		self.group = igroup

	def get_index(self):
		return self.index

	def get_group(self):
		return self.group


class Group:
	def __init__(self, index):
		self.index = index
		self.nelem = 0
		self.elemlist = []
		self.nadj = 0
		self.adjlist = []
		self.isgap = False
		self.nnode = 0
		self.gapid = 0
	def get_elemlist(self):
		return self.elemlist
	def get_nelem(self):
		return self.nelem
	def get_nadj(self):
		return self.nadj
	def get_adjlist(self):
		return self.adjlist
	def add_elem(self,index,ielem):
		if index==self.index:
			ne = 0
			if len(self.elemlist)<0:
				for ie in self.elemlist:
					if ielem != ie:
						ne +=1
				if ne == self.nelem:
					self.nelem+=1
					self.elemlist.append(ielem)
					return self.nelem
			else:
				self.nelem+=1
				self.elemlist.append(ielem)
				return self.nelem
		else:
			return 0
	def add_adjgroup(self,igroup):
		if igroup==self.index-1:
			return 0
		else:
			self.nadj+=1
			self.adjlist.append(igroup)
			return self.nadj
	def get_gapid(self):
		return self.gapid

def get_total_groups(elems):
	group = []
	for elem in elems:
		igroup = elem[-1]
		if len(group)>0:
			n = 0
			for jgroup in group:
				if igroup !=jgroup:
					n +=1
			if n==len(group):
				group.append(igroup)
		else:
			group.append(igroup)
	return len(group)


def sort_elems(elems):
	group = []
	ngroups = get_total_groups(elems)
	for i in range(ngroups):
		group.append(Group(i+1))

	for ie,elem in zip(range(len(elems)),elems):
		igroup = elem[-1]
		group[igroup-1].add_elem(igroup,ie+1)

	ne = 0
	for igroup in group:
		ne += igroup.get_nelem()
	return ne,group

def check_gaps(group,elem,igap,gleft,gright):
	nnodes = 0
	for ielem in elem:
		nlist = ielem[:-1]
		maxnode = max(nlist)
		nnodes = max(maxnode,nnodes)

	gaplnode = np.zeros(nnodes)
	gaprnode = np.zeros(nnodes)
	leftnode = np.zeros(nnodes)
	rightnode = np.zeros(nnodes)

	ngelist = group[igap-1].get_elemlist()

	for ie in ngelist:
		nlist = elem[ie-1][:-1]
		if len(nlist)%2==0:
			half = int(len(nlist)/2)
			for inode in nlist[:half]:
				gaplnode[inode-1]=1
			for inode in nlist[half:]:
				gaprnode[inode-1]=1
		else:
			print("error")

	if np.dot(gaplnode,gaprnode)==0:
		print(sum(gaplnode),sum(gaprnode))
	else:
		print("error")

	for ig in gleft:
		nblist = group[ig-1].get_elemlist()
		for ie in nblist:
			nlist = elem[ie-1][:-1]
			for inode in nlist:
				leftnode[inode-1]=1

	for ig in gright:
		nblist = group[ig-1].get_elemlist()
		for ie in nblist:
			nlist = elem[ie-1][:-1]
			for inode in nlist:
				rightnode[inode-1]=1

	if np.dot(leftnode,rightnode)==0:
		pass
	else:
		print("error")

	multi1 = np.dot(gaplnode,leftnode)
	multi2 = np.dot(gaplnode,rightnode)
	multi3 = np.dot(gaprnode,leftnode)
	multi4 = np.dot(gaprnode,rightnode)


	if (multi1==multi3 or multi1==multi4) and (multi2==multi3 or multi2==multi4):
		return 0
	else:
		for index,in1,in2 in zip(range(nnodes),gaprnode,leftnode):
			if in1*in2 !=0:
				print(index+1,in1,in2)


		print(multi1,multi2,multi3,multi4)

def find_adjacent_group(group,elems):
	nnodes = 0
	for ielem in elems:
		nlist = ielem[:-1]
		maxnode = max(nlist)
		nnodes = max(maxnode,nnodes)

	curgnode = np.zeros(nnodes)
	targnode = np.zeros(nnodes)

	ngroup = len(group)

	print("Find adjacent group:")
	pgb = ProgressBar()
	for igroup in pgb(range(ngroup)):
		curgnode = np.zeros(nnodes)
		ngelist = group[igroup].get_elemlist()
		for ie in ngelist:
			nlist = elems[ie-1][:-1]
			for inode in nlist:
				curgnode[inode-1] = 1
		# print(igroup,sum(curgnode))

		for jgroup in range(ngroup):
			targnode = np.zeros(nnodes)
			if igroup != jgroup:
				ngelist = group[jgroup].get_elemlist()
				for ie in ngelist:
					nlist = elems[ie-1][:-1]
					for inode in nlist:
						targnode[inode-1] = 1
				#print(jgroup,sum(targnode))
			if np.dot(curgnode,targnode)!=0:
				group[igroup].add_adjgroup(jgroup)


		# nadj = group[igroup].get_nadj()
		# print(igroup,"->",nadj)
		#print(group[igroup].get_adjlist())
	pgb.finish()

	for igroup in range(ngroup):
		curgnode = np.zeros(nnodes)
		ngelist = group[igroup].get_elemlist()
		for ie in ngelist:
			nlist = elems[ie-1][:-1]
			for inode in nlist:
				curgnode[inode-1] = 1
		targnode = np.zeros(nnodes)
		nadj = group[igroup].get_nadj()
		adjlist = group[igroup].get_adjlist()
		for jgroup in adjlist:
			ngelist = group[jgroup].get_elemlist()
			for ie in ngelist:
				nlist = elems[ie-1][:-1]
				for inode in nlist:
					targnode[inode-1] = 1
		if np.dot(curgnode,targnode)==sum(curgnode):
			group[igroup].isgap = True
			print(igroup)

	# G = nx.Graph()
	# for igroup in range(ngroup):
	# 	nadj = group[igroup].get_nadj()
	# 	adjlist = group[igroup].get_adjlist()
	# 	for iadj in adjlist:
	# 		if iadj>igroup:
	# 			G.add_edge(igroup,iadj)

	# nx.draw_networkx(G)
	# plt.show()

	G_NoEdge = nx.Graph()
	for igroup in range(ngroup):
		if not group[igroup].isgap:
			G_NoEdge.add_node(igroup)
	for igroup in range(ngroup):
		if group[igroup].isgap:
			nadj = group[igroup].get_nadj()
			adjlist = group[igroup].get_adjlist()
			for iadj in adjlist:
				if not group[iadj].isgap:
					for jadj in adjlist:
						if iadj!= jadj:
							if not group[jadj].isgap:
								G_NoEdge.add_edge(iadj,jadj)
	nx.draw_networkx(G_NoEdge)
	plt.show()

def group_node_flag(group,elems,maxnodes,index):
	curgnode = np.zeros(maxnodes)
	ngelist = group[index].get_elemlist()
	for ie in ngelist:
		nlist = elems[ie-1][:-1]
		for inode in nlist:
			curgnode[inode-1] = 1
	return curgnode

def check_block_gaps(group,elems):
	nnodes = 0
	for ielem in elems:
		nlist = ielem[:-1]
		maxnode = max(nlist)
		nnodes = max(maxnode,nnodes)
	ngroup = len(group)

	print("Check gaps:")

	pgb = ProgressBar()
	for igroup in pgb(range(ngroup)):
		if group[igroup].isgap:
			gaplnode = np.zeros(nnodes)
			gaprnode = np.zeros(nnodes)

			ngelist = group[igroup].get_elemlist()
			for ie in ngelist:
				nlist = elems[ie-1][:-1]
				if len(nlist)%2==0:
					half = int(len(nlist)/2)
					for inode in nlist[:half]:
						gaplnode[inode-1]=1
					for inode in nlist[half:]:
						gaprnode[inode-1]=1
				else:
					print("error")

			adjlist = group[igroup].get_adjlist()
			for jgroup in adjlist:
				if group[jgroup].isgap:
					continue
				ngelist = group[jgroup].get_elemlist()
				targnode = np.zeros(nnodes)
				for ie in ngelist:
					nlist = elems[ie-1][:-1]
					for inode in nlist:
						targnode[inode-1] = 1

				multi1 = np.dot(gaplnode,targnode)
				multi2 = np.dot(gaprnode,targnode)
				#print(igroup,jgroup,multi1,multi2)
				if multi1*multi2==0:
					pass
				else:
					group[igroup].isgap = False
					# print("error",igroup,jgroup)
	pgb.finish()

	gap = []
	ngap = 0
	for igroup in range(ngroup):
		if group[igroup].isgap:
			gap.append(Gap(ngap,igroup))
			group[igroup].gapid = ngap
			ngap += 1

	print("Success! Find these gaps:")
	for igap in range(ngap):
		print(gap[igap].get_index(),"<->",gap[igap].get_group()+1)
	# for igroup in range(ngroup):
	# 	if group[igroup].isgap:
	# 		print(igroup+1,end=',')
	print('\n')
	return gap


def build_block(group,elems):
	ngroup = len(group)
	block = []
	nblock = 0
	for igroup in range(ngroup):
		if group[igroup].isgap:
			continue

		nbglist = [igroup]
		adjlist = group[igroup].get_adjlist()
		iso = True
		for jgroup in adjlist:
			if jgroup<igroup:
				if not group[jgroup].isgap:
					iso = False
					mastergroup = jgroup
					nbglist.append(jgroup)
		if iso:
			nblock +=1
			block.append(Block(nblock))
			block[nblock-1].grouplist = [igroup]
			for jgroup in adjlist:
				if group[jgroup].isgap:
					block[nblock-1].gaplist.append(jgroup)
		else:
			for iblock in range(nblock):
				grouplist = block[iblock].grouplist
				for jgroup in grouplist:
					if jgroup == mastergroup:
						adjgap = []
						for iadj in adjlist:
							if group[iadj].isgap:
								adjgap.append(iadj)

						block[iblock].add_group(igroup,adjgap)



	print("block -> adjacent gaps")

	for iblock in block:
		grouplist = iblock.get_group()
		gaplist = iblock.get_gap()
		print(np.add(grouplist,1),'->',np.add(gaplist,1))


	return block

def get_vec(p1,p2):
	vec = np.subtract(p1,p2)
	dist = np.sqrt(np.dot(vec,vec))
	if dist>0:
		vec = np.divide(vec,dist)
	return vec

def find_fix_nodes(block,group,elems,nodes):
	nblock = len(block)

	nnode = len(nodes)


	for iblock in range(nblock):
		gaplist = block[iblock].get_gap()
		grouplist = block[iblock].get_group()

		blocknode = np.zeros(nnode)
		gapnode = np.zeros(nnode)
		for igroup in grouplist:
			nblist = group[igroup].get_elemlist()
			for ie in nblist:
				nlist = elems[ie-1][:-1]
				for inode in nlist:
					blocknode[inode-1]=1

		for igroup in gaplist:
			nblist = group[igroup].get_elemlist()
			for ie in nblist:
				nlist = elems[ie-1][:-1]
				for inode in nlist:
					gapnode[inode-1]=1
		#print(sum(blocknode),sum(gapnode))

		# Find inner node
		for inode in range(nnode):
			if blocknode[inode]*gapnode[inode]==1:
				blocknode[inode]=0

		#print("number of inner points in ",iblock,"is ", sum(blocknode))
		if len(nodes[0])==2:
			z = 0.0
			for inode in range(nnode):
				if blocknode[inode]>0:
					coord = nodes[inode]
					x,y = coord
					bandx = {"min":x,"max":x,"minpoint":inode,"maxpoint":inode}
					bandy = {"min":y,"max":y,"minpoint":inode,"maxpoint":inode}
					bandz = {"min":z,"max":z,"minpoint":inode,"maxpoint":inode}
					break
		else:
			for inode in range(nnode):
				if blocknode[inode]>0:
					coord = nodes[inode]
					x,y,z = coord
					bandx = {"min":x,"max":x,"minpoint":inode,"maxpoint":inode}
					bandy = {"min":y,"max":y,"minpoint":inode,"maxpoint":inode}
					bandz = {"min":z,"max":z,"minpoint":inode,"maxpoint":inode}
					break

		nodelist = []
		if len(nodes[0])==2:
			z = 0.0
			for inode in range(nnode):
				if blocknode[inode]>0:
					nodelist.append(inode)
					coord = nodes[inode]
					x,y = coord
					if x<bandx['min']:
						bandx['min']=x
						bandx['minpoint']=inode
					if x>bandx['max']:
						bandx['max']=x
						bandx['maxpoint']=inode
					if y<bandy['min']:
						bandy['min']=y
						bandy['minpoint']=inode
					if y>bandy['max']:
						bandy['max']=y
						bandy['maxpoint']=inode
					if z<bandz['min']:
						bandz['min']=z
						bandz['minpoint']=inode
					if z>bandz['max']:
						bandz['max']=z
						bandz['maxpoint']=inode
		else:
			for inode in range(nnode):
				if blocknode[inode]>0:
					nodelist.append(inode)
					coord = nodes[inode]
					x,y,z = coord
					if x<bandx['min']:
						bandx['min']=x
						bandx['minpoint']=inode
					if x>bandx['max']:
						bandx['max']=x
						bandx['maxpoint']=inode
					if y<bandy['min']:
						bandy['min']=y
						bandy['minpoint']=inode
					if y>bandy['max']:
						bandy['max']=y
						bandy['maxpoint']=inode
					if z<bandz['min']:
						bandz['min']=z
						bandz['minpoint']=inode
					if z>bandz['max']:
						bandz['max']=z
						bandz['maxpoint']=inode

		print(iblock,len(nodelist))
		vecx = [1,0,0]
		vecy = [0,1,0]
		vecz = [0,0,1]

		threshold = 0.0
		vecxmin = [threshold,0,0]
		vecymin = [0,threshold,0]
		veczmin = [0,0,threshold]
		vecxp = [0,0]
		vecyp = [0,0]
		veczp = [0,0]

		if len(nodelist)>10000:
			continue

		pgb = ProgressBar()
		for inode in pgb(range(len(nodelist))):
			point1 = nodes[nodelist[inode]]
			for jnode in range(inode+1,len(nodelist)):
					point2 = nodes[nodelist[jnode]]
					tvec = get_vec(point1,point2)
					if abs(np.dot(tvec,vecx))>abs(np.dot(vecxmin,vecx)):
						vecxmin = tvec
						vecxp = [nodelist[inode],nodelist[jnode]]
					if abs(np.dot(tvec,vecy))>abs(np.dot(vecymin,vecy)):
						vecymin = tvec
						vecyp = [nodelist[inode],nodelist[jnode]]
					if abs(np.dot(tvec,vecz))>abs(np.dot(veczmin,vecz)):
						veczmin = tvec
						veczp = [nodelist[inode],nodelist[jnode]]

					#vec.append([get_vec(point1,point2),inode,jnode])
		pgb.finish()
		print(vecxmin,vecxp)
		print(vecymin,vecyp)
		print(veczmin,veczp)

		block[iblock].xnode = vecxp
		block[iblock].xvec = vecxmin
		block[iblock].ynode = vecyp
		block[iblock].yvec = vecymin
		block[iblock].znode = veczp
		block[iblock].zvec = veczmin

	return 0

if __name__ == '__main__':

	# path = 'D:\\HSTAR_Q\\HSTAR_Q\\Example\\Gravity3D\\4SInGroup'
	# path='D:\\ShaPai\\NewModel\\09StaticAllGapStep'
	# path = 'D:\\ShaPai\\NewModel\\13StaticAllGapStep'
	# path = 'C:\\Users\\qhjun\\Desktop\\1.0'

	path = sys.argv[1]

	nodes = []
	# Read Nodes
	# D:\\ShaPai\\NewModel\\09StaticAllGapStep\\1.cor

	with open(path+'\\1.cor','r') as f:
		lines = f.readlines()
		for line in lines:
			data = list(map(float,line.split()))
			nodes.append(data[1:])

	elems = []
	# ReadElems
	with open(path+'\\1.ele','r') as f:
		lines = f.readlines()
		for line in lines:
			data = list(map(int,line.split()))
			elems.append(data[1:])

	nelem,group = sort_elems(elems)

	find_adjacent_group(group,elems)

	gap = check_block_gaps(group,elems)

	block = build_block(group,elems)

	find_fix_nodes(block,group,elems,nodes)

	with open(path+'\\1.block','w') as f:
		for igap in range(len(gap)):
			f.write('ngroupt,xlwmd(1:ndimn),frict_less,goodman,thin_layer/listgropt/gap0,statei/ft0/frict/cohes\n')
			f.write(str(len(gap))+' 0	0	0	0	0	0\n')
			for jgap in range(len(gap)):
				if igap==jgap:
					coef = 1
					igroup = gap[jgap].group+1
					igroup *= coef
					f.write(str(igroup)+' ')
				else:
					coef = -1
			f.write('\n')
			f.write('0	1	\n')
			f.write('100*5.00E+10	5.00E+10\n')
			f.write('100*1	1	\n')
			f.write('100*5.00E+10	5.00E+10\n')
			f.write('1	1.00E-08	1.00E-10	1.00E-10	1.00E-05	1.00E-10	1.00E-10\n')

		for iblock in range(len(block)):
			gaplist = block[iblock].get_gap()
			grouplist = block[iblock].get_group()
			f.write('ngrout,ngropb  nrdof eblock is_cs 		\n')
			f.write(str(len(gaplist))+'	'+str(len(grouplist))+'		6	1	0\n')
			f.write('1	1	1	1	1	1\n')
			for igap in gaplist:
				jgap = group[igap].get_gapid()
				f.write(str(jgap+1)+'	')
			f.write('\n')
			for igroup in grouplist:
				f.write(str(igroup+1)+'	')
			f.write('\n')

		f.write('x-prescribe\n')
		for iblock in range(len(block)):
			xnode = block[iblock].get_znode()
			for inode in xnode:
				f.write(str(inode+1)+'	')
			f.write('\n')
		f.write('y-prescribe\n')
		for iblock in range(len(block)):
			ynode = block[iblock].get_xnode()
			for inode in ynode:
				f.write(str(inode+1)+'	')
			f.write('\n')
		f.write('z-prescribe\n')
		for iblock in range(len(block)):
			znode = block[iblock].get_ynode()
			for inode in znode:
				f.write(str(inode+1)+'	')
			f.write('\n')



	# build_topology_structure(elems)
	# for i in range(10):
	# 	print("Please Input the Gaps Group Number:")
	# 	igap = int(input())
	# 	print("Please Input the Left Group Number:")
	# 	gleft = list(map(int,input().split()))
	# 	print("Please Input the Right Group Number:")
	# 	gright = list(map(int,input().split()))
	# 	check_gaps(group,elems,igap,gleft,gright)

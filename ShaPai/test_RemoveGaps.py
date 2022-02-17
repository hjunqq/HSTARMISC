# -*- coding: utf-8 -*-

import unittest

from RemoveGaps import *

class TestFunc(unittest.TestCase):
	
	def test_isFourInPlane(self):
		nodes = [[0.0,0.0,0.0],
		[0.0,1.0,0.0],
		[1.0,0.0,0.0],
		[1.0,1.0,0.0]]
		nlist = [1,2,3,4]
		self.assertTrue(isFourInPlane(nodes,nlist))
		nodes = [[0.0,0.0,0.0],
		[0.0,1.0,0.0],
		[1.0,0.0,0.0],
		[1.0,1.0,1.0]]
		self.assertFalse(isFourInPlane(nodes,nlist))

	def test_remove_elems(self):
		#nodes = [[0.0,0.0,0.0],
		#[0.0,1.0,0.0],
		#[1.0,0.0,0.0],
		#[1.0,1.0,0.0],
		#[0.0,0.0,1.0],
		#[0.0,1.0,1.0],
		#[1.0,0.0,1.0],
		#[1.0,1.0,1.0]]
		elems = [
			[8,45490,51753,45490,45490,45245,10663,45245,45245]]
		newelem = [] 
		nodes = []
		with open('D:\\ShaPai\\02Model\\1.cor','r') as f:
			lines = f.readlines()
			for line in lines:
				data = list(map(float,line.split()))
				nodes.append(data[1:])

		self.assertEqual(newelem,remove_elems(nodes,elems))

	def test_replace_nodes(self):
		elems = [
			[8,1,2,3,4,5,6,7,8],
		]
		ndmp = [8,7,6,10,5,1,4,3,11]
		newelem = [
			[8,8,7,6,10,5,1,4,3],
		]
		self.assertEqual(newelem,replace_nodes(elems,ndmp))

	def test_renumber(self):
		nodes = [[0.0,0.0,2.0],
		[0.0,1.0,2.0],
		[1.0,0.0,2.0],
		[1.0,1.0,2.0],
		[0.0,0.0,3.0],
		[0.0,1.0,3.0],
		[1.0,0.0,3.0],
		[1.0,1.0,3.0],
		[0.0,0.0,0.0],
		[0.0,1.0,0.0],
		[1.0,0.0,0.0],
		[1.0,1.0,0.0],
		[0.0,0.0,1.0],
		[0.0,1.0,1.0],
		[1.0,0.0,1.0],
		[1.0,1.0,1.0],
		]
		elems = [
			[8,9,10,11,12,5,6,7,8]
		] 
		newnode = [[0.0,0.0,3.0],
		[0.0,1.0,3.0],
		[1.0,0.0,3.0],
		[1.0,1.0,3.0],
		[0.0,0.0,0.0],
		[0.0,1.0,0.0],
		[1.0,0.0,0.0],
		[1.0,1.0,0.0]]
		newelem = [
			[8,5,6,7,8,1,2,3,4]
		]
		self.assertEqual(newnode,renumber(nodes,elems)[0])
		self.assertEqual(newelem,renumber(nodes,elems)[1])


if __name__=='__main__':
	unittest.main()
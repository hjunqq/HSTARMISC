import unittest

from CheckGaps import *

class Test_test_CheckGaps(unittest.TestCase):
	def test_get_total_groups(self):
		elems=[
			[8,1,2,3,4,5,6,7,8,1],
			[8,1,2,3,4,5,6,7,8,2],
			[8,1,2,3,4,5,6,7,8,3],
			[8,1,2,3,4,5,6,7,8,2]
			]
		self.assertEqual(3,get_total_groups(elems))
	def test_Group(self):
		g = Group(1)
		g.add_elem(1,10)
		g.add_elem(2,10)
		self.assertEqual(1,g.get_nelem())

	def test_sort_elems(self):
		elems=[
			[8,1,2,3,4,5,6,7,8,1],
			[8,1,2,3,4,5,6,7,8,2],
			[8,1,2,3,4,5,6,7,8,3],
			[8,1,2,3,4,5,6,7,8,2]
			]
		self.assertEqual(4,sort_elems(elems))

if __name__ == '__main__':
	unittest.main()

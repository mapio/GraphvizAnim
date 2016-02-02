import unittest

from gvanim.animation import Step
import gvanim.action as ga

class TestActions( unittest.TestCase ):
	def setUp(self):
		self.steps = [ Step() ]

	def tearDown( self ):
		self.steps = None

	def test_remove_unlabeled_node( self ):
		ga.RemoveNode( 0 )( self.steps )

	def test_unlabel_unexistent_node( self ):
		ga.UnlabelNode( 0 )( self.steps )

if __name__ == '__main__':
	unittest.main()

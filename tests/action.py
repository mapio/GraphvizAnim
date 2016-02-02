# Copyright 2016, Massimo Santini <santini@di.unimi.it>
#
# This file is part of "GraphvizAnim".
#
# "GraphvizAnim" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# "GraphvizAnim" is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# "GraphvizAnim". If not, see <http://www.gnu.org/licenses/>.

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

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

from __future__ import absolute_import

from argparse import ArgumentParser, FileType
from sys import stdin

from gvanim import Animation, render, gif

def main():

	parser = ArgumentParser( prog = 'gvanim' )
	parser.add_argument( 'animation', nargs = '?', type = FileType( 'r' ), default = stdin, help = 'The file containing animation commands (default: stdin)' )
	parser.add_argument( '--delay', '-d', default = '100', help = 'The delay (in ticks per second, default: 100)' )
	parser.add_argument( 'basename', help = 'The basename of the generated file' )
	args = parser.parse_args()

	ga = Animation()
	ga.parse( args.animation )
	gif( render( ga.graphs(), args.basename, 'png' ), args.basename, args.delay )

if __name__ == '__main__':
	main()

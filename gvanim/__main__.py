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

from argparse import ArgumentParser, FileType
from sys import stdin, argv, stderr

import animation, render

def main():

	parser = ArgumentParser( prog = 'gvanim' )
	parser.add_argument( 'animation', nargs = '?', type = FileType( 'r' ), default = stdin, help = 'The file containing animation commands (default: stdin)' )
	parser.add_argument( '--delay', '-d', default = '100', help = 'The delay (in ticks per second, default: 100)' )
	parser.add_argument( 'basename', help = 'The basename of the generated file' )
	args = parser.parse_args()

	ga = animation.Animation()
	cmd2method = {
		'ns' : ga.next_step,
		'an' : ga.add_node,
		'hn' : ga.highlight_node,
		'ln' : ga.label_node,
		'un' : ga.unlabel_node,
		'rn' : ga.remove_node,
		'ae' : ga.add_edge,
		'he' : ga.highlight_edge,
		're' : ga.remove_edge,
	}

	for line in args.animation:
		parts = line.strip().split()
		cmd, params = parts[ 0 ], parts[ 1: ]
		try:
			cmd2method[ cmd ]( *params )
		except KeyError:
			print >>stderr, 'gvanim: unrecognized command: {}'.format( cmd )
			return
		except TypeError:
			print >>stderr, 'gvanim: wrong number of parameters: {}'.format( line.strip() )
			return

	render.to_gif( render.render( ga.graphs(), args.basename, 'png' ), args.basename, args.delay )

if __name__ == '__main__':
	main()

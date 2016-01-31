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

from sys import stdin, argv

import animation, render


if len( argv ) != 2:
	dest = 'dest'
else:
	dest = argv[ 1 ]

ga = animation.Animation()

cmd2method = {
	'ns' : ga.next_step,
	'an' : ga.add_node,
	'hn' : ga.highlight_node,
	'rn' : ga.remove_node,
	'ae' : ga.add_edge,
	'he' : ga.highlight_edge,
	're' : ga.remove_edge,
}

for line in stdin:
	parts = line.strip().split()
	cmd, params = parts[ 0 ], parts[ 1: ]
	cmd2method[ cmd ]( *params )

render.to_gif( render.render( ga.to_graphs(), dest, 'png' ), dest, 50 )

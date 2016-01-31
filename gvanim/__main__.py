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

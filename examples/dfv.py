from random import sample

from gvanim import Animation, render, to_gif

N = range( 6 )
K = 3

G = dict( ( v, sample( N, K ) ) for v in N )

ga = Animation()
for v, adj in G.items():
    for u in adj:
        ga.add_edge( v, u )
ga.next_step()

seen = [ False for v in  N ]
def dfv( v ):
    ga.highlight_node( v )
    ga.next_step()
    seen[ v ] = True
    for u in G[ v ]:
        if not seen[ u ]:
            ga.highlight_node( v )
            ga.highlight_edge( v, u )
            ga.next_step()
            dfv( u )

dfv( 0 )

graphs = ga.to_graphs()
files = render( graphs, 'dfv', 'png' )
to_gif( files, 'dfv', 50 )

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

from random import sample
from gvanim import Animation, render, gif

# Create a sample graph
N = range(6)
K = 3

G = dict((v, sample(N, K)) for v in N)

# Initialize the animation object
ga = Animation()
# For every node in the graph go through the neighbouring nodes
for v, adj in G.items():
    for u in adj:
        # Add a "add egdge" animation step
        ga.add_edge(v, u)
ga.next_step()

# No node has been visited so far
seen = [False for v in N]


def dfv(v):
    """
    Go through all the adjacent nodes to vertex v in graph G
    For that modifies in place the animation object 'ga'

    Parameters
    ----------
    v:
        node key (in the graph dict)
    """
    # Highlight current node
    ga.highlight_node(v)
    # Next step
    ga.next_step()
    # Current node has been seen
    seen[v] = True
    # For all the adjacent nodes that have not yet been visited
    for u in G[v]:
        if not seen[u]:
            # Highlight it
            ga.highlight_node(v)
            # as well as the edge connecting current node to it
            ga.highlight_edge(v, u)
            ga.next_step()
            # Recursively go through all the nodes
            # (if they are all connected...)
            dfv(u)

# Highlight graph construction process
dfv(0)

# Get the animation object graphs (one per 'step')
graphs = ga.graphs  # For pygraphviz replace by .py_graphs()
# Render those graphs to png files through `dot`
files = render(graphs, 'dfv', 'png')  # add size=20., layout='dot'
# Make a gif out of those files
gif(files, 'dfv', 50)

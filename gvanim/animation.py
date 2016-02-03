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

from email.utils import quote
import shlex
import action
import pygraphviz as pgv

class ParseException(Exception):
    pass


class Step(object):
    def __init__(self, step=None):
        # If step is not None we are building upon the previous step,
        # otherwise we clean up by removing all nodes and edges
        if step:
            self.V = step.V.copy()
            self.E = step.E.copy()
            self.L = step.L.copy()
        else:
            self.V = set()
            self.E = set()
            self.L = dict()
        # Highlights are all gone
        self.hV = set()
        self.hE = set()

    def node_format(self, v):
        """
        Format a given node according to the lists of highlighted nodes,
        and labels which can be updated by :py:class:`action`

        Parameters
        ----------
        v:
            Node key

        Returns
        -------
        str
            String describing the node in dot format
        """
        fmt = []
        try:
            fmt.append('label="{}"'.format(self.L[v]))
        except KeyError:
            pass
        if v in self.hV:
            fmt.append('color=red')
        elif v not in self.V:
            fmt.append('style=invis')
        if fmt:
            return '[{}]'.format(','.join(fmt))
        return ''

    def edge_format(self, e):
        """
        See :py:func:`node_format`
        Parameters
        ----------
        e:
            Edge key

        Returns
        -------
        str
        """
        if e in self.hE:
            return '[color=red]'
        elif e in self.E:
            return ''
        return '[style=invis]'

    def __repr__(self):
        return '{{ V = {}, E = {}, hV = {}, hE = {}, L = {} }}'.format(self.V,
                                                                       self.E,
                                                                       self.hV,
                                                                       self.hE,
                                                                       self.L)


class Animation(object):
    """
    Class describing the animation of a graph. In contains a list of actions
    (stored in self._actions) that are instructions on how to build the graph
    (adding nodes, edges, highlighting them...)
    See :py:class:action for more details
    """
    def __init__(self):
        self._actions = []

    def next_step(self, clean=False):
        self._actions.append(action.NextStep(clean))

    def add_node(self, v):
        self._actions.append(action.AddNode(v))

    def highlight_node(self, v):
        self._actions.append(action.HighlightNode(v))

    def label_node(self, v, label):
        self._actions.append(action.LabelNode(v, label))

    def unlabel_node(self, v):
        self._actions.append(action.UnlabelNode(v))

    def remove_node(self, v):
        self._actions.append(action.RemoveNode(v))

    def add_edge(self, u, v):
        self._actions.append(action.AddEdge(u, v))

    def highlight_edge(self, u, v):
        self._actions.append(action.HighlightEdge(u, v))

    def remove_edge(self, u, v):
        self._actions.append(action.RemoveEdge(u, v))

    def parse(self, lines):
        action2method = {
            'ns': self.next_step,
            'an': self.add_node,
            'hn': self.highlight_node,
            'ln': self.label_node,
            'un': self.unlabel_node,
            'rn': self.remove_node,
            'ae': self.add_edge,
            'he': self.highlight_edge,
            're': self.remove_edge,
        }
        for line in lines:
            parts = shlex.split(line.strip(), True)
            if not parts:
                continue
            act, params = parts[0], parts[1:]
            try:
                action2method[act](*params)
            except KeyError:
                raise ParseException('unrecognized command: {}'.format(act))
            except TypeError:
                raise ParseException(
                    'wrong number of parameters: {}'.format(line.strip()))
                return

    @property
    def steps(self):
        steps = [Step()]
        for act in self._actions:
            act(steps)
        return steps

    @property
    def edges_nodes(self):
        """
        Get all the edges and nodes encountered in all the steps
        At the same time get all the steps (for free, as we need them to get
        nodes and edges anyway)

        Returns
        -------
        steps:
        E:
        V:
        """
        steps = self.steps
        # Get all the vertices and edges that we will encounter in those graphs
        V, E = set(), set()
        for step in steps:
            V |= step.V
            E |= step.E

        return steps, E, V

    @property
    def graphs(self):
        """
        Create dot format graphs from the current :class:`Animation` object.
        Each graph in the list of graphs that is returned is the state of the
        graph during one frame of the animation

        Returns
        -------
        graphs: list of str
        """
        # Get a list of all the steps. Each step contains a list of all
        # current nodes, edges as well as highlighted edges and nodes. Those
        # are animation steps
        # Get also all nodes and vertices
        steps, E, V = self.edges_nodes
        # Go through all the steps
        graphs = []
        for n, s in enumerate(steps):
            # New graph for the current animation frame
            graph = ['digraph G {']
            # Add all the nodes in their dot format
            for v in V:
                graph.append('"{}" {};'.format(quote(str(v)), s.node_format(v)))
            # Add all the edges, described in dot format
            for e in E:
                graph.append('"{}" -> "{}" {};'.format(quote(str(e[0])),
                                                       quote(str(e[1])),
                                                       s.edge_format(e)))
            graph.append('}')
            # Add this graph to the list of all graphs
            graphs.append('\n'.join(graph))
        return graphs

    def py_graphs(self, **kwargs):
        """
        Create pygraphviz graphs from the  current :class:`Animation` object.

        Returns
        -------
        py_graphs: list of Graphviz graphs

        Keyword arguments
        -----------------
        directed: bool
            Is the graph directed or not?
            See :py:class:`pygraph.AGraph` for details
        strict: bool
            Parallel edges or self loop allowed?
            See :py:class:`pygraph.AGraph` for details
        """

        # Optional graph properties
        directed = kwargs.get('directed', True)
        strict = kwargs.get('strict', False)
        # Get all steps, edges and nodes
        steps, E, V = self.edges_nodes
        py_graphs = []
        for n, s in enumerate(steps):
            # Initialize a new graph
            graph = pgv.AGraph(strict=strict, directed=directed)
            # Note: We are node handling the 'invis' case as in the
            # node_format of edge_format method of the Step class but it
            # should not happen as we get our edges and nodes from the steps
            # For every node
            for v in V:
                if v in s.hV:
                    color = 'red'
                else:
                    color = 'black'
                graph.add_node(str(v), color=color)
            # For every edge
            for e in E:
                if e in s.hE:
                    color = 'red'
                else:
                    color = 'black'
                graph.add_edge(e, color=color)
            py_graphs.append(graph)
        return py_graphs

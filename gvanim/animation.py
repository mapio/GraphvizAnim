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

import action

class Step( object ):

	def __init__( self, step = None ):
		if step:
			self.V = step.V.copy()
			self.E = step.E.copy()
		else:
			self.V = set()
			self.E = set()
		self.hV = set()
		self.hE = set()

	def node_format( self, v ):
		if v in self.hV:
			return '[color=red]'
		elif v in self.V:
			return ''
		return '[style=invis]'

	def edge_format( self, e ):
		if e in self.hE:
			return '[color=red]'
		elif e in self.E:
			return ''
		return '[style=invis]'

	def __repr__( self ):
		return '{{ V = {}, E = {}, hV = {}, hE = {} }}'.format( self.V, self.E, self.hV, self.hE )

class Animation( object ):

	def __init__( self ):
		self._actions = []

	def next_step( self, clean = False ):
		self._actions.append( action.NextStep( clean ) )

	def add_node( self, v ):
		self._actions.append( action.AddNode( v ) )

	def highlight_node( self, v ):
		self._actions.append( action.HighlightNode( v ) )

	def remove_node( self, v ):
		self._actions.append( action.RemoveNode( v ) )

	def add_edge( self, u, v ):
		self._actions.append( action.AddEdge( u, v ) )

	def highlight_edge( self, u, v ):
		self._actions.append( action.HighlightEdge( u, v ) )

	def remove_edge( self, u, v ):
		self._actions.append( action.RemoveEdge( u, v ) )

	def to_graphs( self ):
		graphs = []
		steps = [ Step() ]
		V, E = set(), set()
		for action in self._actions:
			action( steps )
			V |= steps[ -1 ].V
			E |= steps[ -1 ].E
		for n, s in enumerate( steps ):
			graph = [ 'digraph G {' ]
			for v in V: graph.append( '{} {};'.format( v, s.node_format( v ) ) )
			for e in E: graph.append( '{}->{} {};'.format( e[0], e[1], s.edge_format( e ) ) )
			graph.append( '}' )
			graphs.append( '\n'.join( graph ) )
		return graphs

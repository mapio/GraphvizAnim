import pygraphviz as pgv


def _py_render( params ) :
	"""
	Render PyGraphViz graphs

	Parameters
	----------
	params: tuple
		Path, format, size, layout and graph to output
		size: float
			Size in inches
		layout: str
			The kind of layout we want to use.
			['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
			Defaults to neato
			See :py:func:`pygraphviz.AGraph.layout` for details
	Returns
	-------
	path: str
		Path to the newly created file
	"""
	# FIXME: PyGraphviz layout is not stable so we are not guaranteed
	# to get similar layouts every time
	path , fmt , size , layout , graph = params
	print path
	graph.graph_attr.update( size=size )
	graph.draw( path , format=fmt , prog=layout )
	return path


def render( graphs , basename , fmt='png' , size=320 , layout='neato' ) :
	# FIXME: Could not get the Pool to work with pygraphviz graphs
	return map( _py_render , [( '{}_{:03}.{}'.format( basename , n , fmt )  ,
				fmt , size , layout , graph )
				for n , graph in enumerate( graphs ) ] )


def get_py_graphs( anim , **kwargs ) :
	"""
	Create pygraphviz graphs from the  current :class:`Animation` object.

	Parameters
	----------
	anim: :py:class:Animation object
		Which anim object to transform into pygraphviz graphs

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
	directed = kwargs.get( 'directed' , True )
	strict = kwargs.get( 'strict' , False )
	# Get all steps , edges and nodes
	steps , E , V = anim.edges_nodes
	py_graphs = []
	for n , s in enumerate( steps ) :
		# Initialize a new graph
		graph = pgv.AGraph( strict=strict , directed=directed )
		# Note: We are node handling the 'invis' case as in the
		# node_format of edge_format method of the Step class but it
		# should not happen as we get our edges and nodes from the steps
		# For every node
		for v in V:
			if v in s.hV:
				color = 'red'
			else:
				color = 'black'
			graph.add_node( str( v )  , color=color )
		# For every edge
		for e in E:
			if e in s.hE:
				color = 'red'
			else:
				color = 'black'
			graph.add_edge( e , color=color )
		py_graphs.append( graph )
	return py_graphs

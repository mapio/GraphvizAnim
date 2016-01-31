import animation

class NextStep( object ):
	def __init__( self, clean = False ):
		self.clean = clean
	def __call__( self, steps ):
		steps.append( animation.Step( None if self.clean else steps[ -1 ] ) )

class AddNode( object ):
	def __init__( self, v ):
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].V.add( self.v )

class HighlightNode( object ):
	def __init__( self, v ):
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].V.add( self.v )
		steps[ -1 ].hV.add( self.v )

class RemoveNode( object ):
	def __init__( self, v ):
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].V.discard( self.v )
		steps[ -1 ].hV.discard( self.v )
		dE = set( e for e in steps[ -1 ].E if self.v in e )
		steps[ -1 ].E -= dE
		steps[ -1 ].hE -= dE

class AddEdge( object ):
	def __init__( self, u, v ):
		self.u = u
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].V.add( self.u )
		steps[ -1 ].V.add( self.v )
		steps[ -1 ].E.add( ( self.u, self.v ) )

class HighlightEdge( object ):
	def __init__( self, u, v ):
		self.u = u
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].V.add( self.u )
		steps[ -1 ].V.add( self.v )
		steps[ -1 ].E.add( ( self.u, self.v ) )
		steps[ -1 ].hE.add( ( self.u, self.v ) )

class RemoveEdge( object ):
	def __init__( self, u, v ):
		self.u = u
		self.v = v
	def __call__( self, steps ):
		steps[ -1 ].E.discard( ( self.u, self.v ) )
		steps[ -1 ].hE.discard( ( self.u, self.v ) )


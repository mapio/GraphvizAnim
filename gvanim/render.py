from subprocess import Popen, PIPE, STDOUT, call

def render( graphs, basename, fmt ):
	files = []
	for n, graph in enumerate( graphs ):
		file = '{}_{:03}.{}'.format( basename, n, fmt )
		with open( file , 'w' ) as out:
 			pipe = Popen( [ 'dot', '-T', fmt ], stdout = out, stdin = PIPE, stderr = None )
			pipe.communicate( input = graph )
			pass
		files.append( file )
	return files

def to_gif( files, basename, delay = 10 ):
	cmd = [ 'convert' ]
	for file in files:
		cmd.extend( ( '-delay', str( delay ), file ) )
	cmd.append( basename + '.gif' )
	call( cmd )

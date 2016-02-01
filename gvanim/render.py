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

from subprocess import Popen, PIPE, STDOUT, call

def render( graphs, basename, fmt ):
	files = []
	for n, graph in enumerate( graphs ):
		file = '{}_{:03}.{}'.format( basename, n, fmt )
		with open( file , 'w' ) as out:
 			pipe = Popen( [ 'dot', '-T', fmt ], stdout = out, stdin = PIPE, stderr = None )
			pipe.communicate( input = graph )
		files.append( file )
	return files

def gif( files, basename, delay = 10 ):
	cmd = [ 'convert' ]
	for file in files:
		cmd.extend( ( '-delay', str( delay ), file ) )
	cmd.append( basename + '.gif' )
	call( cmd )

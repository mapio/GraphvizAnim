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

from __future__ import absolute_import

from os.path import join
from tempfile import mkdtemp
from shutil import rmtree

from IPython.display import Image
import ipywidgets as widgets

from gvanim import render

def interactive( animation, size = 320 ):
	basedir = mkdtemp()
	basename = join( basedir, 'graph' )
	steps = [ Image( path ) for path in render( animation.graphs(), basename, 'png', size ) ]
	rmtree( basedir )
	slider = widgets.IntSlider( min = 0, max = len( steps ) - 1, step = 1, value = 0 )
	return widgets.interactive( lambda n: steps[ n ], n = slider )

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

from subprocess import Popen, PIPE, call
from multiprocessing import Pool, cpu_count


def _render(params):
    """
    Render dot graphs as images

    Parameters
    ----------
    params: tuple
        Path, format, size and graph to output

    Returns
    -------
    path: str
        Path to the newly created file
    """
    path, fmt, size, graph = params
    print path
    with open(path, 'w') as out:
        pipe = Popen(['dot', '-Gsize=1,1!', '-Gdpi={}'.format(size), '-T', fmt],
                     stdout=out, stdin=PIPE, stderr=None)
        pipe.communicate(input=graph)
    return path


def _py_render(params):
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
    # FIXME: PyGrpahviz layout is not stable so we are not guaranteed
    # to get similar layouts every time
    path, fmt, size, layout, graph = params
    print path
    graph.graph_attr.update(size=size)
    graph.draw(path, format=fmt, prog=layout)
    return path


def render(graphs, basename, fmt='png', size=320, layout='neato'):
    if isinstance(graphs[0], str):
        # We have a dot format graph
        try:
            _map = Pool(processes=cpu_count()).map
        except NotImplementedError:
            _map = map
        return _map(_render,
                    [('{}_{:03}.{}'.format(basename, n, fmt), fmt, size, graph)
                     for n, graph in enumerate(graphs)])
    else:
        # We hope we get a pygraphviz graph
        # FIXME: Could not get the Pool to work with pygraphviz graphs
        return map(_py_render,
                    [('{}_{:03}.{}'.format(basename, n, fmt),
                      fmt, size, layout, graph)
                     for n, graph in enumerate(graphs)])


def gif(files, basename, delay=100):
    cmd = ['convert']
    for f in files:
        cmd.extend(('-delay', str(delay), f))
    cmd.append(basename + '.gif')
    call(cmd)

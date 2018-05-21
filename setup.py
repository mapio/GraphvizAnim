from distutils.core import setup

def read( path ):
	with open( path, 'r' ) as f:
		return f.read()

setup(
	name = 'GraphvizAnim',
	version = '1.0.1',
	description = 'A tool to create animated graph visualizations, based on graphviz',
	long_description = read( 'README.md' ),
	long_description_content_type='text/markdown',
	author = 'Massimo Santini',
	author_email = 'santini@di.unimi.it',
	url = 'https://github.com/mapio/GraphvizAnim',
	license = 'GNU/GPLv3',
	packages = [ 'gvanim' ],
	keywords = 'drawing graph animation',
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: Unix',
		'Topic :: Software Development :: Libraries :: Python Modules'
	]
)

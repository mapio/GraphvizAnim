/*
 * Copyright 2016, Massimo Santini <santini@di.unimi.it>
 *
 * This file is part of "GraphvizAnim".
 *
 * "GraphvizAnim" is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 *
 * "GraphvizAnim" is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * "GraphvizAnim". If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main( void )
{
	int i, j, n = 10, g;
	double p = 0.1;

	srand( time( NULL ) );

	for ( i = 0; i < n; i++ ) {
		printf( "hn %d\nns\n", i );
		for ( j = 0; j < n; j++ )
			if ( random() < p * RAND_MAX )
				printf( "hn %d\nhe %d %d\nns\n", i, i, j );
	}

	return 0;
}

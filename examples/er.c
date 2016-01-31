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

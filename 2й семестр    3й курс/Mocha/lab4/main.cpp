#include "/opt/homebrew/Cellar/open-mpi/5.0.2/include/mpi.h"
#include <iostream>
#include <stdio.h>
#include <math.h>
#include <sys/time.h>

using namespace std;

long long n = 15000;
long double h = 1;

long double func(double x) {
    return exp(-x) - cos(x) + sin (2 * x * pow(n, 2));
}

void multyThreadSolution (){
    int rank, size;
    long double result = 0.0, sum = 0.0;

    struct timeval start_time, end_time;

    gettimeofday(&start_time, NULL);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    long double start = 1 + h * rank, end = n + 1.;
    for (long double i = start; i <= end; i += h * size) sum += func(i);
    
    MPI_Reduce(&sum, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    gettimeofday(&end_time, NULL);
    if (rank == 0) {
        cout << "Result = " << result << endl;
        printf("Time: %lf \n", (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0);
    }
}

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);
    multyThreadSolution();
    MPI_Finalize();
}
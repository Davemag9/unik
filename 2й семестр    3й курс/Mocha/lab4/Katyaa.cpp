#include "/opt/homebrew/Cellar/open-mpi/5.0.2/include/mpi.h" // тут исправить на mpi.h если не в вс код
#include <iostream>
//                             mpic++ -o Katyaa.out Katyaa.cpp
//                             mpirun -n 6 Katyaa.out
#include <stdio.h>
#include <math.h>
#include <sys/time.h>

using namespace std;

double func(double x) {
    return sqrt(x-1) + 1/(x+3);// тут я заменил x-3 на х+3? а то гейство делить на 0
    // return x;
}

int main(int argc, char *argv[]) {
    int n = 10;
    int h = 2;
    
    int rank, size;
    double result = 0.0;
    double x, sum = 0.0;
    
    struct timeval start_time, end_time;

    double elapsed_time;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int chunkSize = n / size;
    int remainder = n % size;

    int start = rank * chunkSize + 1; // задаем начало и конец чанка для каждого потока)
    int end = (rank + 1) * chunkSize;

    if (rank == size - 1) { //остаток пихаем в последний поток, ибо нехуй 
        end += remainder;
    }

    gettimeofday(&start_time, NULL);

    for (int i = start; i <= end; i+=h) {
        if ((i - 1) % h != 0) i += (h - (i - 1) % h); // элеганстный костылек†††
        // если у нас h = 2 и потоков 2 то при попытке разделить на потоки выходило так, что часть
        // потоков начиналась с чисел которые не могут получиться с шагом 2, поэтому тут я делаю так, чтобы потоки
        //начинались исключительно с тех чисел которые могут быть при таком шаге
        
        // cout << i << endl;
        sum += func(i);
    }

    MPI_Reduce(&sum, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    gettimeofday(&end_time, NULL);

    if (rank == 0) {
        elapsed_time = (end_time.tv_sec - start_time.tv_sec) + (end_time.tv_usec - start_time.tv_usec) / 1000000.0;
        printf("Result: %lf\n", result); // точность результата зависит от рандома(на больших числах)
        // это либо я лох какойто, либо оно просто без критической секции ебашит или чегото такого
        printf("Elapsed time: %lf seconds\n", elapsed_time);
    }

    MPI_Finalize();
    return 0;
}

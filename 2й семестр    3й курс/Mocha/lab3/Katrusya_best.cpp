#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include "omp.h"

using namespace std;

double omp_get_wtime(void);

const int CORES_NUM = 8;
const bool PRINT = false;
const int MATRIX_SIZE = 1000;

double test_func(double x){
    return 1;
}

double func1(double x){
    return pow(x, 2) / (pow(6.1 + x, 2) + pow(3.7 + x, 2)); //это 27й вариант(5)
    
}

double func2(double x){
    return x * exp(0.7 * x) * cos(0.1 * x); //это 27й вариант(5)
}


double integral_formula(double a, double b){
    // Формула центральних прямокутників
    // return test_func(a);
    return (b - a) * func1((a + b) / 2);
    // return (b - a) * func2((a + b) / 2);
}

double count_integral(double a, double b, double step){
    double res = 0.;
    int k = (b - a) / step;
    #pragma omp for
    for (int i = 0; i < k; i++){
        double now = a + i * step;
        res += integral_formula(now, now+step);
    }
    return res;

}

int main() {
    double h = 0.2;// шаг 
    //1 integral 
    double a = 0.;
    double b = 2.;

    //2 integral 
    // double a = 0.5;
    // double b = 1.5;

    double result = 0.;
    double result_of_thread = 0.;

    omp_lock_t lock;
    omp_init_lock(&lock);
    FILE *pFile;
    pFile = fopen("integral.txt", "w");

    double timerBegin = omp_get_wtime();

#pragma omp parallel num_threads(CORES_NUM) firstprivate(result_of_thread)
    {
        result_of_thread = count_integral(a, b, h);

        while (!omp_test_lock(&lock))
        {
            fprintf(pFile,
                    "flow number %d blocked. time: %lf\n",
                    omp_get_thread_num(),
                    omp_get_wtime() - timerBegin);
            std::this_thread::sleep_for(std::chrono::milliseconds(200));
        }

        fprintf(pFile,
                "started writing to file, flow: %d, time: %lf\n",
                omp_get_thread_num(),
                omp_get_wtime() - timerBegin);

        result += result_of_thread;

        fprintf(pFile,
                "stopped writing to file, flow: %d, time: %lf\n\n",
                omp_get_thread_num(),
                omp_get_wtime() - timerBegin);

        omp_unset_lock(&lock);
    }

    double timerEnd = omp_get_wtime();

    std::cout << "Cores: " << CORES_NUM << std::endl;
    std::cout << "Res: " << result << std::endl;
    std::cout <<"Execution time: " << timerEnd - timerBegin << std::endl;
}
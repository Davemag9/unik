#include "omp.h"
#include <iostream>
#include <math.h>
#include <vector>
#include <unistd.h>
#include <chrono>
#include <stdio.h>
#include <thread>

using namespace std;

double test_func(double x){
    return 1;
}

double func1(double x){
    return 1 / (pow(2.8, 2) + 5.1 * pow(cos(1.4 * x), 2));
}

double func2(double x){
    return pow(x, 2) / (1.6 * pow(x, 2) + 0.4 * x + 1);
}


double integral(double a, double b){
    // return test_func(a);
    return func1(a) * (b - a);
    // return func2(a) * (b - a);
}

double omp_get_wtime(void);

int main(){
    
    double h = 0.00002;
    double eps = 0.01;
    double a = 0.;
    double b = 50;
    vector<double> lims;

    double rs = 0.;

    double k = a;
    while (k <= b){
        lims.push_back(k);
        k += h;
    }

    vector<double> res(lims.size(), 0.);
    omp_lock_t lock;
    omp_init_lock(&lock);
    FILE *pFile;
    pFile = fopen("integral.txt", "w");

    double t2 = omp_get_wtime();
    
    omp_set_num_threads (8);
    #pragma omp parallel shared(res)
    {   
        #pragma omp single
        cout << endl << "Lozovyi Oleh CS315 option15 (3)" << endl << endl;
        #pragma omp for
        for(int i = 0; i < lims.size() - 1; i++){
            // omp_set_lock(&lock);
            int n = omp_get_thread_num();
            while (!omp_test_lock (&lock)){
                fprintf(pFile,
                    "flow number %d blocked. time: %lf\n",
                    omp_get_thread_num(),
                    omp_get_wtime() - t2);
                std::this_thread::sleep_for(std::chrono::milliseconds(200));
                cout << "Potok locked tralaala" << endl;
            }
            // printf("The beginning of the closed section, flow %d\n\n", n);
            fprintf(pFile,
                "started writing to file, flow: %d, time: %lf\n",
                omp_get_thread_num(),
                omp_get_wtime() - t2);
            res[i] = integral(lims[i], lims[i + 1]);
            fprintf(pFile,
                "stopped writing to file, flow: %d, time: %lf\n\n",
                omp_get_thread_num(),
                omp_get_wtime() - t2);

            // cout << "Made with love by thread : " << omp_get_thread_num() << endl;
            // printf("The end of the closed section, flow %d\n\n", n);
            omp_unset_lock(&lock);
        }
    }
    
    omp_destroy_lock(&lock);
    double t1 = omp_get_wtime();
    
    for(auto x : res){
        rs += x;
    }

    cout << endl << "Result : " << rs << endl;
    cout << "Time : " << t1 - t2 << endl;
}
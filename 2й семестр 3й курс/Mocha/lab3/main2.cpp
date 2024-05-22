#include "omp.h"
// ^ этот покемон будет зависить от того, где у тебя omp.h

#include <iostream>
#include <math.h>
#include <vector>
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
    return test_func(a);
    // return func1(a) * (b - a);
    // return func2(a) * (b - a);
}

double omp_get_wtime(void);

int main(int argc, char* argv[]){
    // double h = 0.025;
    // double a = 0;
    // double b = 0.5;
    // vector<double> lims;

    // double rs = 0.;

    // for(double i = a; i + h <= b; i += h){
    //     lims.push_back(i);
    // }

    // vector<double> res(lims.size(), 0.);
    

    int c = 3;
    omp_set_num_threads (c);
    int n = 100;
    vector<double> vect(n, 0.); // вектор
    vector<double> resvect(n, 0.); // результат
    vector<vector<double>> arr(n, vector<double>(n, 0.)); // матрица

    for(int i = 0; i < n; i++){ // обычный цикл
        for(int ii = 0; ii < n; ii++){ // я выебываюсь что знаю римские цифры
            arr[i][ii] = i * cos(2 * ii)/3; // вариант 7(типа 27)
            // arr[i][ii] = i; // check1 я использовал для проверки 
        }
    }

    for(int i = 0; i < n; i++){
        vect[i] = log2(sqrt(i + 5))/(tan(2 * i) + 10); // вариант 7(типа 27)
        resvect[i] = 0.;
    }

    double t2 = omp_get_wtime();

    int count = 0;
    #pragma omp parallel shared(arr, vect, resvect)
    #pragma omp for
    for(int i = 0; i < n; i++){
        double sum = 0;
        count += 1;
        for(int ii = 0; ii < n; ii++){
            sum += arr[i][ii] * vect[ii];
        }
        resvect[i] = sum;
    }

    double t1 = omp_get_wtime();

    cout << count << endl;
}

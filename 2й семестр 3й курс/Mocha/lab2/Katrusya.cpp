#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>  // For rand and srand
#include <ctime>    // For time

#include "omp.h"

using namespace std;

double omp_get_wtime(void);

const int CORES_NUM = 8;
const bool PRINT = false;
const int MATRIX_SIZE = 1000;

int main() {
    std::srand(static_cast<unsigned>(std::time(0)));
    omp_set_num_threads(CORES_NUM);

    vector<vector<double>> a(MATRIX_SIZE, vector<double>(MATRIX_SIZE));
    vector<double> result(MATRIX_SIZE);


#pragma omp parallel shared(a, result)
    {
#pragma omp for
        for (int i = 0; i < MATRIX_SIZE; i++) {
            for (int j = 0; j < MATRIX_SIZE; j++) {
                a[i][j] = rand() % 1000 * pow(-1, rand() % 2); // тут поменял на рандомные числа(они могут быть отрицателыне)
            }
        }
    }

    if (PRINT) {
        for (int i = 0; i < MATRIX_SIZE; i++) {
            for (int j = 0; j < MATRIX_SIZE; j++) {
                cout << a[i][j] << " ";
            }
            cout << endl;
        }

        cout << endl << endl;
    }

    double timerBegin = omp_get_wtime();


// 12 это 27 в системе 15 вариантов 
// 12 Порахувати добуток від’ємних елементів у кожному рядку матриці (dynamic, 4) та (guided, 6)
#pragma omp parallel shared(a, result)
    {

//Вот тут 3 строчки omp for, каждая из них отвечает за 1н из вариантов задания

#pragma omp for                         // static
// #pragma omp for schedule (dynamic, 4)   
// #pragma omp for schedule (guided, 6)

        for (int i = 0; i < MATRIX_SIZE; i++) {
            double sum = 1;

            for (int j = 0; j < MATRIX_SIZE; j++) {
                if(a[i][j] < 0){
                    sum *= a[i][j]; // тут поменял на твое задание(поиск всех отрицательных и перемножил все)
                }
            }
            result[i] = sum;
        }

    }

    double timerEnd = omp_get_wtime();


    if (PRINT) {
        for (int i = 0; i < MATRIX_SIZE; i++) {
            cout << result[i] << " ";
        }
        cout << endl << endl;
    }

    std::cout << "Cores: " << CORES_NUM << std::endl;
    std::cout << "Matrix (MATRIX_SIZE): " << MATRIX_SIZE << std::endl;
    std::cout <<"Execution time: " << timerEnd - timerBegin << std::endl;
}
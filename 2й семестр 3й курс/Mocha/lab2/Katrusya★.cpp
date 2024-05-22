#include "omp.h" 
#include <iostream>
#include <math.h>
#include <vector>
#include <climits>
#include <cstdlib>  // For rand and srand
#include <ctime>    // For time
using namespace std;

double omp_get_wtime(void);

void inputPrint(vector<vector<int>> arr){
    for(int i = 0; i < arr.size(); i++){
        for(int ii = 0; ii < arr[i].size(); ii++){
            cout << arr[i][ii] << " ";
        }
        cout << endl;
    }

    cout << endl << endl;
}

void resultPrint(vector<int> res){
    for (int i = 0; i < res.size(); i++){
        cout << res[i] << " ";
    }

    cout << endl << endl;
}

vector<int> findRes0(vector<vector<int>> arr, int n, int k){

    vector<int> res(n, 0);
    omp_set_num_threads (k);
    double t2 = omp_get_wtime();

    #pragma omp parallel shared(arr)
    {
        #pragma omp for
        for (int i = 0; i < n; i++){

            double sum = 1;
            for (int j = 0; j < i; j++) {
                if(arr[i][j] < 0){
                    sum *= arr[i][j]; // тут поменял на твое задание(поиск всех отрицательных и перемножил все)
                }
            }
            res[i] = sum;

        }
    }

    double t1 = omp_get_wtime();

    cout << "Time with no schedule : " << t1 - t2 << endl;

    return res;
} 

vector<int> findRes1(vector<vector<int>> arr, int n, int k){

    vector<int> res(n, 0);
    omp_set_num_threads (k);
    double t2 = omp_get_wtime();

    #pragma omp parallel shared(arr)
    {
        #pragma omp for schedule (dynamic, 4)
        for (int i = 0; i < n; i++){

            double sum = 1;
            for (int j = 0; j < i; j++) {
                if(arr[i][j] < 0){
                    sum *= arr[i][j]; // тут поменял на твое задание(поиск всех отрицательных и перемножил все)
                }
            }
            res[i] = sum;

        }
    }

    double t1 = omp_get_wtime();

    cout << "Time with schedule (dynamic, 4) : " << t1 - t2 << endl;

    return res;
} 

vector<int> findRes2(vector<vector<int>> arr, int n, int k){

    vector<int> res(n, 0);
    omp_set_num_threads (k);
    double t2 = omp_get_wtime();

    #pragma omp parallel shared(arr)
    {
        #pragma omp for schedule (guided, 6)
        for (int i = 0; i < n; i++){

            double sum = 1;
            for (int j = 0; j < i; j++) {
                if(arr[i][j] < 0){
                    sum *= arr[i][j]; // тут поменял на твое задание(поиск всех отрицательных и перемножил все)
                }
            }
            res[i] = sum;

        }
    }

    double t1 = omp_get_wtime();

    cout << "Time with schedule (guided, 6) : " << t1 - t2 << endl;

    return res;
} 

int main(){

    int n = 5000;
    int firs_num = 5;
    int num_of_0 = 3;
    std::srand(static_cast<unsigned>(std::time(0)));
    omp_set_num_threads (8);
    vector<vector<int>> arr(n, vector<int>(n, 0));

    #pragma omp parallel shared(arr)
    #pragma omp for 
    for (int i = 0; i < arr.size(); i++){
        for (int ii = 0; ii < arr[i].size(); ii++){
            arr[i][ii] = rand() % 1000 * pow(-1, rand() % 2);
        }
    }

    // inputPrint(arr);

    for (int i = 1; i < firs_num + 1; i++){
        for (int k = 1; k < 10; k*=2){
        cout << endl << "N = " << i*pow(10, num_of_0) << endl;
        cout << "Num of threads = " << k << endl;
        vector<int> res0 = findRes0(arr, i*pow(10, num_of_0), k);
        vector<int> res1 = findRes1(arr, i*pow(10, num_of_0), k);
        vector<int> res2 = findRes2(arr, i*pow(10, num_of_0), k);
        }
        cout << endl << endl << endl;
    }
    
    

    // resultPrint(res);
}
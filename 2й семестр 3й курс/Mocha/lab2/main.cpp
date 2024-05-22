#include "omp.h" 
#include <iostream>
#include <math.h>
#include <vector>
#include <climits>
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

            int min = INT_MAX;
            int max = INT_MIN;

            for (int ii = 0; ii < n; ii++){
                if (arr[i][ii] > max) max = arr[i][ii];
                if (arr[i][ii] < min) min = arr[i][ii];
            }

            res[i] = min + max;

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
        #pragma omp for schedule (dynamic, 2)
        for (int i = 0; i < n; i++){

            int min = INT_MAX;
            int max = INT_MIN;

            for (int ii = 0; ii < n; ii++){
                if (arr[i][ii] > max) max = arr[i][ii];
                if (arr[i][ii] < min) min = arr[i][ii];
            }

            res[i] = min + max;

        }
    }

    double t1 = omp_get_wtime();

    cout << "Time with schedule (dynamic, 2) : " << t1 - t2 << endl;

    return res;
} 

vector<int> findRes2(vector<vector<int>> arr, int n, int k){

    vector<int> res(n, 0);
    omp_set_num_threads (k);
    double t2 = omp_get_wtime();

    #pragma omp parallel shared(arr)
    {
        #pragma omp for schedule (guided, 2)
        for (int i = 0; i < n; i++){

            int min = INT_MAX;
            int max = INT_MIN;

            for (int ii = 0; ii < n; ii++){
                if (arr[i][ii] > max) max = arr[i][ii];
                if (arr[i][ii] < min) min = arr[i][ii];
            }

            res[i] = min + max;

        }
    }

    double t1 = omp_get_wtime();

    cout << "Time with schedule (guided, 2) : " << t1 - t2 << endl;

    return res;
} 

int main(){

    int n = 50000;
    
    omp_set_num_threads (8);
    vector<vector<int>> arr(n, vector<int>(n, 0));

    #pragma omp parallel shared(arr)
    #pragma omp for 
    for (int i = 0; i < arr.size(); i++){
        for (int ii = 0; ii < arr[i].size(); ii++){
            arr[i][ii] = rand() % 10;
        }
    }

    // inputPrint(arr);


    for (int k = 1; k < 10; k*=2){
        for (int i = 1; i < 6; i++){
        cout << endl << "N = " << i*10000 << endl;
        vector<int> res0 = findRes0(arr, i*10000, k);
        vector<int> res1 = findRes1(arr, i*10000, k);
        vector<int> res2 = findRes2(arr, i*10000, k);
        }
        cout << endl << endl << endl;
    }
    
    

    // resultPrint(res);
}
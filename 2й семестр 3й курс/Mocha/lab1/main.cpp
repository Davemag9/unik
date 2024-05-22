#include "omp.h" 
#include <iostream>
#include <math.h>
#include <vector>
using namespace std;

double omp_get_wtime(void);
double time1Core;


void inputPrint(vector<double> vect, vector<vector<double>> arr){
    for(int i = 0; i < arr.size(); i++){
        for(int ii = 0; ii < arr.size(); ii++){
            cout << arr[i][ii] << " ";
        }
        cout << endl;
    }

    cout << endl << endl;

    for(int i = 0; i < arr.size(); i++){
        cout << vect[i] << " ";
    }
    cout << endl << endl;

    // for (int i = 0; i < n; i++){
    //     cout << resvect[i] << " ";
    // }
    // cout << endl << endl;
}


void outputPrint(int cores, int n, double t){
    cout << "Threads : " << cores << endl;
    // cout << "Matrix size : " << n << endl;
    cout << "Time : " << t << endl;
    cout << "Speedup : " << time1Core / t << endl;
    cout << "Efficiency : " << time1Core / (double(cores) * t) << endl << endl;

    // cout << cores << " " << t << " " <<  time1Core / t << " " << time1Core / (double(cores) * t) << endl;
}


pair<vector<double>, double> findRes(int cores, vector<double> vect, vector<vector<double>> arr){
    
    vector<double> resvect(arr.size(), 0.);
    omp_set_num_threads (cores);

    double t2 = omp_get_wtime();

    #pragma omp parallel shared(arr, vect, resvect)
    {   
        // #pragma omp critical
        #pragma omp for 
        for(int i = 0; i < arr.size(); i++){
            for(int ii = 0; ii < arr.size(); ii++){
                resvect[ii] += arr[ii][i] * vect[i];
            }
        }
    }

    double t1 = omp_get_wtime();

    return make_pair(resvect, t1 - t2);
}


int main(){
    cout.precision(4);
    int n = 1000;
    vector<double> vect(n, 0.);
    vector<vector<double>> arr(n, vector<double>(n, 0.));

    for(int i = 0; i < n; i++){
        for(int ii = 0; ii < n; ii++){
            arr[i][ii] = ii * tan(i);
        }
        vect[i] = i * sqrt(i * cos(i));
    }

    for(int i = 1; i < 10; i*=2){

        omp_set_num_threads (i);
        pair<vector<double>, double> res = findRes(i, vect, arr);

        if(i == 1) time1Core = res.second;
        outputPrint(i, n, res.second);
        
    }

    // omp_set_num_threads (1);
    // pair<vector<double>, double> res0 = findRes(1, vect, arr);
    // time1Core = res0.second;
    // outputPrint(1, n, res0.second);

    // omp_set_num_threads (8);
    // pair<vector<double>, double> res = findRes(1, vect, arr);
    // outputPrint(8, n, res.second);

    // omp_set_num_threads (80);
    // pair<vector<double>, double> res1 = findRes(1, vect, arr);
    // outputPrint(80, n, res1.second);

}

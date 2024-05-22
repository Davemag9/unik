#include "omp.h"
// ^ этот покемон будет зависить от того, где у тебя omp.h

#include <iostream>
#include <math.h>
#include <vector>
using namespace std;

double omp_get_wtime(void); // инициализация таймера

int main(int argc, char* argv[]){
    int c = 1; // Желательно ставить не больше чем количество ядер
    int n = 5;
    
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
        // vect[i] = i; // check2 я использовал для проверки
        /*
            Инструкция для сheck: 
            1) установить n = 5
            2) убрать // с check1 и check2
            3) в результате (resvect) должно получиться 0 10 20 30 40
            4) радоваться что оно правильно считает :)
        */
        resvect[i] = 0.;
    }

    // вывод матрицы и вектора
    // for(int i = 0; i < n; i++){
    //     for(int ii = 0; ii < n; ii++){
    //         cout << arr[i][ii] << " ";
    //     }
    //     cout << endl;
    // }

    // cout << endl << endl;

    // for(int i = 0; i < n; i++){
    //     cout << vect[i] << " ";
    // }
    // cout << endl << endl;

    double t2 = omp_get_wtime();// начало таймера

    // Katyaa★ (матрица по строкам)
    int counter = 0;
    omp_set_num_threads (c); // определяю количество ядер для того чтобы знать на сколько потоков делить

    #pragma omp parallel shared(arr, vect, resvect) // выделить паралельные фрагменты(методичка так говорит)
    // при этом arr, vect, resvect будут общими для каждого потока 
    #pragma omp for // обозначает что следующий цикл for будет разпаралелен
    // тоесть если потока 2 то 0й поток будет брать все четные i а 1й все нечетные


    // ниже простой цикл для поиска результата(for(i) - распаралеленый)
    for(int i = 0; i < n; i++){
        counter += i;
        double sum = 0;
        for(int ii = 0; ii < n; ii++){
            sum += arr[i][ii] * vect[ii]; // матрица для умножения поделена на строки
        }
        resvect[i] = sum;
    }

    // не Katyaa
    //   (матрица по столбикам)
    // #pragma omp parallel shared(arr, vect, resvect) // выделить паралельные фрагменты(методичка так говорит)
    // // при этом arr, vect, resvect будут общими для каждого потока 
    // #pragma omp for // обозначает что следующий цикл for будет разпаралелен
    // // тоесть если потока 2 то 0й поток будет брать все четные i а 1й все нечетные
    

    // // ниже простой цикл для поиска результата(for(i) - распаралеленый)
    // for(int i = 0; i < n; i++){
    //     for(int ii = 0; ii < n; ii++){
    //         resvect[ii] += arr[ii][i] * vect[i]; // матрица для умножения поделена на столбики
    //     }
    // }

    double t1 = omp_get_wtime(); // конец таймера


    // вывод результата
    // for (int i = 0; i < n; i++){
    //     cout << resvect[i] << " ";
    // }
    // cout << endl << endl;
    
    //вывод таймера и количества ядер использованых при распаралеливании
    // printf("Time : %f \nCore num : %d \nMatrix size : %d", t1 - t2, c, n);

    cout << counter << endl;
}

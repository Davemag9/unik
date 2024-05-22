#include <opencv2/opencv.hpp>
#include </opt/homebrew/Cellar/llvm/18.1.4/lib/clang/18/include/omp.h>
#include <iostream>
#include <vector>
#include <filesystem>
#include <utility>
#include <algorithm>
#include <chrono>
// g++ -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -std=c++17 $(pkg-config --cflags --libs opencv4) -Xclang -fopenmp main.cpp -o main -lomp && ./main
using namespace std;

struct df{
    std::vector<vector<int>> Image;
    int Class;
    df(std::vector<vector<int>> img, int cls) : Image(img), Class(cls) {}
};


int main() {
    omp_set_num_threads (8);
    int res_count = 0;
    std::vector<std::string> folder_names;
    vector<df> test;
    vector<df> train;

    vector<string> loh = {".git", "Bazooka", "Revolver", "Knife"};
    std::string directory_path = "/Users/davemag9/VSCode/Mocha/Mochurad Hvoida/Different-Weapon-Types-datasets";

    int lolkek = 0;
    std::chrono::steady_clock::time_point start_time1 = std::chrono::steady_clock::now();
    for (const auto& entry : std::__fs::filesystem::directory_iterator(directory_path)) {
        if (entry.is_directory()) {
            bool check = true;
            string folder = entry.path().filename().string();
            
            #pragma omp parallel
            #pragma omp for
            for (auto item : loh) if (item == folder) check = false;
            if (check) folder_names.push_back(entry.path().filename().string());
        }
    }
    
    for (auto item : folder_names){
        int kurwa_bober = 0;
        string now_load = directory_path + "/" + item;
        for (const auto& entry : std::__fs::filesystem::directory_iterator(now_load)) {
            std::string link = now_load + "/" + entry.path().filename().string();
            cv::Mat image = cv::imread(link, cv::IMREAD_GRAYSCALE);

            if (image.empty()) {
                std::cerr << "Error: Unable to load image." << std::endl;
                return -1;
            }
            cv::resize(image, image, cv::Size(144, 144));
            int height = image.rows;
            int width = image.cols;
    
            std::vector<vector<int>> imagehui(height, (vector<int>(width, 0))); 
            #pragma omp parallel
            #pragma omp for
            for (int i = 0; i < height; ++i) {
                for (int j = 0; j < width; ++j) {
                    int intensity = static_cast<int>(image.at<uchar>(i, j));
                    imagehui[i][j] = abs(intensity);
                }
            }

            df tmp (imagehui, lolkek);
            if (kurwa_bober > 5) train.push_back(tmp);
            else test.push_back(tmp);
            kurwa_bober += 1;
        }
        lolkek +=1;
    }
    chrono::steady_clock::time_point end_time1 = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_seconds1 = end_time1 - start_time1;
    omp_set_num_threads(8);
    
    vector<pair<string, string>> result;
    std::chrono::steady_clock::time_point start_time = std::chrono::steady_clock::now();
    #pragma omp parallel
    #pragma omp for
    for (auto item : test){
        vector<pair<int, int>> len;
        for (int z = 0; z < train.size(); z++){
            long long tmp_len = 0;
            for (int i = 0; i < train[z].Image.size(); i++){
                for (int j = 0; j < train[z].Image[0].size(); j++){
                    tmp_len += pow(train[z].Image[i][j] - item.Image[i][j], 2);
                }
            }
            len.push_back(make_pair(sqrt(tmp_len), train[z].Class));
        }
        sort(len.begin(), len.end());

        vector<int> classes(folder_names.size(), 0);
        for (int c = 0; c < 10; c++) classes[len[c].second] += 1;

        int index = 0;
        for (int c = 0; c < folder_names.size(); c++) if (classes[c] > classes[index]) index = c; 

        if (item.Class == index) res_count += 1;
        // result.push_back(make_pair(item.Class, folder_names[index]));
        cout << "real = " << folder_names[item.Class] << "    " << "pred = " << folder_names[index] << endl;
    }

    chrono::steady_clock::time_point end_time = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed_seconds = end_time - start_time;
    cout << elapsed_seconds.count() << endl;
    cout << elapsed_seconds1.count() << endl;

    cout  << double(res_count)/double(test.size()) * 100. << "%" << endl;
}

        // 5 all 75%
        // 15 all 72.2%
        // 5 without knife 70%
        // 15 without knife 66.6%
        // 100 without knife 63.3%
        // 786 without knife 50%
        // 5 without knife, revolver 75%
        // 15 without knife, revolver 75%
        // 25 without knife, revolver 75%
        // 5 without Hunting_Rifle, revolver 75%
        // 15 without Hunting_Rifle, revolver 75%
        // 25 without Hunting_Rifle, revolver 75%
        // 25 without Hunting_Rifle, Knife 66.6%

        // norm
        // 25 without Hunting_Rifle, Knife 91.6%
        // 25 all 80.5%
        // 50 all 72.5%
        // 10 all 83.3%
        // 10 no revolver 90%
        // 10 no revolver, knife 95.8%
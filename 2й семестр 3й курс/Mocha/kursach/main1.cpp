#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>

using namespace std;


int main() {
    string input = "/Users/davemag9/VSCode/Mocha/Mochurad Hvoida/Different-Weapon-Types-datasets/Assault_Rifle/saldiri_tufek1.jpg";
    vector<vector<int>> STRING;
    ifstream openFile;
    openFile.open(input.c_str(), std::ios::binary);

    if(openFile.is_open()){
        cout << "File opened" << endl;
        std::vector<unsigned char> buffer(istreambuf_iterator<char>(openFile), {});

        for(auto x : buffer){
            cout << x << endl;
        }
    }  
    else {
        cout << "Cant open the file " << endl;
    }
    // cout << openFile << endl;
}
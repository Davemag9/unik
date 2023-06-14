

#include "Ctrl.h"
#include "GamePlan.h"
#include "QuickGamePlan.h"

void Ctrl::GameRules() {
    cout << "Youre playing the Football daft." << endl
         << "Use only nums buttons. Goodluck!" << endl
         << "----------------------------------------------------------------------------------------" << endl;
}

void Ctrl::GameType() {
    cout << "Now choose game gametype." << endl
         << "If you want to play a quick game (only 1 click) type 1 ." << endl
         << "If you want to play a normal game (22 clicks) type 2 ." << endl;
}

void Ctrl::speech() {
    Ctrl::GameRules();
    Ctrl::GameType();
    bool check = true;
    while (check){
        cout << "Your pick: ";
        string inp;
        cin >> inp;
        bool flag = false;
        for(auto c:inp){
            if(!isdigit(c)){
                flag = true;
                break;
            }
        }
        if(flag) {
            cout << "Only digit. Try again." << endl;
            continue;
        }
        int k = stoi(inp);
        if(k == 1){
            QuickGamePlan::startQuickGame();
            check = false;
        }
        else if(k == 2){
            GamePlan::startsGame();
            check = false;
        }
        else{
            cout << "Only 1 or 2. Try again." << endl;
        }
    }
}


#include "GameProcess.h"
#include "Player.h"
#include "GameMechanic.h"

vector<int> GameProcess::quickTeamSet = {};
void GameProcess::pickCout(vector<pair<int, bool>> arr) {
    if(arr[1].second) cout << "\t\t\t2 " << endl;
    else cout << "\t\t\t2x" << endl;
    if(arr[0].second) cout << "1 \t\t\t\t\t\t";
    else cout << "1x\t\t\t\t\t\t";
    if(arr[2].second) cout << "3 " << endl;
    else cout << "3x" << endl;
    if(arr[3].second) cout << "\t\t4 \t\t";
    else cout << "\t\t4x\t\t";
    if(arr[4].second) cout << "5 " << endl;
    else cout << "5x" << endl;
    if(arr[5].second) cout << "\t\t\t6 " << endl;
    else cout << "\t\t\t6x" << endl;
    if(arr[6].second) cout << "7 \t\t\t\t\t\t";
    else cout << "7x\t\t\t\t\t\t";
    if(arr[7].second) cout << "8 " << endl;
    else cout << "8x" << endl;
    if(arr[8].second) cout << "\t\t9 \t\t";
    else cout << "\t\t9x\t\t";
    if(arr[9].second) cout << "10 " << endl;
    else cout << "10x" << endl;
    if(arr[10].second) cout << "\t\t\t11 " << endl;
    else cout << "\t\t\t11x" << endl;
    cout << endl;
}
void GameProcess::pickPosition() {
    vector<pair<int, bool>> arr;
    for(int i = 0; i < 11; i++)arr.push_back({i + 1, false});
    GameProcess::pickCout(arr);
    for(int j = 0; j < 11; j++){
        int pos;
        bool check = false;
        while (!check){
            cout << "Pick position : ";
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
            pos = stoi(inp);
            if(pos > 11 or pos < 1){
                cout << "There is no position with number " << pos <<". Try to pick one more time." << endl;
            }
            else{
                if(arr[pos - 1].second){
                    cout << "You already choose player on that position. Try to pick another position." << endl;
                }
                else{
                    check = true;
                }
            }
        }
        cout << endl;
        if(pos == 1) GameMechanic::PlayersForPeak(lw);
        else if(pos == 2) GameMechanic::PlayersForPeak(st);
        else if(pos == 3) GameMechanic::PlayersForPeak(rw);
        else if(pos == 4) GameMechanic::PlayersForPeak(cm1);
        else if(pos == 5) GameMechanic::PlayersForPeak(cm2);
        else if(pos == 6) GameMechanic::PlayersForPeak(cdm);
        else if(pos == 7) GameMechanic::PlayersForPeak(lb);
        else if(pos == 8) GameMechanic::PlayersForPeak(rb);
        else if(pos == 9) GameMechanic::PlayersForPeak(lcd);
        else if(pos == 10) GameMechanic::PlayersForPeak(rcd);
        else if(pos == 11) GameMechanic::PlayersForPeak(gk);
        arr[pos - 1].second = true;
        GameProcess::pickCout(arr);
    }
}

int GameProcess::leagueScore(vector<int> vect){
    set<string> check;
    for(int i = 0; i < vect.size(); i++){
        check.insert(Player::teamGetPlayer(i,vect).getLeague());
    }
    return check.size();
}

int GameProcess::nationScore(vector<int> vect){
    set<string> check;
    for(int i = 0; i < vect.size(); i++){
        check.insert(Player::teamGetPlayer(i,vect).getNation());
    }
    return check.size();
}

int GameProcess::ratingScore(vector<int> vect){
    int sum = 0;
    for(int i = 0; i < vect.size(); i++){
        sum += Player::teamGetPlayer(i,vect).getRating();
    }
    return sum / 11;
}


vector<pair<int, int>> links;
vector<vector<int>> graph;

void GameProcess::createLinks(){
    links.push_back({1, 3});
    links.push_back({3 , 2});
    links.push_back({1, 4});
    links.push_back({3, 4});
    links.push_back({3, 5});
    links.push_back({2 , 5});
    links.push_back({4, 5});
    links.push_back({4, 6});
    links.push_back({5, 6});
    links.push_back({4, 7});
    links.push_back({5, 8});
    links.push_back({6, 9});
    links.push_back({6, 10});
    links.push_back({7, 9});
    links.push_back({8, 10});
    links.push_back({9, 10});
    links.push_back({9, 11});
    links.push_back({10, 11});
}

void GameProcess::createGraph(){
    graph.resize(12);
    for(auto x : links){
        graph[x.first].push_back(x.second);
        graph[x.second].push_back(x.first);
    }
}

void GameProcess::customCout(){
    //11 bukv
    cout << "\t\t\t" << Player::getFieldPlayer(st).getName() << endl;
    cout << Player::getFieldPlayer(lw).getName() << "\t\t\t\t\t\t" << Player::getFieldPlayer(rw).getName() << endl << endl;

    cout << "\t   " << Player::getFieldPlayer(cm1).getName() << "\t\t" << Player::getFieldPlayer(cm2).getName() << endl;
    cout << "\t\t\t" << Player::getFieldPlayer(cdm).getName() << endl << endl;

    cout << Player::getFieldPlayer(lb).getName() << "\t\t\t\t\t\t" << Player::getFieldPlayer(rb).getName() << endl;
    cout << "\t   " << Player::getFieldPlayer(lcd).getName() << "\t\t" << Player::getFieldPlayer(rcd).getName() << endl;
    cout << "\t\t\t" << Player::getFieldPlayer(gk).getName() << endl;
}


void GameProcess::quickCustomCout(){
    //11 bukv
    cout << "\t\t\t" << Player::teamGetPlayer(st, GameProcess::getQuickTeam()).getName() << endl;
    cout << Player::teamGetPlayer(lw, GameProcess::getQuickTeam()).getName() << "\t\t\t\t\t\t" << Player::teamGetPlayer(rw, GameProcess::getQuickTeam()).getName() << endl << endl;

    cout << "\t   " << Player::teamGetPlayer(cm1, GameProcess::getQuickTeam()).getName() << "\t\t" << Player::teamGetPlayer(cm2, GameProcess::getQuickTeam()).getName() << endl;
    cout << "\t\t\t" << Player::teamGetPlayer(cdm, GameProcess::getQuickTeam()).getName() << endl << endl;

    cout << Player::teamGetPlayer(lb, GameProcess::getQuickTeam()).getName() << "\t\t\t\t\t\t" << Player::teamGetPlayer(rb, GameProcess::getQuickTeam()).getName() << endl;
    cout << "\t   " << Player::teamGetPlayer(lcd, GameProcess::getQuickTeam()).getName() << "\t\t" << Player::teamGetPlayer(rcd, GameProcess::getQuickTeam()).getName() << endl;
    cout << "\t\t\t" << Player::teamGetPlayer(gk, GameProcess::getQuickTeam()).getName() << endl;
}

int GameProcess::chemistryScore(vector<int> vect){
    vector<int> teamChemistry(12);
    GameProcess::createLinks();
    GameProcess::createGraph();
    //cout << 1;
    for(int i = 1; i < vect.size(); i++){
        int counter = 0;
        //cout << 2;
        for(auto x : graph[i]){
            if(Player::teamGetPlayer(i,vect).getLeague() == Player::teamGetPlayer(x - 1,vect).getLeague()){
                counter ++;
                //cout << 3;
            }
            if(Player::teamGetPlayer(i,vect).getNation() == Player::teamGetPlayer(x - 1,vect).getNation()){
                counter++;
                //cout << 3;
            }
            if(Player::teamGetPlayer(i,vect).getClub() == Player::teamGetPlayer(x - 1,vect).getClub()){
                counter ++;
                //cout << 3;
            }

        }
        double check = counter / graph[i].size();
        //cout << 4;
        if(check >= 0 and check <= 0.2){
            teamChemistry[i + 1] = 3;
        }
        else if(check > 0.2 and check <= 0.4){
            teamChemistry[i + 1] = 4;
        }
        else if(check > 0.4 and check <= 0.7){
            teamChemistry[i + 1] = 6;
        }
        else if(check > 0.7 and check < 1){
            teamChemistry[i + 1] = 7;
        }
        else{
            teamChemistry[i + 1] = 10;
        }
    }
    //cout << 5;
    int sumOfChem = 0;
    for(int i = 1; i < 12; i++){
        sumOfChem += teamChemistry[i];
    }
    if(sumOfChem > 100){
        sumOfChem = 100;
    }
    return sumOfChem;

}


void GameProcess::countScore(vector<int> team, vector<int> vect){
    int yourScore = 0, botScore = 0;
    int u, o;
    u = GameProcess::leagueScore(team);
    o = GameProcess::leagueScore(vect);
    if(u == o){
        yourScore++;
        botScore++;
    }
    else if(u > o){
        yourScore++;
    }
    else{
        botScore++;
    }
    cout << "Leagues: YOU - " << u << "    Oponent - " << o << endl;
    u = GameProcess::nationScore(team);
    o = GameProcess::nationScore(vect);
    if(u == o){
        yourScore++;
        botScore++;
    }
    else if(u > o){
        yourScore++;
    }
    else{
        botScore++;
    }
    cout << "Nations: YOU - " << u << "    Oponent - " << o << endl;
    u = GameProcess::ratingScore(team);
    o = GameProcess::ratingScore(vect);
    if(u == o){
        yourScore++;
        botScore++;
    }
    else if(u > o){
        yourScore++;
    }
    else{
        botScore++;
    }
    cout << "Avarage rating: YOU - " << u << "    Oponent - " << o << endl;
    u = GameProcess::chemistryScore(team);
    o = GameProcess::chemistryScore(vect);
    if(u == o){
        yourScore++;
        botScore++;
    }
    else if(u > o){
        yourScore += 2;
    }
    else{
        botScore += 2;
    }
    cout << "Team chemistry:  YOU - " << u << "    Oponent - " << o << endl;
    if(yourScore > botScore){
        cout << "You WIN." << endl;
    }
    else if(yourScore == botScore){
        cout << "Draw." << endl;
    }
    else{
        cout << "You LOSE. Good luck in the next game." << endl;
    }
}

void GameProcess::setOponent(vector<int> team){
    vector<int> bot1 = { 8, 9, 3, 9, 6, 9, 3, 9, 8, 8, 2};
    vector<int> bot2 = { 4, 5, 4, 5, 4, 4, 4, 5, 4, 8, 4};
    vector<int> bot3 = { 6, 7, 7, 8, 8, 8, 7, 7, 6, 7, 6};
    int a = rand()%3;
    if(a == 0){
        GameProcess::countScore(team, bot1);
    }
    else if(a == 1){
        GameProcess::countScore(team, bot2);
    }
    else{
        GameProcess::countScore(team, bot3);
    }
}

const vector<int> &GameProcess::getQuickTeam() {
    return GameProcess::quickTeamSet;
}

void GameProcess::quickTeam() {
    vector<int> bot1 = { 6, 6, 2, 3, 4, 6, 1, 2, 3, 4, 5};
    vector<int> bot2 = { 1, 2, 1, 2, 2, 1, 1, 3, 1, 9, 1};
    vector<int> bot3 = { 2, 6, 8, 4, 3, 7, 8, 1, 4, 2, 6};
    cout << "Pick number from 1 to 3: ";
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
        return GameProcess::quickTeam();
    }
    int num = stoi(inp);
    if(num < 1 or num > 3){
        cout << "Only 1 to 3! Try again." << endl;
        return GameProcess::quickTeam();
    }
    else{
        if(num == 1){
            quickTeamSet = bot1;
        }
        else if(num == 2){
            quickTeamSet = bot2;
        }
        else if(num == 3){
            quickTeamSet = bot3;
        }
    }

}


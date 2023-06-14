//
// Created by davem on 03.05.2022.
//

#ifndef ROZRAHAFINALCUT_GAMEPROCESS_H
#define ROZRAHAFINALCUT_GAMEPROCESS_H
#include <iostream>
#include "boost/di.hpp"
using namespace std;

class GameProcess {

private:
    static vector<int> quickTeamSet;
public:
    static int leagueScore(vector<int> vect);
    static int nationScore(vector<int> vect);
    static int ratingScore(vector<int> vect);
    static void createLinks();
    static void createGraph();
    static void customCout();
    static void quickCustomCout();
    static int chemistryScore(vector<int> vect);
    static void countScore(vector<int> team, vector<int> vect);
    static void setOponent(vector<int> team);
    static void quickTeam();
    static void pickPosition();
    static void pickCout(vector<pair<int, bool>> arr);
    static const vector<int> &getQuickTeam();
};


#endif //ROZRAHAFINALCUT_GAMEPROCESS_H

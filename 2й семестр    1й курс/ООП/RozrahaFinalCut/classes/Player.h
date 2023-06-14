#ifndef ROZRAHAFINALCUT_PLAYER_H
#define ROZRAHAFINALCUT_PLAYER_H
#include <iostream>
#include "boost/di.hpp"
#include "IPlayer.h"

using namespace std;

enum Position{ lw = 0, rw, st, cm1, cm2, cdm, lb, rb, lcd, rcd, gk };



class Player: public IPlayer{
public:
    static constexpr auto bName = []{};
    static constexpr auto bClub = []{};
    static constexpr auto bNation = []{};
    static constexpr auto bLeague = []{};
    static constexpr auto bRating = []{};

    BOOST_DI_INJECT(Player, (named = bName)string aName, (named = bClub)string aClub,
                    (named = bNation)string aNation, (named = bLeague)string aLeague, (named = bRating)int aRating)
    : Name (aName), Club(aClub), Nation(aNation), League(aLeague), Rating(aRating) {}

    static void createPlayers();
    static Player getPlayer(int position, int num);
    static Player teamGetPlayer(int id, vector<int> arr);
    static Player getFieldPlayer(int position);
    string getName() override;
    string getClub() override;
    string getNation() override;
    string getLeague() override;
    int getRating();
    static void teamAddPlayer(int id);
    static const vector<int>& getTeam();

private:
    string Name;
    string Club;
    string Nation;
    string League;
    int Rating;

    static vector< vector < Player > > Pl_IoC;
    static vector<int> team;
};


#endif //ROZRAHAFINALCUT_PLAYER_H



#include "Player.h"
#include <fstream>

vector< vector < Player > > Player::Pl_IoC(gk + 1);
vector<int> Player::team = {};

void Player::createPlayers(){
    int counter = 0;
    ifstream indata;
    indata.open("data\\PlrData.data");
    if(not indata) { // file couldn't be opened
        cerr << "Error: file could not be opened" << endl;
        exit(1);
    }
    while ( !indata.eof() ) { // keep reading until end-of-file
        string str1, str2, str3, str4;
        int rtg;
        indata >> str1 >> str2 >> str3 >> str4 >> rtg;
        Pl_IoC[counter / 10].push_back(boost::di::make_injector(
                boost::di::bind<string>.named(bName).to(str1), boost::di::bind<string>.named(bClub).to(str2),
                boost::di::bind<string>.named(bNation).to(str3), boost::di::bind<string>.named(bLeague).to(str4),
                boost::di::bind<int>.named(bRating).to(rtg)).create<Player>());
        counter++;
    }
    indata.close();

}

string Player::getName(){
    return this->Name;
}
string Player::getClub() {
    return this->Club;
}
string Player::getNation() {
    return this->Nation;
}
string Player::getLeague() {
    return this->League;
}
int Player::getRating() {
    return this->Rating;
}

Player Player::getPlayer(int position, int num) {
    return Pl_IoC[position][num];
}

void Player::teamAddPlayer(int id) {
    team.push_back(id);
}

Player Player::teamGetPlayer(int id, vector<int> arr) {
    return Pl_IoC[id][arr[id]];
}

Player Player::getFieldPlayer(int position) {
    return Pl_IoC[position][team[position]];
}

const vector<int> &Player::getTeam() {
    return team;
}

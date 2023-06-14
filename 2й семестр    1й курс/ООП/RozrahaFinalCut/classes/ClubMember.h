//
// Created by davem on 12.05.2022.
//

#ifndef ROZRAHAFINALCUT_CLUBMEMBER_H
#define ROZRAHAFINALCUT_CLUBMEMBER_H
#include <string>
using namespace std;

class ClubMember {
public:
    virtual string getLeague() = 0;
    virtual string getClub() = 0;
};


#endif //ROZRAHAFINALCUT_CLUBMEMBER_H

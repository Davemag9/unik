//
// Created by davem on 12.05.2022.
//

#ifndef ROZRAHAFINALCUT_PERSON_H
#define ROZRAHAFINALCUT_PERSON_H
#include <string>
using namespace std;

class Person {
public:
    virtual string getName() = 0;
    virtual string getNation() = 0;
};


#endif //ROZRAHAFINALCUT_PERSON_H

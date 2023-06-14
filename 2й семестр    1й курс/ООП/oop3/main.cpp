#include <bits/stdc++.h>
#include "boost/di.hpp"
using namespace std;
namespace di = boost::di;
//i
class ISpoiler{
public:
    virtual void DownForce() = 0;
};

class ITires{
public:
    virtual void Speed() = 0;
};

class IEngine{
public:
    virtual void Power() = 0;
};
//s
class DuckTail : public ISpoiler{
public:
    void DownForce() override{
        cout << "You use a Ducktail. So you have minimal downforce." << endl;
    }
};

class BigSpoiler : public ISpoiler{
public:
    void DownForce() override{
        cout << "You use a Big Spoiler. So you have maximal downforce." << endl;
    }
};

class FrontSpoiler : public ISpoiler{
public:
    void DownForce() override{
        cout << "You use a Front Spoiler. So you have medium downforce." << endl;
    }
};

class SoftSlicks : public ITires{
public:
    void Speed() override{
        cout << "You use Soft Slicks.\n Characteristics:\n Speed: maximal\n Distance: minimal\n" << endl;
    }
};

class MediumSlicks : public ITires{
public:
    void Speed() override{
        cout << "You use Medium Slicks.\n Characteristics:\n Speed: medium\n Distance: medium\n" << endl;
    }
};

class HardSlicks : public ITires{
public:
    void Speed() override{
        cout << "You use Hard Slicks.\n Characteristics:\n Speed: minimal\n Distance: maximal\n" << endl;
    }
};

class ToyotaEngine : public IEngine{
public:
    void Power() override{
        cout << "You use 2jz-gte. Now you have 700 hp." << endl;
    }
};

class NissanEngine : public IEngine{
public:
    void Power() override{
        cout << "You use RB26DETT. Now you have 400 hp." << endl;
    }
};

class LadaEngine : public IEngine{
public:
    void Power() override{
        cout << "You use 2103`s engine. Maybe you have some hp/dp(donkey powers)." << endl;
    }
};

class Car{
public:
    IEngine* Engine = nullptr;
    ISpoiler* Spoiler = nullptr;
    ITires* Tires = nullptr;
    //di
    Car(IEngine* aEngine, ISpoiler* aSpoiler, ITires* aTires) : Engine(aEngine), Spoiler(aSpoiler), Tires(aTires){};

    void CarInfo(){
        Engine -> Power();
        Spoiler -> DownForce();
        Tires -> Speed();
    }
};

int main(){
    auto preset1 = di::make_injector(boost::di::bind<IEngine>.to(new ToyotaEngine), boost::di::bind<ISpoiler>.to(new DuckTail), boost::di::bind<ITires>.to(new SoftSlicks));
    auto preset2 = di::make_injector(boost::di::bind<IEngine>.to(new NissanEngine), boost::di::bind<ISpoiler>.to(new FrontSpoiler), boost::di::bind<ITires>.to(new HardSlicks));
    auto preset3 = di::make_injector(boost::di::bind<IEngine>.to(new LadaEngine), boost::di::bind<ISpoiler>.to(new BigSpoiler), boost::di::bind<ITires>.to(new MediumSlicks));
    Car myCar = preset3.create<Car>();
    myCar.CarInfo();
}
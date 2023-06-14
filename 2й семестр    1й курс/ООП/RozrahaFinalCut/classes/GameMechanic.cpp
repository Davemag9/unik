
#include "GameMechanic.h"
#include "Player.h"

int PickPlayer(){
    cout << "Your choice: ";
    int choise;
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
        return PickPlayer();
    }
    choise = stoi(inp);
    if(choise < 1 or choise > 5){
        cout << "Wrong choice :(" << " Try again." << endl;
        return PickPlayer();
    }
    else{
        return choise;
    }
}

void GameMechanic::PlayersForPeak(int position) {
    srand(time(NULL));
    vector<int> pick;
    int counter = 1;
    pick.push_back(rand() % 10);
    while (counter != 5){
        bool check = true;
        int a = rand()%10;
        for(auto x : pick){
            if(a == x){
                check = false;
                break;
            }
        }
        if(check){
            pick.push_back(a);
            counter++;
        }
    }
    int num = 1;
    for(auto x : pick){
        Player player = Player::getPlayer(position, x);
        cout << num << ") " << player.getName() << " " << player.getClub() << " "
             << player.getNation() << " " << player.getLeague() << " " << player.getRating() << endl;
        num++;
    }
    Player::teamAddPlayer(pick[PickPlayer() - 1]);
}
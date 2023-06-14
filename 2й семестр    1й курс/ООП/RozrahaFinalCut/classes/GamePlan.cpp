
#include "GamePlan.h"
#include "Ctrl.h"
#include "Player.h"
#include "GameProcess.h"

void GamePlan::startsGame(){
    Player::createPlayers();
    GameProcess::pickPosition();
    GameProcess::customCout();
    cout << endl;
    GameProcess::setOponent(Player::getTeam());
}
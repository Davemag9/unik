//
// Created by davem on 13.05.2022.
//
#include "Ctrl.h"
#include "Player.h"
#include "GameProcess.h"
#include "QuickGamePlan.h"

void QuickGamePlan::startQuickGame() {
    Player::createPlayers();
    GameProcess::quickTeam();
    GameProcess::quickCustomCout();
    cout << endl;
    GameProcess::setOponent(GameProcess::getQuickTeam());
}
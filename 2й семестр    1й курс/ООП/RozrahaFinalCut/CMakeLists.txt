cmake_minimum_required(VERSION 3.22)
project(RozrahaFinalCut)

set(CMAKE_CXX_STANDARD 17)

add_executable(RozrahaFinalCut main.cpp data/PlrData.data classes/GamePlan.cpp classes/GamePlan.h classes/Ctrl.cpp classes/Ctrl.h classes/Player.cpp classes/Player.h classes/GameMechanic.cpp classes/GameMechanic.h classes/GameProcess.cpp classes/GameProcess.h classes/ClubMember.h classes/Person.h classes/IPlayer.h classes/QuickGamePlan.cpp classes/QuickGamePlan.h)

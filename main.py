import gamedata
import numpy as np

if __name__ == "__main__":
  totalGames = 0
  while 1:
    plays = []
    numPlays = 0
    game = gamedata.gameData(4)
    while 1:
      game.printSituation()
      input("Press enter...")
      move = game.chooseMove()
      print(move.toString())
      if len(plays) > 0:
        plays = np.vstack((plays, game.getPlay(move.index)))
      else:
        plays = game.getPlay(move.index)
      numPlays += 1
      input("Press enter...")
      game.executeMove(move)
      outcome = game.postMove()
      if outcome >= 0:
        break

    if outcome > 100000:
      input("Win "+str(outcome))
    elif outcome >= 0:
      input("Loss "+str(outcome))
    outcomes = np.full((numPlays,1),outcome)
    plays = np.hstack((plays, outcomes))
    np.savetxt("dataset.csv", plays, delimiter=",")

    totalGames += 1
    if totalGames > 1:
      break




  #game.play(2)
  #game.printSituation()
  #game.printDeck()
  #print()
  #game.printPlayers()
import gamedata
import numpy as np

if __name__ == "__main__":
  totalGames = 0
  cont = ""
  while 1:
    plays = []
    numPlays = 0
    game = gamedata.gameData(4)
    while 1:
      #game.printSituation()
      #input("Press enter...")
      move = game.chooseMove()
      print(move.toString())
      if len(plays) > 0:
        plays = np.vstack((plays, game.getPlay(move.index)))
      else:
        plays = game.getPlay(move.index)
      numPlays += 1
      #input("Press enter...")
      game.executeMove(move)
      outcome = game.postMove()
      if outcome >= 0:
        break

    if outcome > 100000 and cont!="just run":
      cont=input("Win "+str(outcome))
    elif outcome >= 0 and cont!="just run":
      cont=input("Loss "+str(outcome))
    if numPlays > 1:
      outcomes = np.full((numPlays,1),outcome)
      plays = np.hstack((plays, outcomes))
    else:
      plays = np.append(plays, [outcome])
    #for play in plays:
    #  print(play)
    #  input("press enter...")
    with open("dataset.csv",'a') as dataFile:
      np.savetxt(dataFile, plays)
    #np.savetxt("dataset.csv", plays, delimiter=",")

    totalGames += 1
    if totalGames > 1000000:
      break




  #game.play(2)
  #game.printSituation()
  #game.printDeck()
  #print()
  #game.printPlayers()
import gamedata
import numpy as np
import hanabiTrainer

def generateData():
  #print("play")
  #return
  totalGames = 0
  totalPlays = 0
  fileSuffix = 0
  cont = ""
  while 1:
    plays = []
    numPlays = 0
    game = gamedata.gameData(4)
    while 1:
      #game.printSituation()
      #input("Press enter...")
      move = game.chooseMove()
      #print(move.toString())
      onePlay = game.getPlay(move.index)
      if len(plays) > 0:
        #plays = np.vstack((plays, game.getPlay(move.index)))
        plays = np.vstack((plays, onePlay))
      else:
        plays = onePlay#game.getPlay(move.index)
      #print(onePlay)
      #print("huh")
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
    totalPlays += numPlays
    #for play in plays:
    #  print(play)
    #  input("press enter...")
    with open("dataset"+str(fileSuffix)+".csv",'a') as dataFile:
      np.savetxt(dataFile, plays)
    #np.savetxt("dataset.csv", plays, delimiter=",")

    totalGames += 1
    #if totalGames > 1000000:
    #  break
    if totalPlays > 2:
      break

if __name__ == "__main__":
  todo = input("Play or train?\n")
  if todo.upper() == "PLAY":
    generateData()
  elif todo.upper() == "TRAIN":
    trainer = hanabiTrainer.hanabiTrainer()
    trainer.loadData()
  else:
    print("Don't be an idiot, Dwigt\n")



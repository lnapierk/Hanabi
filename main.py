import gamedata

if __name__ == "__main__":
  totalGames = 0
  while 1:
    game = gamedata.gameData(4)
    while 1:
      game.printSituation()
      input("Press enter...")
      move = game.chooseMove()
      print(move.toString())
      print(game.getPlay(move.index))
      input("Press enter...")
      game.executeMove(move)
      outcome = game.postMove()
      if outcome >= 0:
        break

    if outcome > 100000:
      input("Win "+str(outcome))
    elif outcome >= 0:
      input("Loss "+str(outcome))
    
    totalGames += 1
    if totalGames > 10000000:
      break




  #game.play(2)
  #game.printSituation()
  #game.printDeck()
  #print()
  #game.printPlayers()
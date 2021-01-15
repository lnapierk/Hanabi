import gamedata

if __name__ == "__main__":
  game = gamedata.gameData(4)
  while 1:
    move = game.chooseMove()
    
  
  game.printDeck()
  print()
  game.printPlayers()
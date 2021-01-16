import gamedata

if __name__ == "__main__":
  game = gamedata.gameData(4)
  while 1:
    game.printSituation()
    input("Press enter...")
    move = game.chooseMove()
    print(move.toString())
    input("Press enter...")
    game.executeMove(move)
    outcome = game.postMove()
    if outcome != 0:
      break

if outcome == -1:
  print("Loss")
if outcome == 1:
  print("Win")

  #game.play(2)
  #game.printSituation()
  #game.printDeck()
  #print()
  #game.printPlayers()
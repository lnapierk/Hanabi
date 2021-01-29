import structures as st
import random
import numpy as np

class gameData:
  def __init__(self, numPlayers):
    random.seed()
    if numPlayers > 5 or numPlayers < 2:
      raise Exception
    self.numPlayers = numPlayers
    if numPlayers > 3:
      self.numCards = 4
    else:
      self.numCards = 5

    self.turnLimit = None
    self.clues = 8
    self.bombs = 3

    self.deck = st.Deck()

    self.players = []
    for i in range(0, self.numPlayers):
      self.players.append(st.Player("PLAYER "+str(i+1)))
      for j in range(0, self.numCards):
        self.players[i].draw(self.deck)

    self.active = random.randint(0, numPlayers-1)
    self.turnsTaken = 0

    self.discards = {}
    for color in st.Color:
      self.discards[color.value] = [0,0,0,0,0]
      for num in st.realValues:
        self.discards[color.value][num-1]+=1
    self.table = {}
    for color in st.Color:
      self.table[color] = 0

  def chooseMove(self):
    player = self.players[self.active]
    totalMoves = (player.handSize * 2)
    if self.clues > 0:
      totalMoves += (2*((self.numPlayers-1)*5))
    choice = random.randrange(0, totalMoves)
    ogChoice = choice
    if choice < player.handSize:
      move = st.Play(choice, ogChoice)
      return move
    elif choice < (player.handSize * 2):
      move = st.Discard(choice-player.handSize, ogChoice)
      return move
    else:
      choice -= (player.handSize*2)
      clueRecipient = (choice//(10))+1
      contentChoice = choice%10
      if contentChoice == 0: 
        clueContent = st.Color.Blue
      elif contentChoice == 1:
        clueContent = st.Color.Red
      elif contentChoice == 2:
        clueContent = st.Color.Green
      elif contentChoice == 3:
        clueContent = st.Color.White
      elif contentChoice == 4:
        clueContent = st.Color.Yellow
      elif contentChoice == 5:
        clueContent = 1
      elif contentChoice == 6:
        clueContent = 2
      elif contentChoice == 7:
        clueContent = 3
      elif contentChoice == 8:
        clueContent = 4
      elif contentChoice == 9:
        clueContent = 5
      move = st.Clue(clueRecipient, clueContent, ogChoice)
      return move

  def getPlay(self, selection):
    playArray = []
    player = self.players[self.active]
    for j in range(0, self.numCards):
      if j < player.handSize:
        card = player.hand[j]
        tempArray = self.getCardArray(card, True)
        #print(tempArray)
      playArray = np.append(playArray, tempArray)

    for i in range(1,self.numPlayers):
      playerIndex = (self.active+i)%self.numPlayers
      player = self.players[playerIndex]
      for j in range(0, player.handSize):
        if j < player.handSize:
          card = player.hand[j]
          tempArray = self.getCardArray(card, False)
        #print(tempArray)
        playArray = np.append(playArray, tempArray)
    
    tempArray = (self.getDiscardArray())/3
    playArray = np.append(playArray, tempArray)
    return playArray

  def getCardArray(self, card, isSelf):
    if isSelf==True:
      tempArray = np.zeros(10)
    else:
      tempArray = np.zeros(12)
    if card.colorKnown or isSelf==False:
      if card.color == st.Color.Blue: 
        tempArray[0] = 1
      elif card.color == st.Color.Red:
        tempArray[1] = 1
      elif card.color == st.Color.Green:
        tempArray[2] = 1
      elif card.color == st.Color.White:
        tempArray[3] = 1
      elif card.color == st.Color.Yellow:
        tempArray[4] = 1
    if card.valueKnown or isSelf==False:
      if card.value == 1:
        tempArray[5] = 1
      elif card.value == 2:
        tempArray[6] = 1
      elif card.value == 3:
        tempArray[7] = 1
      elif card.value == 4:
        tempArray[8] = 1
      elif card.value == 5:
        tempArray[9] = 1
    if isSelf==False:
      if card.colorKnown:
        tempArray[10] = 1
      if card.valueKnown:
        tempArray[11] = 1
    return tempArray

  def getDiscardArray(self):
    outArray = []
    for color in st.Color:
      outArray = np.append(outArray, self.discards[color.value])
    print(outArray)
    return outArray

  def executeMove(self, move):
    if isinstance(move, st.Play):
      self.play(move.whichCard)
    elif isinstance(move, st.Clue):
      self.giveClue(move.player, move.clue)
    elif isinstance(move, st.Discard):
      self.discard(move.whichCard)

  def play(self, whichCard):
    player = self.players[self.active]
    card = player.discard(whichCard)
    player.draw(self.deck)
    if self.table[card.color] == (card.value - 1):
      self.table[card.color] = card.value
      if card.value == 5 and self.clues < 8:
        self.clues += 1
    else:
      self.bombs -= 1
      self.discards[card.color.value][card.value-1]-=1
    
  def giveClue(self, recipient, clue):
    if self.clues < 1:
      return
    absIndex = (self.active+recipient)%self.numPlayers
    receiver = self.players[absIndex]
    if isinstance(clue, st.Color):
      for card in receiver.hand:
        if card.color == clue:
          card.colorKnown = True
    else:
      for card in receiver.hand:
        if card.value == clue:
          card.valueKnown = True
    self.clues -= 1

  def discard(self, index):
    player = self.players[self.active]
    card = player.discard(index)
    player.draw(self.deck)
    self.discards[card.color.value][card.value-1]-=1
    if self.clues < 8:
      self.clues += 1

  def postMove(self):
    self.active += 1
    self.active = self.active % self.numPlayers
    if self.deck.size < 1:
      if self.turnLimit > 0:
        self.turnLimit -= 1
      else:
        self.turnLimit = self.numPlayers
    if self.checkWin():
      return 100000000+self.scoreGame()
    if self.checkLose():
      return self.scoreGame()
    return -1

  def scoreGame(self):
    total = 0
    for color in st.Color:
      total += self.table[color]
    return total

  def checkWin(self):
    for color in st.Color:
      if self.table[color]!=5:
        return False
    return True

  def checkLose(self):
    if self.bombs < 1:
      return True
    if self.turnLimit == 0:
      return True
    for color in st.Color:
      for num in st.possibleValues:
        if self.discards[color.value][num-1] < 1:
          return True
    return False

  def printDeck(self):
    print("DECK")
    print(self.deck.size)
    for i in range(0, self.deck.size):
      card = self.deck.cards[i]
      print(str(i+1)+". ", end="")
      print(card.toString())

  def printPlayers(self):
    for i in range(0, self.numPlayers):
      player = self.players[i]
      print(player.name + " - " + str(player.handSize) + " Cards")
      for j in range(0, player.handSize):
        print(player.hand[j].toString())
      print()

  def printBombs(self):
    print("BOMBS: " + str(self.bombs))

  def printClues(self):
    print("CLUES: " + str(self.clues))

  def printTurns(self):
    if self.turnLimit:
      print(str(self.turnLimit)+"TURNS REMAINING")
  
  def printWhosUp(self):
    print(self.players[self.active].name + " plays next")

  def printTable(self):
    print("BOARD")
    for color in st.Color:
      print(color.value+": "+str(self.table[color]))

  def printSituation(self):
    self.printTable()
    print()
    self.printWhosUp()
    self.printClues()
    self.printTurns()
    self.printBombs()
    print()
    self.printPlayers()
    self.printDeck()

  def printDiscards(self):
    for color in st.Color:
      for num in st.possibleValues:
        print(color.value+" "+str(num)+": "+self.discards[color][num-1])
  
        



    

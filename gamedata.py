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

  def chooseMove(self):#select a play to make
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

  def getLabels(self):
    outArray = []
    for j in range(0, self.numCards):
      outArray = np.append(outArray, ["SelfCard"+str(j)+"Color", "SelfCard"+str(j)+"Number"])
    for k in range(1, self.numPlayers):
      for i in range(0, self.numCards):
        outArray = np.append(outArray, ["Player"+str(k)+"Card"+str(i)+"Color","Player"+str(k)+"Card"+str(i)+"ColorKnown","Player"+str(k)+"Card"+str(i)+"Number","Player"+str(k)+"Card"+str(i)+"NumberKnown"])
    for color in st.Color:
      outArray = np.append(outArray,[color.value+str(1)+"s",color.value+str(2)+"s",color.value+str(3)+"s",color.value+str(4)+"s",color.value+str(5)+"s"])
    for color in st.Color:
      outArray = np.append(outArray,[color.value+"Played"])
    outArray = np.append(outArray, ["DeckSize","Clues","Bombs","Turns","Move","Score"])
    return outArray

  def getPlay(self, selection):#get the full array representing a move and situation
    playArray = []
    player = self.players[self.active]
    for j in range(0, self.numCards):# go through your own cards
      if j < player.handSize:
        card = player.hand[j]
        tempArray = self.getCardArraySimple(card, True)
        #print(tempArray)
      else:
        tempArray = ["none", "none"]
      playArray = np.append(playArray, tempArray)

    for i in range(1,self.numPlayers):# go through other players
      playerIndex = (self.active+i)%self.numPlayers
      player = self.players[playerIndex]
      for j in range(0, self.numCards):
        if j < player.handSize:
          card = player.hand[j]
          tempArray = self.getCardArraySimple(card, False)
        #print(tempArray)
        playArray = np.append(playArray, tempArray)
    
    #tempArray = self.getDiscardArray()/3
    tempArray = self.getDiscardArraySimple()
    playArray = np.append(playArray, tempArray)
    playArray = np.append(playArray, self.getTableArraySimple())
    playArray = np.append(playArray, self.getMiscArraySimple())
    #tempArray = np.zeros((player.handSize * 2)+(2*((self.numPlayers-1)*5)))
    #tempArray[selection-1] = 1
    #playArray = np.append(playArray, tempArray)
    playArray = np.append(playArray, [str(selection)])
    return playArray

  def getCardArraySimple(self, card, isSelf):
    colorVal = card.color.value
    numberVal = str(card.value)
    if isSelf == True:
      if card.colorKnown == False:
        colorVal = "unknown"
      if card.valueKnown == False:
        numberVal = "unknown"
      return [colorVal, numberVal]

    return [colorVal, str(card.colorKnown), numberVal, str(card.valueKnown)]
  def getCardArray(self, card, isSelf):#get the array representing the cards in a player's hand
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

  def getDiscardArray(self):#get the array of discarded cards
    outArray = []
    for color in st.Color:
      outArray = np.append(outArray, self.discards[color.value])
    #print(outArray)
    return outArray

  def getDiscardArraySimple(self):#get the array of discarded cards
    outArray = []
    for color in st.Color:
      for discard in self.discards[color.value]:
        outArray = np.append(outArray, [str(discard/3)])
    #print(outArray)
    return outArray

  def getTableArray(self):#get the array of played cards
    output = []
    for color in st.Color:
      tempArray = np.zeros(5)
      if self.table[color] != 0:
        tempArray[self.table[color]-1] = 1
      output = np.append(output, tempArray)
      #input(tempArray)
    return output

  def getTableArraySimple(self):#get the array of played cards
    output = []
    for color in st.Color:
      output = np.append(output, [str(self.table[color])])
      #input(tempArray)
    return output

  def getMiscArray(self):#get the array with clues, bombs, turns remaining, and the deck size
    deckSize = self.deck.size
    deckSize = deckSize / (50 - (self.numCards*self.numPlayers))  
    clues = self.clues / 8
    bombs = self.bombs / 3
    if self.turnLimit == None:
      turns = 1
    else:
      turns = self.turnLimit / self.numPlayers
    return [deckSize, clues, bombs, turns]

  def getMiscArraySimple(self):#get the array with clues, bombs, turns remaining, and the deck size
    deckSize = self.deck.size
    deckSize = str(deckSize / (50 - (self.numCards*self.numPlayers)))  
    clues = str(self.clues/8)
    bombs = str(self.bombs/3)
    if self.turnLimit == None:
      turns = "inf"
    else:
      turns = str(self.turnLimit/self.numPlayers)
    output = [deckSize, clues, bombs, turns]
    #print(output)
    return output

  def executeMove(self, move):#carry out a move
    if isinstance(move, st.Play):
      self.play(move.whichCard)
    elif isinstance(move, st.Clue):
      self.giveClue(move.player, move.clue)
    elif isinstance(move, st.Discard):
      self.discard(move.whichCard)

  def play(self, whichCard):#play a card
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
    
  def giveClue(self, recipient, clue):#give a clue
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

  def discard(self, index):#discard
    player = self.players[self.active]
    card = player.discard(index)
    player.draw(self.deck)
    self.discards[card.color.value][card.value-1]-=1
    if self.clues < 8:
      self.clues += 1

  def postMove(self):#actions to be taken after a move
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

  def scoreGame(self):#calculate the score based on played cards
    total = 0
    for color in st.Color:
      total += self.table[color]
    return total

  def checkWin(self):#check if the game has been won
    for color in st.Color:
      if self.table[color]!=5:
        return False
    return True

  def checkLose(self):#check if the game has been lost
    if self.bombs < 1:
      return True
    if self.turnLimit == 0:
      return True
    for color in st.Color:
      for num in st.possibleValues:
        if self.discards[color.value][num-1] < 1:
          return True
    return False

  def printDeck(self):#print the cards in the deck for debugging
    print("DECK")
    print(self.deck.size)
    for i in range(0, self.deck.size):
      card = self.deck.cards[i]
      print(str(i+1)+". ", end="")
      print(card.toString())

  def printPlayers(self):#print players' hands
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
  
        



    

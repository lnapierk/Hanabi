import structures as st
import random

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
    self.turnHistory = []

    self.discards = []
    self.table = {}
    for color in st.Color:
      self.table[color] = 0

  def chooseMove(self):
    player = self.players[self.active]
    totalMoves = (player.handSize * 2)
    if self.clues > 0:
      totalMoves += (2*((len(self.numPlayers)-1)*5))
    choice = random.randrange(0, totalMoves)
    if choice < self.handSize:
      move = st.Play(choice)
      return move
    elif choice < (self.handSize * 2):
      move = st.Discard(choice-self.handSize)
      return move
    else:
      choice -= (self.handSize*2)
      clueRecipient = choice//(self.numPlayers-1)
      switch (choice%10){
        case 0: 
          clueContent = st.Color.Blue
          break
        case 1:
          clueContent = st.Color.Red
          break
        case 2:
          clueContent = st.Color.Green
          break
        case 3:
          clueContent = st.Color.White
          break
        case 4:
          clueContent = st.Color.Yellow
          break
        case 5:
          clueContent = 1
          break
        case 6:
          clueContent = 2
          break
        case 7:
          clueContent = 3
          break
        case 8:
          clueContent = 4
          break
        case 9:
          clueContent = 5
          break
      }
      move = st.Clue(clueRecipient, clueContent)
      return move

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

  
        



    

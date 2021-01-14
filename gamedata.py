import structures as st

class gameData:
  def __init__(self, numPlayers):
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
      self.players.append(st.Player())
      for j in range(0, self.numCards):
        self.players[i].draw(self.deck)

    self.discards = []
    self.table = {}
    for color in st.Color:
      self.table[color] = 0

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
      print("PLAYER " + str(i+1) + " - " + str(player.handSize) + " Cards")
      for j in range(0, player.handSize):
        print(player.hand[j].toString())
      print()

  
        



    

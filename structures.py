from enum import Enum
import random

class Color(Enum):
  Blue = "Blue"
  Red = "Red"
  Green = "Green"
  White = "White"
  Yellow = "Yellow"

possibleValues = range(1,6)
realValues = [1,1,1,2,2,3,3,4,4,5]

class Card:
  def __init__(self, color, value):
    self.color = color
    self.value = value
    self.colorKnown = False
    self.valueKnown = False
  
  def toString(self):
    colorK = ""
    valueK = ""
    if self.colorKnown:
      colorK = "(k)"
    if self.valueKnown:
      valueK = "(k)"
    return self.color.value+colorK+" "+str(self.value)+valueK

class Deck:
  def __init__(self):
    self.cards = []
    for num in realValues:
      for hue in Color:
        self.cards.append(Card(hue,num))
    random.shuffle(self.cards)
    self.size = len(self.cards)
  
  def dispense(self):
    if self.size > 0:
      self.size -= 1
      return self.cards.pop()
    else:
      return None


class Player:
  def __init__(self, name):
    self.hand = []
    self.handSize = 0
    self.name = name
  
  def draw(self, deck):
    newCard = deck.dispense()
    if newCard != None:
      self.hand.append(newCard)
      self.handSize += 1

  def discard(self, index):
    if index >= self.handSize:
      return None
    card = self.hand[index]
    del self.hand[index]
    self.handSize -= 1
    return card

class Move:
  def toString(self):
    return "{Action: Nothing}"

class Discard(Move):
  def __init__(self, number, index):
    self.whichCard = number
    self.index = index
  def toString(self):
    return "{Action: Discard,Card: "+str(self.whichCard)+"}"

class Play(Move):
  def __init__(self, number, index):
    self.index = index
    self.whichCard = number
  def toString(self):
    return "{Action: Play,Card: "+str(self.whichCard)+"}"

class Clue(Move):
  def __init__(self, player, clue, index):
    self.index = index
    self.player = player
    self.clue = clue
  def toString(self):
    actionStr = "Action: Clue"
    playerStr = "Player: "+str(self.player)
    if isinstance(self.clue, Color):
      clueStr = "Clue: "+self.clue.value
    else:
      clueStr = "Clue: "+str(self.clue)
    return "{"+actionStr+","+playerStr+","+clueStr+"}"
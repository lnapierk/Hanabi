from enum import Enum
import random

class Color(Enum):
  Blue = "Blue"
  Red = "Red"
  Green = "Green"
  White = "White"
  Yellow = "Yellow"

class MoveType(Enum):
  Discard = "Discard"
  Play = "Play"
  Clue = "Clue"

possibleValues = range(1,6)
realValues = [1,1,1,2,2,3,3,4,4,5]

class Card:
  def __init__(self, color, value):
    self.color = color
    self.value = value
    self.colorKnown = False
    self.valueKnown = False
  
  def toString(self):
    return self.color.value+" "+str(self.value)

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

class Move:
  pass

class Discard(Move):
  def __init__(self, number):
    self.whichCard = number
    self.type = MoveType.Discard

class Play(Move):
  def __init__(self, number):
    self.whichCard = number

class Clue(Move):
  def __init__(self, player, clue):
    self.player = player
    self.clue = clue
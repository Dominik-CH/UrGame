import random

class Game:
    def __init__(self):
        self.matchfield = self.populateMatchfield()
        self.PlayerTurn = 0 # 0 White 1 Black
        self.Player1Stones = self.createStones(0) #White Stones
        self.Player2Stones = self.createStones(1) #Black Stones
        self.Player1StonesFinished = 0
        self.Player2StonesFinished = 0
        self.Won = False
    def populateMatchfield(self): #Erstellt die 3x8 Matrix
        matchfield = []
        for fieldheight in range(3):
            matchfield.append([])
            for fieldwidth in range(8):
                matchfield[fieldheight].append(Field(fieldheight,fieldwidth))
        for row in matchfield:
            for x in row:
                print(x.rose,end=" ")
            print()
        return matchfield

    def switchPlayerTurn(self):
        if self.PlayerTurn == 0:
            self.PlayerTurn = 1
        else:
            self.PlayerTurn = 0
    def rollDice(self):
        rolls = []
        total = 0
        for roll in range(4):
            oneOrzero = random.randint(0,1)
            rolls.append(oneOrzero)
            total += oneOrzero
        rolls.append(total) #First 4 Elements resemble diceroll 5th is the total value calculated
        print(rolls)
        return rolls

    def createStones(self,color):
        stones = []
        for stone in range(7):
            stones.append(Stone(color))
        return stones
    def stonesFinished(self):
        player1Finished = 0
        player2Finished = 0
        for stones1 in self.Player1Stones:
            if(stones1.finished == True):
                player1Finished +=1
        for stones2 in self.Player2Stones:
            if(stones2.finished == True):
                player2Finished +=1

        if player1Finished > self.Player1StonesFinished:
            self.Player1StonesFinished = player1Finished

        if player2Finished > self.Player2StonesFinished:
            self.Player2StonesFinished = player2Finished

    def renderMatchfield(self):
        for row in self.matchfield:
            for element in row:
                if element.color == 0:
                    print("X",end=" ")
                if element.color == 1:
                    print("O",end=" ")
                else:
                    print("E",end=" ")
            print()



class Field:
    def __init__(self,yPos,xPos):
        self.xPos = xPos
        self.yPos = yPos
        self.occupied = False
        self.color = 2 #To if a field is blank
        self.rose = self.AmIRose(yPos,xPos)

    def AmIRose(self,yPos,xPos):
        if xPos == 0 and yPos == 0:
            return True
        if xPos == 6 and yPos == 0:
            return True

        if xPos == 0 and yPos == 2:
            return True
        if xPos == 6 and yPos == 2:
            return True

        if xPos == 3 and yPos == 1:
            return True

        return False

    def MovedToField(self,PlayerColor):
        self.occupied = True
        self.color = PlayerColor

class Stone:
    def __init__(self,color,xPos=None,yPos=None):
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.safe = True
        self.finished = False
    def isSafe(self): #Determines if a Stone is in a safe Zone (Drawing)
        if self.yPos == 0:
            return True
        if self.yPos == 2:
            return True
        if self.xPos == 3 and self.yPos == 1:
            return True
        else:
            return False




game = Game()
game.rollDice()
game.renderMatchfield()
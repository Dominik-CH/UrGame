import random

class Game:
    def __init__(self):
        self.matchfield = self.populateMatchfield()
        self.moveField = self.populateMovefield()
        self.PlayerTurn = 0 # 0 White 1 Black
        self.Player1Stones = self.createStones(0) #White Stones
        self.Player2Stones = self.createStones(1) #Black Stones
        self.Player1StonesFinished = 0
        self.Player2StonesFinished = 0

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

    def populateMovefield(self):
        moveField = []
        for fieldnumber in range(14):
            moveField.append(LineField(fieldnumber))
        return moveField

    def start(self):
        print("Im Start")

        #while True:  #Diese Schleife muss später den gesamten Code hier umschließen--> Geht solange bis jemand gewonnen hat
        #if (self.gameFinished() == 0) or (self.gameFinished() == 1):
        #    break

        print("Diceroll")
        roll = self.rollDice()[4] #Forth Element of List is the total amount of steps
        self.showPossibleMoves(roll)

        self.renderAllMovefield()

        self.switchPlayerTurn()

    def showPossibleMoves(self,roll):

        if roll == 0: #Nothing possible with 0, --> Skip
            return

        newStonePossible = self.isNewStonePossible(roll)



    def isNewStonePossible(self,roll):
        roll -=1 #Adjusting to the array 4 -> 3, because 0,1,2,3
        print(roll)
        return False

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

    def gameFinished(self):
        if self.Player1StonesFinished == 7:
            print("Player 1 Won")
            return 0 #SPieler 1 gewonnen
        elif self.Player2StonesFinished == 7:
            print("Player 2 Won")
            return 1 #Spieler 2 geownnen



    def renderAllMovefield(self):

        for element in self.moveField:
            if element.color == 0:
                print("X",end=" ")
            elif element.color == 1:
                print("O",end=" ")
            else:
                print("E",end=" ")
        print()

        for element in self.moveField:
            if element.isPossibleDouble:
                print("True",end=" ")
            else:
                print("False",end=" ")
        print()

        for element in self.moveField:
            if element.isRose:
                print("True",end=" ")
            else:
                print("False",end=" ")
        print()

        for element in self.moveField:
            if element.isSafeField:
                print("True",end=" ")
            else:
                print("False",end=" ")
        print()

        for element in self.moveField:
            print(element.fieldNumber,end=" ")


    def renderMatchfield(self): #Erst nach der MoveField implementiernug notwenidg, dann mit den aufgezeigten fkt im kommentar
        # Muss zum rendern dann durch den moveField laufen und schauen auf welchen Felder was steht. Bei doppelter belegung eben unterschied zw. 1 und 2
        for row in self.matchfield:
            for element in row:
                if element.color == 0:
                    print("X",end=" ")
                elif element.color == 1:
                    print("O",end=" ")
                else:
                    print("E",end=" ")
            print()



class Field: #Könnte in dieser Form noch sinnvoll für die spätere ausgabe des gerenderten Feld z.b. wenn im Gui Felder untersch. DEsigns haben
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

class LineField():
    def __init__(self,fieldNumber):
        self.color = 2  #Blank
        self.fieldNumber = fieldNumber
        self.occupiedWhite = False
        self.occupiedBlack = False
        self.isPossibleDouble = self.possibleDoubleOcc()#Schaut ob 2 auf dem Feld stehen können aka Schwarz und weiß KEINE GLEICHEN FARBEN
        self.isSafeField = self.isSafe()
        self.isRose = self.AmIRose()


    def isSafe(self):
        if self.fieldNumber < 4:
            return True
        if (self.fieldNumber ==12) or (self.fieldNumber ==13):
            return True
        if self.fieldNumber == 7: #Mittleres Feld welches Sicher ist
            return True
        return False

    def possibleDoubleOcc(self):    #Überprüft ob man doppelt auf einem Feld sein kann
        if self.fieldNumber < 4:
            return True
        if (self.fieldNumber ==12) or (self.fieldNumber ==13):
            return True

        return False #Kriegerische Zone von 4-11

    def AmIRose(self): #Schauen ob man nochmal Würfeln darf
        if self.fieldNumber == 3:
            return True
        if self.fieldNumber == 7:
            return True
        if self.fieldNumber == 13:
            return True
        return False


class Stone:
    def __init__(self,color,xPos=None,yPos=None):
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.safe = False
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
game.renderMatchfield()
game.start()

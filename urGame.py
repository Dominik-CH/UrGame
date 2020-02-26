import random


class Game:
    def __init__(self):
        self.matchfield = self.populateMatchfield()
        self.moveField = self.populateMovefield()
        self.PlayerTurn = 0  # 0 White 1 Black
        self.Player1Stones = self.createStones(0)  # White Stones
        self.Player2Stones = self.createStones(1)  # Black Stones
        self.Player1StonesFinished = 0
        self.Player2StonesFinished = 0
        self.Player1StonesOnField = 0
        self.Player2StonesOnField = 0

    def populateMatchfield(self):  # Erstellt die 3x8 Matrix
        matchfield = []
        for fieldheight in range(3):
            matchfield.append([])
            for fieldwidth in range(8):
                matchfield[fieldheight].append(Field(fieldheight, fieldwidth))
        return matchfield

    def populateMovefield(self):
        moveField = []
        for fieldnumber in range(14):
            moveField.append(LineField(fieldnumber))
        return moveField

    def start(self):
        print("Im Start")

        # while True:  #Diese Schleife muss später den gesamten Code hier umschließen--> Geht solange bis jemand gewonnen hat
        # if (self.gameFinished() == 0) or (self.gameFinished() == 1):
        #    break
        while (self.Player1StonesFinished != 7) or (self.Player1StonesFinished !=0):
            if self.PlayerTurn == 0:
                print("Weiß")
            if self.PlayerTurn == 1:
                print("Schwarz")
            print()
            while True: #break benötigt wenn Feld keine Rose ist
                roll = self.rollDice()[4]  # Forth Element of List is the total amount of steps

                move2make = self.showPossibleMoves(roll)
                self.moveStone(move2make)
                self.renderMovefield()
                if self.checkIfRoll(move2make)!=True: #Wenn man nicht auf der Rose ist darf auch nicht nochmal gewürfelt werden
                    break

            self.switchPlayerTurn()

    def movesDialog(self,possibilities):
        count = 1 #Beginnt bei 1 für den User aber in der Liste dann bei 0
        if len(possibilities) != 0:
            for possible in possibilities:
                if possible[0] != None:
                    print(count, "\t Von ", possible[0]+1, "bis ", possible[1]+1)   #Die +1 weil ein nutzer von 1 beginnt zu zählen und nicht 0
                else:
                    print(count, "\t Von ", possible[0], "bis ", possible[1] + 1)
                count += 1
            selection = int(input("Welchen move willst du machen? Nur INT!\n"))-1  # Muss ein Int sein.    -1 um den echten Index an der 1. Stelle zu bekommen
            #Keine Abfrage ob man außerhalb der Liste ist vom Index her weil es nicht bei der textbasierten Form bleibt
            return possibilities[selection]
        else:
            return None


    def showPossibleMoves(self, roll):
        if roll == 0:  # Nothing possible with 0, --> Skip
            return
        # Hier tritt der Fehler auf: Nur bei neuem Stein wird einer abgezogen sonst nicht. roll -= 1  # Adjusting to the array 4 -> 3, because 0,1,2,3
        newStonePossible = self.isNewStonePossible(roll-1)  #Null wird mitgezählt
        print(newStonePossible)
        possibilities = self.movesOtherStones(roll)
        if newStonePossible == True:
            possibilities.append([None,roll-1])

        print(possibilities)  # Soll später so sein, dass über Stein gehovert wird und man angezeigt bekommt welchen weg man nimmt

        move2make = self.movesDialog(possibilities)
        return move2make

    def movesOtherStones(self,
                         roll):  # Zeigt nur an welche Felder rein theoretisch möglich sind. Noch nichts wird bewegt
        possibleMoves = []
        print("Roll: ", roll)
        fieldCount = 0  # Bei welchem Feld man sich momentan befindet Max 13
        for field in self.moveField:
            if self.PlayerTurn == 0:
                # print("Player 1")
                if field.occupiedWhite == True:  # Feld finden auf dem ein Stein von dir steht
                    # print(fieldCount)
                    if roll + fieldCount < 14:
                        if (self.moveField[fieldCount + roll].occupiedWhite != True):  # Muss 14 sein, da man einen mehr braucht als es Felder gibt um ins Ziel zu kommen
                            if (roll + fieldCount == 7) and (self.moveField[7].occupiedBlack == True):
                                print("Schwarz besetzt den Safespace")
                            else:
                                print("Appended possible Move to list")
                                possibleMoves.append(
                                    [fieldCount, fieldCount + roll])  # Von welchem Feld man ausgeht zur End Destination


            else:
                # print("Player 2")
                if field.occupiedBlack == True:  # Feld finden auf dem ein Stein von dir steht
                    # print(fieldCount)
                    if roll + fieldCount < 14:
                        if (self.moveField[fieldCount + roll].occupiedBlack != True):  # Muss 14 sein, da man einen mehr braucht als es Felder gibt um ins Ziel zu kommen
                            if (roll + fieldCount == 7) and (self.moveField[7].occupiedWhite == True):
                                print("Weiß besetzt den Safespace")
                            else:
                                print("Appended possible Move to list")
                                possibleMoves.append(
                                    [fieldCount, fieldCount + roll])  # Von welchem Feld man ausgeht zur End Destination

            fieldCount += 1
        return possibleMoves

    def moveStone(self,toMove): #Liste mit 2 Elementen Anfangspunkt und Endpunkt
        if toMove == None:  #Wenn es einfach keine Möglichkeit gibt von den Figuren etc her
            return
        if toMove[0] == None: #Also neuer Stein wird gesetzt
            if self.PlayerTurn == 0:    #Spieler 1 also weiß
                self.moveField[toMove[1]].occupiedWhite = True
                self.Player1StonesOnField += 1
            else:
                self.moveField[toMove[1]].occupiedBlack = True
                self.Player2StonesOnField += 1
        else:
            #Abfrage ob geschmissen wird einfügen
            if self.PlayerTurn == 0:    #Spieler 1 also weiß
                if self.checkIfFinish(toMove) == False:
                    self.moveField[toMove[0]].occupiedWhite = False
                    self.moveField[toMove[1]].occupiedWhite = True
                    self.checkIfKilled(toMove)
                else:   #Wenn finsihed dann wird nur der ursprüngliche Punkt auf false gesetzt
                    self.moveField[toMove[0]].occupiedWhite = False
            else:
                if self.checkIfFinish(toMove) == False:
                    self.moveField[toMove[0]].occupiedBlack = False
                    self.moveField[toMove[1]].occupiedBlack = True
                    self.checkIfKilled(toMove)
                else:   #Wenn finsihed dann wird nur der ursprüngliche Punkt auf false gesetzt
                    self.moveField[toMove[0]].occupiedBlack = False

    def checkIfKilled(self, toMove):
        if toMove == None:  #Wenn es einfach keine Möglichkeit gibt von den Figuren etc her
            return
        destination = toMove[1]
        if self.PlayerTurn == 0:
            if (self.moveField[destination].isSafe() == False) and (self.moveField[destination].occupiedBlack == True):
                self.Player2StonesOnField -=1
                self.moveField[destination].occupiedBlack = False #Den Stein von dem Feld schlagen
                print("SPIELR GESHCLAGEN")
        else:
            if (self.moveField[destination].isSafe() == False) and (self.moveField[destination].occupiedWhite == True):
                self.Player1StonesOnField -= 1
                self.moveField[destination].occupiedWhite = False  # Den Stein von dem Feld schlagen
                print("SPIELR GESHCLAGEN")

    def checkIfFinish(self, toMove):
        if toMove == None:  #Wenn es einfach keine Möglichkeit gibt von den Figuren etc her
            False
        if self.PlayerTurn == 0:
            if toMove[0] + toMove[1] == 15:
                self.Player1StonesOnField -=1
                self.Player1StonesFinished +=1
                return True
            else:
                return False
        else:
            if toMove[0] + toMove[1] == 15:
                self.Player2StonesOnField -= 1
                self.Player2StonesFinished += 1
                return True
            else:
                return False


    def checkIfRoll(self,toMove):
        if toMove == None:  #Wenn es einfach keine Möglichkeit gibt von den Figuren etc her
            return False
        destination = toMove[1]
        if self.moveField[destination].isRose == True:
            print("NOCHMAL WÜRFELN")
            return True
        return False

    def applyMoveFieldToMatchfield(self):
        pass

        # Wenn [0] und [1] == 15 sind setzt man den Stones Finished auf +1 dann stones on board auf -1
    def isNewStonePossible(self, roll):
        #roll-=1 #Nur hier wird einer abgezogen weil man das nullte Feld mitzählen muss ansonsten wird normal der roll addiert bei self.moveStones
        if self.PlayerTurn == 0:
            if self.Player1StonesFinished + self.Player1StonesOnField == 7:  # Kann nicht größer sein als 7, da maximal 7 Steine im Spiel sind von einer Farbe
                return False
            if (self.moveField[roll].occupiedWhite == True):
                return False
        else:
            if self.Player2StonesFinished + self.Player2StonesOnField == 7:  # Kann nicht größer sein als 7, da maximal 7 Steine im Spiel sind von einer Farbe
                return False
            if (self.moveField[roll].occupiedBlack ==  True):
                return False
        return True  # Wenn kein Stein der gleichen Farbe auf dem Feld liegt kann der Zug ausgeführt werden



    def switchPlayerTurn(self):
        if self.PlayerTurn == 0:
            self.PlayerTurn = 1
        else:
            self.PlayerTurn = 0

    def rollDice(self):
        rolls = []
        total = 0
        for roll in range(4):
            oneOrzero = random.randint(0, 1)
            rolls.append(oneOrzero)
            total += oneOrzero
        rolls.append(total)  # First 4 Elements resemble diceroll 5th is the total value calculated
        print(rolls)
        return rolls

    def createStones(self, color):
        stones = []
        for stone in range(7):
            stones.append(Stone(color))
        return stones

    def stonesFinished(self):
        player1Finished = 0
        player2Finished = 0
        for stones1 in self.Player1Stones:
            if (stones1.finished == True):
                player1Finished += 1
        for stones2 in self.Player2Stones:
            if (stones2.finished == True):
                player2Finished += 1

        if player1Finished > self.Player1StonesFinished:
            self.Player1StonesFinished = player1Finished

        if player2Finished > self.Player2StonesFinished:
            self.Player2StonesFinished = player2Finished

    def gameFinished(self):
        if self.Player1StonesFinished == 7:
            print("Player 1 Won")
            return 0  # SPieler 1 gewonnen
        elif self.Player2StonesFinished == 7:
            print("Player 2 Won")
            return 1  # Spieler 2 geownnen


    def renderMovefield(self):
        print("Mit weiß belegt")
        for element in self.moveField:
            if element.occupiedWhite == True:
                print("X", end=" ")
            else:
                print("E", end=" ")
        print()
        print("Mit schwarz belegt")
        for element in self.moveField:
            if element.occupiedBlack == True:
                print("X", end=" ")
            else:
                print("E", end=" ")
        print()
    def renderAllMovefield(self):  # Zeigt die Werte jedes einzelnen Feldes an im MoveField

        for element in self.moveField:
            if element.color == 0:
                print("X", end=" ")
            elif element.color == 1:
                print("O", end=" ")
            else:
                print("E", end=" ")
        print()

        for element in self.moveField:
            if element.isPossibleDouble:
                print("True", end=" ")
            else:
                print("False", end=" ")
        print()

        for element in self.moveField:
            if element.isRose:
                print("True", end=" ")
            else:
                print("False", end=" ")
        print()

        for element in self.moveField:
            if element.isSafeField:
                print("True", end=" ")
            else:
                print("False", end=" ")
        print()
        print("Mit weiß belegt")
        for element in self.moveField:
            if element.occupiedWhite == True:
                print("X", end=" ")
            else:
                print("E", end=" ")
        print()
        print("Mit schwarz belegt")
        for element in self.moveField:
            if element.occupiedBlack == True:
                print("X", end=" ")
            else:
                print("E", end=" ")
        print()

        for element in self.moveField:
            print(element.fieldNumber, end=" ")

    def renderMatchfield(
            self):  # Erst nach der MoveField implementiernug notwenidg, dann mit den aufgezeigten fkt im kommentar
        # Muss zum rendern dann durch den moveField laufen und schauen auf welchen Felder was steht. Bei doppelter belegung eben unterschied zw. 1 und 2
        for row in self.matchfield:
            for element in row:
                if element.color == 0:
                    print("X", end=" ")
                elif element.color == 1:
                    print("O", end=" ")
                else:
                    print("E", end=" ")
            print()


class Field:  # Könnte in dieser Form noch sinnvoll für die spätere ausgabe des gerenderten Feld z.b. wenn im Gui Felder untersch. DEsigns haben
    def __init__(self, yPos, xPos):
        self.xPos = xPos
        self.yPos = yPos
        self.occupied = False
        self.color = 2  # To if a field is blank
        self.rose = self.AmIRose(yPos, xPos)

    def AmIRose(self, yPos, xPos):
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
    def __init__(self, fieldNumber):
        self.color = 2  # Blank
        self.fieldNumber = fieldNumber
        self.isOccupied = False
        self.occupiedWhite = False
        self.occupiedBlack = False
        self.isPossibleDouble = self.possibleDoubleOcc()  # Schaut ob 2 auf dem Feld stehen können aka Schwarz und weiß KEINE GLEICHEN FARBEN
        self.isSafeField = self.isSafe()
        self.isRose = self.AmIRose()

    def isSafe(self):
        if self.fieldNumber < 4:
            return True
        if (self.fieldNumber == 12) or (self.fieldNumber == 13):
            return True
        if self.fieldNumber == 7:  # Mittleres Feld welches Sicher ist
            return True
        return False

    def possibleDoubleOcc(self):  # Überprüft ob man doppelt auf einem Feld sein kann
        if self.fieldNumber < 4:
            return True
        if (self.fieldNumber == 12) or (self.fieldNumber == 13):
            return True

        return False  # Kriegerische Zone von 4-11

    def AmIRose(self):  # Schauen ob man nochmal Würfeln darf
        if self.fieldNumber == 3:
            return True
        if self.fieldNumber == 7:
            return True
        if self.fieldNumber == 13:
            return True
        return False


class Stone:
    def __init__(self, color):
        self.color = color
        self.finished = False
        self.posOnMovefield = None  # Auf welchem Feld im Movefield sich der Stein momentan befindet


game = Game()
# game.renderMatchfield()
game.start()

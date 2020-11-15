from tkinter import *

board = [[" ", "-", "-", " ", "-", "-", " "],   # "board" ist die Variable, welche die aktuelle Brettkonfiguration
         ["-", " ", "-", " ", "-", " ", "-"],   # speichert. Die Felder welche zu beginn noch nicht besetzt sind (" ")
         ["-", "-", " ", " ", " ", "-", "-"],   # erhalten im Verlauf des Spieles die Werte "X" und "O". Die Felder,
         [" ", " ", " ", "-", " ", " ", " "],   # welche  nicht besetzt werden können sind mit "-" gekennzeichnet. Es
         ["-", "-", " ", " ", " ", "-", "-"],   # ist wichtig, dass es sie gibt, da man die Felder nun sehr logisch
         ["-", " ", "-", " ", "-", " ", "-"],   # aufrufen kann, da sie in der Matrix die gleiche Position haben wie
         [" ", "-", "-", " ", "-", "-", " "]]   # auf dem Spielbrett.

# "turn" speichert den aktuellen Zug. Die Variable  wird gebraucht, um zu bestimmen wer gerade am Zug ist. Wenn "turn"
# restlos durch zwei teilbar ist, ist "X" sonst "O". "turn" wird auch noch verwendet, um zu bestimmen, wie lange der
# Spieler noch Steine setzten darf, wenn "turn" 18 erreicht, haben beide Spieler ihre 9 Steine gesetzt.
turn = 0

# "turnState" deffiniert was im Zug gerade passiert. Am Anfang jedes neuen Zuges wird "turnState" wieder auf 0 gestellt.
# Die Variable wird gebraucht, wenn die aktion des Spielers mehrere Inputs vom GUI braucht.
turnState = 0

# Die Liste "moveJumpOptions" speichert alle möglichen Felder, auf welche der Spieler springen oder ziehen kann. Die
# Liste wird gefüllt, wenn der Spieler sagt, welchen Spielstein er bewegen möchte.
moveJumpOptions = []

# "lastRow" und "-Column" speichern immer den letzten Zug. Das braucht man, wenn man diese Werte an eine andere Funktion
# weitergeben muss, ohne dass man sie in der ursprünglichen Funktion aufrufen kann. Sie sind default auf -1 gestellt,
# damit man sofort merkt, wenn ein Fehler auftaucht.
lastRow = -1
lastColumn = -1

# Da der Minimax-Algorithmus rekursiv definiert ist, muss man ihm sagen, wann er aufhören soll nach Zügen zu suchen.
# Jedes Mal wenn er sich rekursiv aufruft wird die Tiefe um 1 erhöht, bis sie die "MAXDEPTH" erreicht und abbricht.
# "MAXDEPTHJUMP" wird bei der Springfunktion des Minimax-Algorithmus verwendet und soll kleiner sein als das normale
# "MAXDEPTH", da es beim springen mehr Möglichkeiten gibt und es somit sowieso immer länger geht.
MAXDEPTH = 3
MAXDEPTHJUMP = 2

# In der nextTo-Liste werden alle benachbarten Felder von jedem Feld gespeichert. 
nextTo = [[[[0, 3], [3, 0]], "-", "-", [[0, 0], [0, 6], [1, 3]], "-", "-", [[0, 3], [3, 6]]],
          ["-", [[1, 3], [3, 1]], "-", [[0, 3], [1, 1], [2, 3], [1, 5]], "-", [[1, 3], [3, 5]], "-"],
          ["-", "-", [[3, 2], [3, 2]], [[2, 2], [1, 3], [2, 4]], [[2, 3], [3, 4]], "-", "-"],
          [[[0, 0], [3, 1], [6, 0]], [[3, 0], [1, 1], [3, 2], [5, 1]], [[2, 2], [3, 1], [4, 2]], "-",
           [[2, 4], [4, 4], [3, 5]], [[3, 4], [1, 5], [5, 5], [3, 6]], [[3, 5], [0, 6], [6, 6]]],
          ["-", "-", [[3, 2], [4, 3]], [[4, 2], [5, 3], [4, 4]], [[4, 3], [3, 4]], "-", "-"],
          ["-", [[3, 1], [5, 3]], "-", [[5, 1], [4, 3], [5, 5], [6, 3]], "-", [[5, 3], [3, 5]], "-"],
          [[[3, 0], [6, 3]], "-", "-", [[6, 0], [5, 3], [6, 6]], "-", "-", [[6, 3], [3, 6]]]]


# Allgemein
# Die Funktion askForX() liefert den Modus des Spielers "X" zurück. In gameModeX wird, jenachdem welcher Radiobutton
# aktiv ist, eine andere Zahl gespeichert. Der Wert des Radiobuttons wird in der Variable "gameModeX" gespeichert.
def askForX():
    number = gameModeX.get()
    if number == 1:
        return "h"
    elif number == 2:
        return "m"


# Die Funktion askForO() liefert den Modus des Spielers "O" zurück. In gameModeO wird, jenachdem welcher Radiobutton
# aktiv ist, eine andere Zahl gespeichert. Der Wert des Radiobuttons wird in der Varaible "gameModeO" gespeichert.
def askForO():
    number = gameModeO.get()
    if number == 1:
        return "h"
    elif number == 2:
        return "m"


# Die Funktion getClick() wird immer dann ausgeführt, wenn man ins Spielfeld klickt. Sie ermittelt die genauen X- und
# Y-Koordinaten und gibt die an die Funktion clickGrid() weiter.
def getClick(click):
    clickX = click.x
    clickY = click.y
    print("X: {}; Y: {}".format(clickX, clickY))
    clickGrid(clickX, clickY)


# Die Funtion clickGrid() erhält die Koordinaten des letzten Klicks. Diesen Koordinaten wird dann ein Feld des
# Spielfeldes zugeteilt. Dieses Feld wird dann an die Funktion nextAction() weitergeleitet.
def clickGrid(x, y):
    row = int(y // (400/7))
    column = int(x // (400/7))
    print("Reihe: {}; Spalte: {}".format(row, column))
    nextAction(row, column)


# nextAction() ist eine der wichtigsten Funktionen. Sie wird immer dannausgeführt, wenn man ins Spielfeld klickt und sie
# leitet den nächsten Schritt im Spiel ein.
def nextAction(row, column):
    global turn, top
    modeX = askForX()   # Zuerst wird ermittelt, in was für einem Modus Spieler "X" und "O" sind. Dies wird in den
    modeO = askForO()   # Variablen modeX und modeO gespeichert.
    infoLabel2Update("clear", -1)   # Durch diesen Befehl wird das zweite Info-Label, was sich unten am Fenster
    # befinset, wieder gelehrt. In diesem Label kann zum Beispiel stehen, was der nächste Schritt ist, welcher der
    # Benutzer eingeben muss.
    if turn % 2 == 0:   # Wenn die Zugzahl gerade ist, ist "X" am Zug, ansonsten ist "O" am Zug.
        if turnState == 0:  # Am Anfang von jedem Zug ist "turnState" 0. Es wird die erste Aktion ausgeführt. Der
            # Minimax-Algorithmus bleibt immer im "turnState" 0
            phase = checkPhase(piecesRemaining("X"))    # Die Spielphase in der sich "X" befindet wird ermittlet.
            infoLabel1Update("X")   # Das erste Info-Label, welches sich oben im Fenster befindet, zeigt an, welcher Zug
            # es ist und wer dran ist.
            play("X", "O", phase, modeX, row, column, 0)    # Die Funktion play() wird als Spieler "X" aufgerufen. Man
            # gibt auch noch die Phase des Spielers, sein Modus und die Koordinaten des Feldes, von welchem die Aktion
            # ausgeht, mit.
        elif turnState == 1:    # Dies ist der Fall, wenn eine Aktion, wie z.B. eine Bewegung in zwei Schritten erfolgt.
            # Man kann pro Aufruf nur ein Koordinatenpaar liefern, weshalb man, wenn man von einem Feld zu einem anderen
            # Feld gehen will, die Funktion zweimal aufrufen muss. Wichtig beim zweiten Aufruf ist, dass der letzte
            # Parameter des play()-Aufrufs, eine 1 ist.
            phase = checkPhase(piecesRemaining("X"))
            play("X", "O", phase, "h", row, column, 1)
        elif turnState == 2:    # Der dritte mögliche Klick, der ein Zug braucht ist der Klick, welcher besagt, welchen
            # gegnerischen Spielstein man entfernen will.
            Human_removeEnemy("X", "O", row, column)
        # Am Ende des Zuges wird noch die Funktion draw() aufgerufen, welche das aktuelle Spielbrett in der Konsole
        # darstellt.
        draw()
    else:   # Wenn "O" am Zug ist, sind alle Variablen, welche auf den aktuellen Spieler bezogen sind, umgekehrt wie
        # wenn Spieler "X" am Zug ist. Ansonsten ist es das Gleiche.
        if turnState == 0:
            phase = checkPhase(piecesRemaining("O"))
            infoLabel1Update("O")
            play("O", "X", phase, modeO, row, column, 0)
        elif turnState == 1:
            phase = checkPhase(piecesRemaining("O"))
            play("O", "X", phase, "h", row, column, 1)
        elif turnState == 2:
            Human_removeEnemy("O", "X", row, column)
        draw()


# Die play()-Funktion leitet hauptsächlich die Variablen, mit denen sie aufgerufen worden ist, an ihre Unterfunktionen
# weiter.
def play(player, enemyPlayer, phase, mode, row, column, moveJumpState):
    if mode == "h":    # Wenn der Modus "h" (für human) ist, bedeutet das, dass es ein menschlicher Spieler ist.
        Human_play(player, enemyPlayer, phase, row, column, moveJumpState)
    elif mode == "m":   # Das "m" steht für Minimax.
        infoLabel2Update("minimax", -1)    # Beim unteren Label steht nun, dass der Minimax-Algorithmus überlegt.
        Minimax_play(player, enemyPlayer, phase)


# Die draw()-Funktion zeichnet ein Spielbrett in die Konsole. Im Gerüst des Spielfeldes sind Platzhaltervariablen,
# welche über die .format()-Funktion den jeweiligen Werten in "board" zugewiesen werden.
def draw():
    print(" {0} ------------ {1} ------------ {2} \n |              |              | \n |    {3} ------- {4} ------- \
{5}    | \n |    |         |         |    | \n |    |    {6} -- {7} -- {8}    |    | \n\
 |    |    |         |    |    | \n {9} -- {10} -- {11}         {12} -- {13} -- {14} \n |    |    |         |    |    |\
  \n |    |    {15} -- {16} -- {17}    |    | \n |    |         |         |    | \n |    {18} ------- {19} ------- {20}\
    | \n |              |              | \n {21} ------------ {22} ------------ {23} "
          .format(board[0][0], board[0][3], board[0][6], board[1][1], board[1][3], board[1][5], board[2][2],
                  board[2][3], board[2][4], board[3][0], board[3][1], board[3][2], board[3][4], board[3][5],
                  board[3][6], board[4][2], board[4][3], board[4][4], board[5][1], board[5][3], board[5][5],
                  board[6][0], board[6][3], board[6][6]))


# Diese Funktion gibt an die Funktion, welche sie aufgerufen hat, die aktuelle Spielphase zurück.
def checkPhase(playerRemaining):
    if turn < 18:   # Bis zum Zug 18 müssen die beiden Spieler ihre Steine plazieren.
        return "place"
    elif playerRemaining == 3:  # Wenn ein Spieler alle seine Steine plaziert hat und wieder nur 3 Steine hat, beginnt
        # für ihn die Endphase des Mühle-Spiels. Er kann jetzt seine Steine nicht mehr nur auf benachbarte Felder
        # setzen, sondern auf alle freie Felder.
        return "jump"
    else:   # Wenn die Phase weder "springen" noch "setzen" ist, dann kann der Spieler seine Steine nur auf die
        # angrenzenden Felder verschieben.
        return "move"


# Die mill()-Funktion überprüft, ob sich das Feld, welches mitgegeben wurde, in einer Mühle befindet. Meist wird damit
# geschaut, ob der letzte Zug eine Mühle geschlossen hat. Falls sich das Feld in einer Mühle befindet gint die Funktion
# "True" zurück, ansonsten "False".
def mill(row, column, player):
    playerStones = 0    # Ob das Feld in einer Mühle ist, findet man heraus, wenn man die Steine des Spielers in der
    # Spalte oder der Reihe zählt. Wenn es 3 sind, ist es eine Mühle.
    rowCheckDenied = False  # Wenn eine dieser Variablen "True" ist, heisst das, dass die Reihe oder Spalte schon wegen
    columnCheckDenied = False   # des Sonderfalles geprüft wurde. Ein Sonderfall ist, wenn das Feld entweder auf der
    # mittleren Reihe oder Spalte ist.
    if row == 3:    # Wenn das Feld in der mittleren Reihe ist, muss man aufpassen, da diese Reihe 6 Felder beinhaltet
        # und es nicht umbedingt eine Mühle ist, wenn 3 davon, dem gleichen Spieler gehören. Man muss also schauen, ob
        # die 3 vor oder nach der Mitte dem gleichen Spieler gehören.
        if column < 3:  # Falls das Feld vor der Hälfte  ist, werden ur die Felder vor der Hälfte geprüft.
            for i in range(0, 3):
                if board[row][i] == player:    # Wenn das Feld dem Spieler gehört, wird "playerStones" um 1 grösser.
                    playerStones += 1
        else:
            for i in range(4, 7):
                if board[row][i] == player:
                    playerStones += 1
        if playerStones >= 3:   # Wenn "playerStones" 3 ist, dann ist es eine Mühle und der Boolean "True" wird zurück
            # gegeben.
            return True
        rowCheckDenied = True   # Die Reihe wurde gerade negativ geprüft, weshalb man das unten nicht mehr machen soll.
    elif column == 3:   # Das Gleiche gilt auch für die mittlere Spalte.
        if row < 3:
            for i in range(0, 3):
                if board[i][column] == player:
                    playerStones += 1
        else:
            for i in range(4, 7):
                if board[i][column] == player:
                    playerStones += 1
        if playerStones >= 3:
            return True
        columnCheckDenied = True  # Die Spalte wurde negativ geprüft, weshalb man das unten nicht mehr machen soll.
    playerStones = 0
    if not rowCheckDenied:   # Falls die Reihe schon geprüft wurde, darf man das nicht nocheinmalmachen
        for i in range(0, 7):   # Wenn es nicht die mittlere Reihe ist, werden alle Felder in der Reihe geprüft.
            if board[row][i] == player:
                playerStones += 1
    if playerStones >= 3:
        return True
    playerStones = 0    # "playerStones" muss wieder auf 0 gesetzt werden, um neu zu zählen beginnen.
    if not columnCheckDenied:   # Falls die Spalte schon geprüft wurde, darf man das nicht nocheinmalmachen
        for i in range(0, 7):   # Wenn es nicht die mittlere Spalte ist, werden alle Felder in der Spalte geprüft.
            if board[i][column] == player:
                playerStones += 1
    if playerStones >= 3:
        return True
    return False    # Falls es keine Mühle gab und die Funktion somit frühzeitig abgebrochen wurde, wird der Boolean
    # "False" zurückgegeben.


# Es gibt 2 Arten zu gewinnen. Entweder hat der Gegner unter 3 Steine oder keine Zugsmöglichkeiten mehr. Falls der
# Gegner verloren hat, wird "True" zurückgegeben, ansonsten "False".
def win(enemyColor):
    if piecesRemaining(enemyColor) <= 2 and turn >= 18:    # Verlieren kann man erst, wenn alle Steine gesetzt wurden,
        # weshalb es mindestens Zug 18 sein muss.
        return True
    elif (zugzwang(enemyColor) and turn >= 18) and piecesRemaining(enemyColor) != 3:    # Wenn der Gegner am Springen
        # ist, kann er nicht an "Zugzwang" verlieren.
        return True
    else:
        return False


# Falls ein Spieler keine Bewegungsmöglichkeit mehr hat, hat er verloren. Man überprüft, ob der Spieler ein leeres Feld
# neben einem seiner Felder hat, auf welches er ziehen kann. Ist dies nicht der Fall ist er im sogenannten "Zugzwang".
def zugzwang(playerColor):
    for i in range(0, 7):   # Man schaut jedes Feld an...
        for j in range(0, 7):
            if board[i][j] == playerColor:  # Und nur wenn das Feld von ihm besetzt ist...
                for nearField in nextTo[i][j]:  # Schaut man, was die benachbarten Felder sind.
                    if board[nearField[0]][nearField[1]] == " ":    # Falls eines dieser Felder leer ist, kann er dort
                        # hinziehen und ist nicht im Zugzwang
                        return False
    return True


# Diese Funktionen setzt alles auf die Startwerte zurück.
def restart():
    global board, turn, turnState   # Die 3 Variblen, welche den Spielstand beschreiben sind "turn", "board" und
    # "boardState" und müssen desalb wieder auf ihre ursprünglichen Werte zurückgesetzt werden
    board = [[" ", "-", "-", " ", "-", "-", " "],
             ["-", " ", "-", " ", "-", " ", "-"],
             ["-", "-", " ", " ", " ", "-", "-"],
             [" ", " ", " ", "-", " ", " ", " "],
             ["-", "-", " ", " ", " ", "-", "-"],
             ["-", " ", "-", " ", "-", " ", "-"],
             [" ", "-", "-", " ", "-", "-", " "]]
    turn = 0
    turnState = 0
    updateGUI()     # Danach wird das GUI refresht
    infoLabel2Update("clear", 0)


# Die Funktion piecesRemaining() zählt die verbleibenden Steine des Spielers. Die Funktion zählt alle Felder des
# Brettes, auf denen ein Stein des Spielers ist und gibt diese Zahl am Schluss zurück.
def piecesRemaining(player):
    pieces = 0
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:
                pieces += 1
    return pieces


# Die Funktion nextTurn() setzt "turnState" wieder auf 0 und vergrössert "turn" um 1
def nextTurn():
    global turn, turnState
    turn += 1
    turnState = 0


# Minimax general
# Bevor die ganzen Minimax-Funktionen erklärt werden, geht es darum, wie der Algorithmus grundsätzlich funktioniert.
# Der Minimax-Algorithmus probiert stur alle Möglichkeiten aus und bewertet diese Positionen mit einer
# Bewertungsfunktion. Dann entscheidet er sich, welche Position am besten ist. Dies ist nicht unbedingt die Position mit
# der höchsten Bewertung! Da es immer zwei Spieler gibt, welche gegeneinander spielen, versucht der eine einen möglichst
# hohe Positionsbewertung haben und sein Gegner versucht dies zu verhindern. Der Spieler, welcher die möglichst hohe
# Bewertung haben möchte, ist der «Maximizer» und sein Gegenspieler der «Minimizer». Zuerst ist immer der Maximizer. Der
# Maximizer beginnt, in dem er seinen Stein auf das erste nicht besetzte Feld setzt. Danach kommt der Minimizer, welcher
# wiederum sein Stein auf das erste leere Feld setzt. So geht es abwechslungsweise weiter, bis die gewünschte Tiefe
# erreicht wird. Wenn die gewünschte Tiefe erreicht wird, bewertet man die aktuelle Brettaufstellung, aus der Sicht des
# Maximizer. Wenn man die Position ausgewertet hat, geht man einen Schritt zurück und setzt den Stein an die zweite
# leere Stelle. Wiederum wird die Position ausgewertet und falls diese neue Position für den, welcher gerade dran ist
# besser ist als die vorherige (wenn es ein Zug des Maximizer ist, ist es besser, wenn die neue Position eine höhere
# Zahl hat und wenn der Minimizer am Zug ist, ist es besser, wenn die Zahl kleiner ist), wird diese merkt man sich
# diese. Dann geht es weiter, bis man alle Möglichkeiten überprüft hat und man die beste Position hat. Danach geht es
# wieder einen Schritt zurück und man probiert alle Möglichkeiten aus. Dann wird wieder geprüft, welche Position am
# besten ist und das ganze geht wieder einen Schritt zurück. So geht es weiter, bis man wieder beim ersten Maximizer
# angekommen ist und dieser entscheidet sich dann für den besten Zug, welcher er machen könnte und macht diesen. Dann
# ist sein Zug beendet.

# Die Funktion Minimax_play() startet, je nachdem welche Phase gerade ist, eine andere Funktion.
def Minimax_play(player, enemyPlayer, phase):
    if phase == "place":
        Minimax_findBestPlace(player, enemyPlayer)
    elif phase == "move":
        Minimax_findBestMove(player, enemyPlayer)
    else:
        Minimax_findBestJump(player, enemyPlayer)


# Da man beim Minimax weitere Züge simulieren muss, muss man auch sagen, in welcher Phase diese Züge sind.
def Minimax_nextPhase(Minimax_turn, player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn):
    if Minimax_turn < 18:
        return Minimax_minimaxPlace(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn,
                                    Minimax_turn)
    elif isMaximizer and piecesRemaining(player) == 3:
        return Minimax_minimaxJump(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn)
    elif not isMaximizer and piecesRemaining(enemyPlayer) == 3:
        return Minimax_minimaxJump(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn)
    else:
        return Minimax_minimaxMove(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn)


# Evaluation
# Die evaluation()-Funktion bewertet die Brettkonfiguration aus sicht des "player". In den einzelnen Phasen werden die
# Koeffiziente anders gewählt, weshalb man die entgültige Punktzahl nicht in dieser Funktion berechnen kann. Alle
# verschiedenen Werte werden zurückgeliefert und in den Phasenspezifischen-Funktionen ausgerechnet.
def evaluation(player, enemyPlayer, row, column):
    if mill(row, column, player):   # Das erste, was berücksichtigt wird, ist, ob gerade eine Mühle geschlossesn wurde.
        recentMill = 1  # Falls eine geschlossen wurde, ist "recentMill" 1
    elif mill(row,  column, enemyPlayer):
        recentMill = -1   # Falls der Gegner gerade eine Mühle geschlossen hat, ist "recentMill" -1
    else:
        recentMill = 0   # Falls keine Mühle geschlossen wurde, bleibt der Wert 0

    existingMills = closedMills(player) - closedMills(enemyPlayer)  # Das zweite, das berücksichtigt wird, ist, wieviele
    # Mühlen der Spieler hat. Hier wird die Differenz, zwischen den Mühlen des Spielers und dessen Gegner, in der
    # Variabel "existingMills" gespeichert.

    blockedPiecesDifference = blockedPieces(enemyPlayer) - blockedPieces(player)    # In der Variabel
    # "blockedPiecesDifference" wird Differenz der Steine, welche keinen Zug machen können, gespeichert.

    pieceDifference = piecesRemaining(player) - piecesRemaining(enemyPlayer)    # "pieceDifference" ist die Differenz
    # der noch vorhandenen Steine des Spielers und seines Gegners

    nearlyMills = nearlyMillCounter(player) - nearlyMillCounter(enemyPlayer)    # Als "nearlyMill" wird bezeichnet, wenn
    # zwei Steine des selben Spielers nebeneinander sind und das dritte Feld leer ist.

    threeConfigurations = threeConfiguration(player) - threeConfiguration(enemyPlayer)  # Eine "threeConfiguration" ist,
    # wenn ein Stein in zwei "nearlyMills" gleichzeitig ist.

    doubleMills = doubleMillCounter(player) - doubleMillCounter(enemyPlayer)    # Eine "doubleMill" ist, wenn ein Stein
    # in zwei Mühlen zur selben Zeit ist.

    if win(enemyPlayer):    # Und zuletzt wird noch betracht gezogen, ob der Spieler oder sein Gegner gewonnen hat.
        winning = 1
    elif win(player):
        winning = -1
    else:
        winning = 0

    return recentMill, existingMills, blockedPiecesDifference, pieceDifference, nearlyMills, threeConfigurations, \
           doubleMills, winning     # Am Schluss werden alle diese Werte noch zurückgegeben


# closedMills() zählt die geschlossenen Mühlen
def closedMills(player):
    closedMills = 0     # Der Zähler wird zuerst auf 0 gesetzt
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:    # Dananch wird für jedes Feld überprüft...
                if mill(row, column, player):   # ... ob es sich in einer Mühle  befindet
                    closedMills += 1    # Wenn schon, geht der Zähler um eines nach oben
    closedMills /= 3    # Zum Schluss wird die Anzahl an gezählten Mühlen durch 3 geteilt, da die Mühle 3 Mal (für jeden
    # Stein einmal) gezählt wurde
    return closedMills


# blockedPieces() zählt wieviele Steine kein freies Feld neben sich haben.
def blockedPieces(player):
    blockedPieces = 0   # Der Zähler wird zuerst auf 0 gestellt.
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:    # Danach wird für jeden Stein geschaut...
                if availableMoves(row, column) == 0:    # ... ob er 0 Felder hat, auf die er gehen kann.
                    blockedPieces += 1  # Ist dies der Fall geht der zähler um 1 hoch
    return blockedPieces


# availableMoves() zählt wieviele Zugsmöglichkeiten ein Stein hat.
def availableMoves(row,  column):
    moves = 0   # Der Zähler wird zuerst auf 0 gestellt.
    for field in nextTo[row][column]:
        if board[field[0]][field[1]] == " ":    # Danach überprüft man für jedes benachbarte Feld, ob dieses Frei ist.
            moves += 1  # Falls schon, geht der Zähler um 1 hoch
    return moves


# nearlyMillCounter() zählt  wieviele fast fertige Mühlen der Spieler hat.
def nearlyMillCounter(player):
    nearlyMills = 0     # Der Zähler wird zuerst auf 0 gestellt.
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:    # Für jeden Stein...
                rowBool, columnBool = nearlyMill(player, row, column)   # ... wird geschaut, ob er in einer "nearlyMill"
                # in seiner Reihe oder Spalte ist. Dies wird in den Booleans "rowBool" und "columnBool" gespeichert.
                if rowBool == columnBool:   # Falls sie gleich sind, ist der Stein entweder in zwei "nearlyMills" oder
                    # in gar keiner.
                    if rowBool:     # Falls "rowBool" True  ist, bedeutet das, dass der Stein in 2 "nearlyMills" ist.
                        nearlyMills += 2
                else:   # Falls die Booleans unterschiedlich sind, ist der Stein in einer "nearlyMill".
                    nearlyMills += 1
    nearlyMills /= 2    # Da eine "nearlyMill" aus zwei Steinen besteht, muss die gezählte Anzahl noch durch zwei
    # dividiert werden.
    return nearlyMills


# Eine "nearlMill" ist eine Mühle, bei der noch ein Stein fehlt. Dieses Feld muss leer sein.
def nearlyMill(player, row, column):
    nearlyMillRow = False   # Eine "nearlyMill" kann in der Reihe oder in der Spalte sein, deshalb muss man das separat
    # testen
    playerCounter = 0   # Diese Zählvariabel wird am Anfang auf 0 gesetzt.
    for i in range(0, 7):   # Man schaut zuerst, ob es eine "nearlyMill" in der Reihe hat.
        if (row == 3 and i == 3) and playerCounter != 2:    # Wenn man die mittlere Reihe überprüft muss man vorsichtig
            # sein, da diese 6 Felder hat und nicht nur 3. Wenn man die mittlere Reihe prüft und im Zentrum des Brettes
            # angekommen ist und nicht schon zwei Steine hat, muss der Zähler zurückgesetzt werden.
            playerCounter = 0
        elif (row == 3 and i == 3) and playerCounter == 2:  # Falls man 2 Steine hat, wird die Schleife abgebrochen
            break
        elif board[row][i] == player:   # Falls es nicht die mittlere Reihe ist, zählt man alle Steine, welche sich in
            # der Reihe befinden.
            playerCounter += 1
    if playerCounter == 2:  # Wenn die Anzahl an Steinen 2 ist, könnte es eine "nearlyMill" sein.
        for i in range(0, 7):
            if board[row][i] == " ":    # Jedoch muss das letzte Feld leer sein.
                nearlyMillRow = True    # Ist auch dies der Fall, gibt es in der Reihe eine "nearlyMill"
    nearlyMillColumn = False    # Für die Spalte macht man nochmal genau das Gleiche.
    playerCounter = 0
    for i in range(0, 7):
        if (column == 3 and i == 3) and playerCounter != 2:
            playerCounter = 0
        elif (column == 3 and i == 3) and playerCounter == 2:
            break
        elif board[i][column] == player:
            playerCounter += 1
    if playerCounter == 2:
        for i in range(0, 7):
            if board[i][column] == " ":
                nearlyMillColumn = True
    return nearlyMillRow, nearlyMillColumn  # Am Schluss werden diese zwei Boolean zurückgeliefert


# Eine "threeConfiguration" ist, wenn ein Stein gleichzeitig in zwei "nearlyMills" ist. Die Funktion ist gleich wie
# nearlyMillCounter(),...
def threeConfiguration(player):
    threeConfigurations = 0
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:
                rowBool, columnBool = nearlyMill(player, row, column)
                if rowBool == columnBool:   # ... ausser dass beide Boolean True sein müssen.
                    if rowBool:
                        threeConfigurations += 1
    return threeConfigurations


# doubleMillCounter() zählt die Doppelmühlen. Eine Doppelmühle ist,  wenn ein Stein in zwei Mühlen vorhanden ist.
def doubleMillCounter(player):
    doubleMills = 0
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:    # Man überprüft für jede Position, ob es eine Doppelmühle ist.
                doublemill = doubleMill(player, row, column)
                if doublemill:  # Falls ja, wird der Zähler um 1 grösser.
                    doubleMills += 1
    return doubleMills


# doubleMill() prüft, ob ein Stein in einer Doppelmühle ist. Die Funktion ist ähnlich wie die normale mill()-Funktion.
# Der Unterschied ist, dass man schaut, ob man eine Mühle in der Reihe und der Spalte hat und nur wenn man sie beide
# hat, gibt die Funktion True zurück.
def doubleMill(player, row, column):
    playerStones = 0
    rowMill = False     # Ist True, falls der Stein in einer Reihen-Mühle  ist.
    columnMill = False       # Ist True, falls der Stein in einer Spalten-Mühle  ist.
    rowCheckDenied = False
    columnCheckDenied = False
    if row == 3:
        if column < 3:
            for i in range(0, 3):
                if board[row][i] == player:
                    playerStones += 1
        else:
            for i in range(4, 7):
                if board[row][i] == player:
                    playerStones += 1
        if playerStones >= 3:
            rowMill = True  # "rowMill" wird True, anstatt dass die Funktion True zurück gibt.
        rowCheckDenied = True
    elif column == 3:
        if row < 3:
            for i in range(0, 3):
                if board[i][column] == player:
                    playerStones += 1
        else:
            for i in range(4, 7):
                if board[i][column] == player:
                    playerStones += 1
        if playerStones >= 3:
            columnMill = True   # "columnMill" wird True, anstatt dass die Funktion True zurück gibt.
        columnCheckDenied = True
    playerStones = 0
    if not rowCheckDenied:
        for i in range(0, 7):
            if board[row][i] == player:
                playerStones += 1
    if playerStones >= 3:
        rowMill = True  # "rowMill" wird True, anstatt dass die Funktion True zurück gibt.
    playerStones = 0
    if not columnCheckDenied:
        for i in range(0, 7):
            if board[i][column] == player:
                playerStones += 1
    if playerStones >= 3:
        columnMill = True   # "columnMill" wird True, anstatt dass die Funktion True zurück gibt.
    if rowMill and columnMill:  # Nur wenn beide Variablen True sind gibt die Funktion True zurück.
        return True
    else:   # Ansonsten gibt sie False zurück
        return False


# Remove
# Bevor man einen gegnerischen Stein entfernt muss man eine Mühle schliessen.
def Minimax_furtherActionChecking(player, enemyPlayer, row, column, phase):
    if mill(row, column, player):   # Wenn man mit dem letzten Zug eine Mühle schloss, darf man einen Gegner entfernen.
        i, j = Minimax_findEnemyToRemove(player, enemyPlayer, phase)    # Diesen Stein findet die Funktion
        # Minimax_findEnemyToRemove(). Diese Funktion gibt die Position des Steines zurück.
        Minimax_removeEnemy(i, j)   # Danach wird dieser Stein entfernt.
        return True, i, j   # Für die Minimax-Funktionen ist es wichtig zu wissen, welchen Stein man entfernt hat,
        # weshalb man seine Position und ein True, welches dafür steht, dass man überhaupt einen Stein entfernt hat,
        # zurückgibt.
    return False, -1, -1    # Falls kein Stein entfernt wurde, gibt man ein False zurück und man muss noch zwei weitere
    # Werte zurückgeben, obwohl diese nicht berücksichtigt werden, denn die Funktion, welche diese Funktion aufruft
    # erwartet 3 Rückgabewerte.


# Diese Funktion ermittelt, welcher gegnerische Stein am wertvollsten ist und gibt seine Position zurück.
def Minimax_findEnemyToRemove(player, enemyPlayer, phase):
    bestRemove = -10000  # Zuerst setzt man den besten Wert auf -1000, damit jeder ermittelte Wert sicher höher ist.
    removeRow = -1  # Die Position des besten Zuges  wird zuerst auf (-1; -1) gesetzt, jedoch sollte diese sich sofort
    removeColumn = -1   # ändern.
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == enemyPlayer and not mill(row, column, enemyPlayer):    # Dann schaut man für jeden
                # gegnerischen Stein, was dessen Bewertung ist. Jedoch darf der Stein nicht in einer geschlossenen Mühle
                # sein, da man diese Steine nicht entfernen darf.
                removeEval = removeEvaluation(player, enemyPlayer, row, column, phase)  # Danach erhält man für den
                # Stein einen Wert. Bei der ermittlung des Wertes kommt es darauf an, in was für einer Phasee sich der
                # Gegner befindet.
                if removeEval > bestRemove:     # Falls der Wert des gerade überprüften Steines grösser ist, als der
                    # bisherige Bestwert, wird dieser neu gesetzt und man merkt sich die Position des Steines.
                    removeRow = row
                    removeColumn = column
                    bestRemove = removeEval
    if removeColumn == -1:  # Falls "removeColumn" immer noch -1 ist bedeutet das, dass alle gegnerischen Steine in
        # geschlossenen Mühlen sind und somit keine Position bewertet wurde. Dann darf man auch Steine, welche in Mühlen
        # sind, entfernen und überprüft deshalb nochmal alle Positionen, aber ohne die einschrenkung, dass der Stein
        # ausserhalb einer Mühle sein muss.
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == enemyPlayer:
                    removeEval = removeEvaluation(player, enemyPlayer, row, column, phase)
                    if removeEval > bestRemove:
                        removeRow = row
                        removeColumn = column
                        bestRemove = removeEval
    return removeRow, removeColumn  # Am Schluss wird die beste Position zurückgegeben


# Wenn man die Position des zu entfernenden Steines hat, muss dieser nur noch entfernt werden. Seine Position wird im
# Spielfeld wieder auf " " gesetzt und das Brett wird neu angezeigt.
def Minimax_removeEnemy(row, column):
    board[row][column] = " "
    updateGUI()


# Je nachdem in welcher Phase sich der Gegner befindet sind andere Faktoren wichtig. Deshalb gibt es eine eigene
# Bewertungsfunktion für jede Phase.
def removeEvaluation(player, enemyPlayer, row, column, phase):
    if phase == "place":
        return evaluationPlace(player, enemyPlayer, row, column)
    elif phase == "move":
        return evaluationMove(player, enemyPlayer, row, column)
    else:
        return evaluationJump(player, enemyPlayer, row, column)


# Place
# Wenn der Minimax in der "setzen"-Phase ist, muss er entscheiden, welche leere Position für ihn am besten ist.
def Minimax_findBestPlace(player, enemyPlayer):
    bestValue = -10000   # Zuerst werden die "besten" Werte so gesetzt, dass man sofort sieht, dass diese nicht die
    bestRow = -1    # richtigen sind
    bestColumn = -1
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == " ":   # Danach geht es darum, jedes leere Feld zu überprüfen.
                board[row][column] = player     # Zuerst setzt man seinen Stein auf das leere Feld.
                a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, row, column, "place")  # Dann schaut man,
                # ob man gerade eine Mühle geschlossen hat. Falls  schon ist "a" True und "b" und "c" ist die Position
                # des entfernten Feldes.
                Minimax_Turn = turn   # Um nicht den globalen "turn" zu verändern erstellt man eine neue "turn"-Variable
                value = Minimax_nextPhase(Minimax_Turn, player, enemyPlayer, 0, False, -1000, 1000, row, column)    # Da
                # es auch sein könnte, dass für den nächsten Zug eine andere Phase herscht, mussman zuerst überprüfen,
                # in welcher Phase der nächste Zug ist. Dann wird die rekursive Minimax()-Funktion aufgerufen, welche
                # den Wert dieser Position zurückgibt. Der erste Minimax-Aufruf ist immer als Minimizer, da die
                # findBest()-Funktionen immer ein Maximizer sind. Die Tiefe ist 0 und Alpha und Beta sind jeweils -1000.
                # Alpha und Beta braucht man, um beim erarbeiten der besten Position abkürzen zu können, da wenn man
                # schon einen besseren Zug hat, muss man nicht mehr die anderen Ausrechnen. Dieses sogenannte
                # "Alpha-Beta-Pruning" spart sehr viel Zeit.
                board[row][column] = " "    # Wenn man den Wert der Position hat, muss man den Zug wieder rückgängig
                # machen, da man diesen Zu nicht umbedingt machen wird.
                if a:   # Falls man einen gegnerischen Stein entfernt hat, muss man auch diesen wieder setzen.
                    board[b][c] = enemyPlayer   # Dafür braucht man die Position, an welcher er entfernt wurde.
                if value > bestValue:   # Dann schaut man ob der Zug gerade besser war, als der Bisherige.
                    bestRow = row   # Wenn schon wird der beste Zug neu gesetzt.
                    bestColumn = column
                    bestValue = value
    Minimax_place(bestRow, bestColumn, player, enemyPlayer)     # Am Schluss schaut man, welcher Zug der allerbeste war
    # und führt diesen aus.


# Die minimax()-Funktion ist rekursiv aufgebaut. Wenn sie die  maximale Tiefe erreicht hat, gibt sie den Wert zurück.
# Der Wert wird dann nach der Grundidee hinter dem Minimax-Algorithmus zurückgegeben, bis man bei der
# bestPlace()-Funktion ist.
def Minimax_minimaxPlace(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn, Minimax_turn):
    score = evaluationPlace(player, enemyPlayer, lastRow, lastColumn)   # Zuerst wird die Position bewertet.
    if score < -1000:   # Falls "score" kleiner als -1000 ist, hat der Speiler verloren und man kann abbrechen.
        return -1000 + depth    # Falls man mit jeder Position verliert, wird noch berücksichtigt, wieviele Züge es noch
        # geht, bis man verloren hat.
    elif score > 1000:  # Falls "score" grösser als 1000 ist, hat der Spieler gewonnen und man kann auch abbrechen.
        return 1000 - depth
    elif depth == MAXDEPTH:     # Wenn die Maximale Tiefe erreicht wurde, wird der Wert zurückgegeben.
        return score

    # Falls der Maximizer am Zug ist, wird als "player" als aktiver Spieler verwendet.
    if isMaximizer:
        bestValue = -10000   # Der Wert wird wieder so klein, dass man immer einen grösseren Wert erhält.
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == " ":
                    board[row][column] = player     # Dann probiert man das erste leere Feld und setzt seinen Stein.
                    a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, row, column, "place")  # Falls ein
                    # Stein entfernt wurde merkt man sich, wie bei der findBest()-Funktion, welcher Stein entfernt wurde
                    Minimax_turn += 1   # Der simuliere "turn" wird um 1 grösser.
                    value = Minimax_nextPhase(Minimax_turn, player, enemyPlayer, depth + 1, False, alpha, beta, row,
                                              column)   # Der Wert erhält man von einem anderen Minimax-Aufruf. Als
                    # Maximizer, gibt man False mit und setzt die vergrössert die Tiefe um 1.
                    bestValue = max(bestValue, value)   # Der beste Wert wird als der grössere Wert aus dem bislang
                    # besten Wert und dem aktuellen Wert hinterlegt.
                    board[row][column] = " "    # Der Zug wird wieder rückgängig gemacht.
                    if a:
                        board[b][c] = enemyPlayer
                    alpha = max(alpha, bestValue)   # Und Alpha wird als den grösseren Wert aus dem bisherigen Alpha und
                    # dem besten Wert hinterlegt. Wie Alpha-Beta-Pruning funktioniert ist schwer vorstellbar, wenn man
                    # keine Grafiken hat, weshalb es hier nicht erklärt wird. Es wird aber in der Arbeit vorhanden sein.
                    if beta <= alpha:
                        break
        return bestValue    # Den besten Wert, welchen man erhalten hat, gibt man eine Ebene zurück.
    else:   # Falls der Minimizer am Zug ist, ist der aktive Spiler der "enemyPlayer".
        bestValue = 10000   # "bestValue" wird als +10000 definiert, da dieser Spieler versucht einen möglichst kleinen
        # Wert zu erhalten.
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == " ":
                    board[row][column] = enemyPlayer    # Man besetzt das Feld als "enemyPlayer".
                    a, b, c = Minimax_furtherActionChecking(enemyPlayer, player, row, column, "place")
                    Minimax_turn += 1
                    value = Minimax_nextPhase(Minimax_turn, player, enemyPlayer, depth + 1, True, alpha, beta, row,
                                              column)   # Man gibt True statt Flase mit, damit es abwechselt.
                    bestValue = min(bestValue, value)   # Jetzt will man den kleineren der Werte, nicht den Grösseren.
                    board[row][column] = " "
                    if a:
                        board[b][c] = player
                    beta = min(beta, bestValue)   # Und auch Beta wird als kleineren der Werte definiert
                    if beta <= alpha:
                        break
        return bestValue    # Der beste Wert dieses Spielers wird zurückgegeben.


# Wenn man weiss, welcher Zugam besten ist, muss man diesen noch setzen.
def Minimax_place(row, column, player, enemyPlayer):
    board[row][column] = player    # Die Position auf dem Spielfeld wird erneuert und man geht zum nächsten Zug über.
    nextTurn()
    updateGUI()     # Das Brett wird mit dem neuen Wert dargestellt.
    a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, row, column, "place")  # Falls man ein Gegner entfernen
    # kann, geschieht dies jetzt, aber dieses Mal wird der Stein nicht noch einaml plaziert, weshalb man die
    # Rückgabewerte dieser Funktion nicht braucht.


# In der "setzen"-Phase sind andere Dinge wichtig, als in den anderne Phasen, weshalb man andere Koeffiziente hat. Die
# Koeffiziente stammen von: http://www.dasconference.ro/papers/2008/B7.pdf
def evaluationPlace(player, enemyPlayer, row, column):
    recentMill, existingMills, blockedPiecesDifference, pieceDifference, nearlyMills, threeConfigurations, \
    doubleMills, winning = evaluation(player, enemyPlayer, row, column)

    score = 18 * recentMill + 26 * existingMills + blockedPiecesDifference + 9 * pieceDifference + 10 * nearlyMills +\
            7 * threeConfigurations
    return score


# Move
# Der Unterschied zwischen "move" und "place" ist, dass man bei "move" einen seiner Steine an eine benachbarte Position
# verschiebt und nicht einen neuen Stein plaziert.
def Minimax_findBestMove(player, enemyPlayer):
    bestValue = -1000
    bestRow = -1
    bestColumn = -1
    replaceRow = -1     # Hier befinden sich zusätzlich noch zwei Werte, welche die Position der Steines, welcher
    replaceColumn = -1  # verschoben wird beschreiben
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:    # Zuerst schaut man, wo einer seiner Steine ist
                nextToList = nextTo[row][column]
                for field in nextToList:
                    if board[field[0]][field[1]] == " ":    # und dann, welche anliegenden Felder noch leer sind.
                        moveToRow = field[0]
                        moveToColumn = field[1]
                        board[moveToRow][moveToColumn] = player   # Danach macht man den Zug einmal vorübergehend
                        board[row][column] = " "
                        a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, moveToRow, moveToColumn, "move")
                        value = Minimax_nextPhase(20, player, enemyPlayer, 0, False, -1000, 1000, moveToRow,
                                                  moveToColumn)    # Der Wert wird gleich ermittelt wie bei "place".
                        board[row][column] = player     # Und auch dieser Zug wird wieder rückgängig gemacht.
                        board[moveToRow][moveToColumn] = " "
                        if a:
                            board[b][c] = enemyPlayer
                        if value > bestValue:   # Falls de rZug besser ist, muss man alle Werte erneuern.
                            bestRow = moveToRow
                            bestColumn = moveToColumn
                            replaceRow = row
                            replaceColumn = column
                            bestValue = value
    Minimax_move(bestRow, bestColumn, replaceRow, replaceColumn, player, enemyPlayer)   # Und der beste Zug wird
    # ausgeführt


# Auch die Minimax()-Funktion ist ähnlich. Das einzige, was anders ist, ist die tatsache, dass man den Stein wieder von
# einer Position an eine benachbarte verschiebt.
def Minimax_minimaxMove(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn):
    score = evaluationMove(player, enemyPlayer, lastRow, lastColumn)
    if score < -1000:
        return -1000 + depth
    elif score > 1000:
        return 1000 - depth
    elif depth == MAXDEPTH:
        return score

    if isMaximizer:
        bestValue = -1000
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == player:
                    nextToList = nextTo[row][column]
                    for field in nextToList:
                        if board[field[0]][field[1]] == " ":
                            moveToRow = field[0]
                            moveToColumn = field[1]
                            board[moveToRow][moveToColumn] = player
                            board[row][column] = " "
                            a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, row, column, "move")
                            value = Minimax_nextPhase(20, player, enemyPlayer, depth + 1, False, alpha, beta, moveToRow,
                                                      moveToColumn)
                            bestValue = max(bestValue, value)
                            board[row][column] = player
                            board[moveToRow][moveToColumn] = " "
                            if a:
                                board[b][c] = enemyPlayer
                            alpha = max(alpha, bestValue)
                            if beta <= alpha:
                                break
        return bestValue
    else:
        bestValue = 1000
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == enemyPlayer:
                    nextToList = nextTo[row][column]
                    for field in nextToList:
                        if board[field[0]][field[1]] == " ":
                            moveToRow = field[0]
                            moveToColumn = field[1]
                            board[moveToRow][moveToColumn] = enemyPlayer
                            board[row][column] = " "
                            a, b, c = Minimax_furtherActionChecking(enemyPlayer, player, row, column, "move")
                            value = Minimax_nextPhase(20, player, enemyPlayer, depth + 1, True, alpha, beta, moveToRow,
                                                      moveToColumn)
                            bestValue = min(bestValue, value)
                            board[row][column] = enemyPlayer
                            board[moveToRow][moveToColumn] = " "
                            if a:
                                board[b][c] = player
                            beta = min(beta, bestValue)
                            if beta <= alpha:
                                break
        return bestValue


# Die alte Position wird wieder freigesetzt und die neue in Beschlag genommen.
def Minimax_move(newRow, newColumn, oldRow, oldColumn, player, enemyPlayer):
    board[newRow][newColumn] = player
    board[oldRow][oldColumn] = " "
    nextTurn()
    updateGUI()
    a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, newRow, newColumn, "move")
    if win(enemyPlayer):    # In der "move"-Phase kann man neu gewinnen.
        infoLabel2Update("win", player)     # Wenn man gewinnt wird dies unten im Fenster angezeigt.
        top = Toplevel()    # Es erscheint auch noch ein neues Fenster, welches einem die Optionen auf einen Neustart
        # oder ein Schlissen des Spieles gibt.
        top.title("Gratulation")
        top.geometry("200x100+1500+600")
        Label(top, text="Spieler {} hat gewonnen".format(player)).pack()
        Button(top, text="Neustart", command=restart).pack()
        Button(top, text="Beenden", command=terminate).pack()


# "move" hat andere Koeffiziente und braucht deshalb eine eigene Funktion.
# Quelle: http://www.dasconference.ro/papers/2008/B7.pdf
def evaluationMove(player, enemyPlayer, row, column):
    recentMill, existingMills, blockedPiecesDifference, pieceDifference, nearlyMills, threeConfigurations, \
    doubleMills, winning = evaluation(player, enemyPlayer, row, column)

    score = 14 * recentMill + 43 * existingMills + 10 * blockedPiecesDifference + 11 * pieceDifference + \
            8 * doubleMills + 1086 * winning
    return score


# Jump
# "jump" ist sehr ähnlich wie "move", der Unteschied ist, dass man den Stein an jede freie Position setzen kann und
# nicht nur an jede Benachbarte.
def Minimax_findBestJump(player, enemyPlayer):
    bestValue = -1000
    bestRow = -1
    bestColumn = -1
    replaceRow = -1
    replaceColumn = -1
    for row in range(0, 7):
        for column in range(0, 7):
            if board[row][column] == player:
                for jumpToRow in range(0, 7):
                    for jumpToColumn in range(0, 7):
                        if board[jumpToRow][jumpToColumn] == " ":
                            board[jumpToRow][jumpToColumn] = player
                            board[row][column] = " "
                            a,b,c = Minimax_furtherActionChecking(player, enemyPlayer, jumpToRow, jumpToColumn, "jump")
                            value = Minimax_nextPhase(20, player, enemyPlayer, 0, False, -1000, 1000, jumpToRow,
                                                      jumpToColumn)
                            board[row][column] = player
                            board[jumpToRow][jumpToColumn] = " "
                            if a:
                                board[b][c] = enemyPlayer
                            if value > bestValue:
                                bestRow = jumpToRow
                                bestColumn = jumpToColumn
                                replaceRow = row
                                replaceColumn = column
                                bestValue = value
    Minimax_jump(bestRow, bestColumn, replaceRow, replaceColumn, player, enemyPlayer)


def Minimax_minimaxJump(player, enemyPlayer, depth, isMaximizer, alpha, beta, lastRow, lastColumn):
    score = evaluationJump(player, enemyPlayer, lastRow, lastColumn)
    if score < -1000:
        return -1000 + depth
    elif score > 1000:
        return 1000 - depth
    elif depth >= MAXDEPTHJUMP:
        return score

    if isMaximizer:
        bestValue = -1000
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == player:
                    for jumpToRow in range(0, 7):
                        for jumpToColumn in range(0, 7):
                            if board[jumpToRow][jumpToColumn] == " ":
                                board[jumpToRow][jumpToColumn] = player
                                board[row][column] = " "
                                a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, row, column, "jump")
                                value = Minimax_nextPhase(20, player, enemyPlayer, depth + 1, False, alpha, beta,
                                                          jumpToRow, jumpToColumn)
                                bestValue = max(bestValue, value)
                                board[row][column] = player
                                board[jumpToRow][jumpToColumn] = " "
                                if a:
                                    board[b][c] = enemyPlayer
                                alpha = max(alpha, bestValue)
                                if beta <= alpha:
                                    break
        return bestValue
    else:
        bestValue = 1000
        for row in range(0, 7):
            for column in range(0, 7):
                if board[row][column] == enemyPlayer:
                    for jumpToRow in range(0, 7):
                        for jumpToColumn in range(0, 7):
                            if board[jumpToRow][jumpToColumn] == " ":
                                board[jumpToRow][jumpToColumn] = enemyPlayer
                                board[row][column] = " "
                                a, b, c = Minimax_furtherActionChecking(enemyPlayer, player, row, column, "jump")
                                value = Minimax_nextPhase(20, player, enemyPlayer, depth + 1, False, alpha, beta,
                                                          jumpToRow, jumpToColumn)
                                bestValue = min(bestValue, value)
                                board[row][column] = enemyPlayer
                                board[jumpToRow][jumpToColumn] = " "
                                if a:
                                    board[b][c] = player
                                beta = min(beta, bestValue)
                                if beta <= alpha:
                                    break
        return bestValue


def Minimax_jump(newRow, newColumn, oldRow, oldColumn, player, enemyPlayer):
    board[newRow][newColumn] = player
    board[oldRow][oldColumn] = " "
    nextTurn()
    updateGUI()
    a, b, c = Minimax_furtherActionChecking(player, enemyPlayer, newRow, newColumn, "jump")
    if win(enemyPlayer):
        infoLabel2Update("win", player)
        top = Toplevel()
        top.title("Gratulation")
        top.geometry("200x100+1500+600")
        Label(top, text="Spieler {} hat gewonnen".format(player)).pack()
        Button(top, text="Neustart", command=restart).pack()
        Button(top, text="Beenden", command=terminate).pack()


def evaluationJump(player, enemyPlayer, row, column):
    recentMill, existingMills, blockedPiecesDifference, pieceDifference, nearlyMills, threeConfigurations, \
    doubleMills, winning = evaluation(player, enemyPlayer, row, column)

    score = 16 * recentMill + 10 * nearlyMills + threeConfigurations + 1190 * winning
    return score


# Human player
# Auch ein menschlicher Spieler hat die 3 Phasen. Im Gegensatz zum Minimax, braucht der Mensch zwei Klicks um einen
# Stein zu bewegen oder um zu springen. Diese Aktionen werden deshalb in zwei Schritte aufgeteilt. Jenachdem, was der
# "turnState" ist, wird der eine oder andere Schritt des  Zuges ausgeführt.
def Human_play(player, enemyPlayer, phase, row, column, moveJumpState):
    if phase == "place":
        Human_place(player, enemyPlayer, row, column)
    elif phase == "move":
        if moveJumpState == 0:
            Human_moveStep1(player, row, column)
        else:
            Human_moveStep2(player, enemyPlayer, row, column)
    else:
        if moveJumpState == 0:
            Human_jumpStep1(player, row, column)
        else:
            Human_jumpStep2(player, enemyPlayer, row, column)


# Um als Menschen einen Stein zu plazieren muss man nur das Feld anwählen, welches man besetzen möchte. "row" und
# "column" sind die Positionen, welche die clickGrid()-Funktion ermittelt hat.
def Human_place(player, enemyPlayer, row, column):
    if board[row][column] == " ":   # Wenn das Feld frei ist, kann es besetzt werden
        board[row][column] = player     # Das Feld erhält dann einen neuen Wert auf dem Spielbrett.
        Human_furtherActionCheck(row, column, player, enemyPlayer)  # Dann wird überprüft,ob man eine Mühle geschlossen
        # hat oder sogar gewonnen hat. In dieser Funktion wird der Zug auch beendet.
        updateGUI()   # Und der Zug wird auf dem GUI angezeigt.
    else:   # Falls das Feld schon besetzt war, wird kein Stein gesetzt und "turnState" bleibt 0, was bedeutet, dass der
        # Spieler nochmals am Zug ist und eine Gültige Position für seinen Stein aussuchen kann.
        print("Schon besetzt")  # In der Konsole steht zusätzlich, dass der Zug nicht gültig war.


# Diese Funktion führt den ersten Schritt der "move" Funktion aus.
def Human_moveStep1(player, row, column):
    global lastRow, lastColumn, turnState, moveJumpOptions
    moveJumpOptions = []    # Wenn diese Funktion aufgerufen wird, muss die Liste leer sein.
    if board[row][column] == player:    # Das erste Kriterium für einen gültigen Zug ist, dass der Spieler auf dem Feld
        # einen Stein hat,
        for field in nextTo[row][column]:   # Da die Aktion in zwei Schritten asgeführt wird und man Werte nicht so
            # einfach mitgeben kann, da die zwei Schritte durch zwei unabhängige Funktionen gestartet werden, muss man
            # die benachbarten Felder global hinterlegen.
            if board[field[0]][field[1]] == " ":    # Man überprüft zuerst, welche benachbarten Felder frei sind
                moveJumpOptions.append(field)   # Und fügt diese dann zur globalen Liste "moveJumpOptions" hinzu.
        lastRow = row   # Man darf das Feld auch noch nicht leeren, weil es möglich wäre, dass der zweite Teil des Zuges
        lastColumn = column     # nicht gültig ist und dann findet der Zug nicht statt.
        turnState = 1   # Der erste Schritt ist getan, deshalb wird "turnState" 1.


# Im zweiten Schrittder Bewegung wird der erste Stein entfernt und am neuen Ort wieder plaziert.
def Human_moveStep2(player, enemyPlayer, row, column):
    global lastRow, lastColumn, turnState, moveJumpOptions
    if [row, column] in moveJumpOptions:    # Es wird überprüft, ob die Position, an die man gehen möchte, ein
        # benachbartes und freies Feld ist.
        board[lastRow][lastColumn] = " "    # Wenn schon, wird der Stein an der alten Position entfernt
        board[row][column] = player     # und an der neuen wieder plaziert.
        lastRow = -1    # "lastRow", "lastColumn" und "moveJumpOptions" werden wieder zurückgesetzt.
        lastColumn = -1
        moveJumpOptions = []
        Human_furtherActionCheck(row, column, player, enemyPlayer)  # Auch hier wird überprüft, ob eine Mühle
        # geschlossen oder das Spiel gewonnen wurde.
        updateGUI()     # Die neuen Ereignisse werden grafisch dargestellt.
    else:   # Falls der zweite Teil des Zuges nicht legitim war, wird nocheinmal mit dem ersten Schritt begonnen.
        turnState = 0


# Die "jump"-Aktion wird auch in zwei teilen durchgeführt. "jump" ist wie "move", ausser das man auf jedes freie Feld
# springen kann und nicht nur auf die Benachbarten.
def Human_jumpStep1(player, row, column):
    global lastRow, lastColumn, turnState, moveJumpOptions
    if board[row][column] == player:
        lastRow = row
        lastColumn = column
        turnState = 1


def Human_jumpStep2(player, enemyPlayer, row, column):
    global lastRow, lastColumn, turnState, moveJumpOptions
    if board[row][column] == " ":
        board[lastRow][lastColumn] = " "
        board[row][column] = player
        lastRow = -1
        lastColumn = -1
        moveJumpOptions = []
        Human_furtherActionCheck(row, column, player, enemyPlayer)
        updateGUI()
    else:
        turnState = 0


# Wenn ein menschlicher Spieler eine Mühle schliesst darf auch er einen gegnerischen Stein entfernen.
def Human_removeEnemy(player, enemyPlayer, row, column):
    global turnState, top
    accept = False  # "accept" beschreibt, ob dieser Stein entfernt werden darf. Am Anfang ist "accept" False
    if board[row][column] == enemyPlayer and mill(row, column, enemyPlayer):    # Wenn der Stein in einer Mühle ist, ist
        # es nur erlaubt diesen zu entfernen, wenn es keinen gegnerischen Stein ausserhalb einer Mühle gibt.
        accept = True   # "accept" wird auf True gessetzt, aber wenn ein Stein ausserhalb einer Mühle gefunden wird,
        # wird "accept" wieder zu False
        for i in range(0, 7):
            for j in range(0, 7):
                if board[i][j] == enemyPlayer:  # Man sucht jeden gegnerischen Stein
                    if not mill(i, j, enemyPlayer):   # und falls einer nicht in einer Mühle ist, wird "accept" False
                        accept = False
    if board[row][column] == enemyPlayer and not mill(row, column, enemyPlayer):    # Falls der Stein nicht in einer
        # Mühle ist, wird "accept" True
        accept = True
    if accept:  # Wenn "accept" True ist, darf der Stein entfernt werden.
        board[row][column] = " "    # Der Stein wird entfernt, der Zug beendet und das Fenster wird aktualisiert
        updateGUI()
        nextTurn()
        infoLabel2Update("clear", 0)
        if win(enemyPlayer):    # Wenn der Spieler durch das entfernen gewonnen hat, erscheint das Fenster, welches
            # mitteilt, dass das Spiel vorüber ist.
            infoLabel2Update("win", player)
            top = Toplevel()
            top.title("Gratulation")
            top.geometry("200x100+1500+600")
            Label(top, text="Spieler {} hat gewonnen".format(player)).pack()
            Button(top, text="Neustart", command=restart).pack()
            Button(top, text="Beenden", command=terminate).pack()
    else:   # Falls ein ungültiger Gegner audgewählt wurde muss der Spieler ein neues Feld wählen
        print("Falsche eingabe")


# Diese  Funktion überprüft, ob der Spieler eine Mühle geschlossen oder gewonnen hat.
def Human_furtherActionCheck(row, column, player, enemyPlayer):
    global turnState, top
    if mill(row, column, player):   # Falls eine Mühle geschlossen wurde, darf ein Gegner entfernt werden.
        turnState = 2   # Dafür wird "turnState" auf 2 gesetzt.
        infoLabel2Update("capture", 0)  # Unten am Fenster steht nun, dass ein Gegner entfern werden darf.
    else:
        nextTurn()  # Wenn keine Mühle geschlossen wurde, ist der Zug fertig.
    if win(enemyPlayer):    # Falls der Spieler durch den Zug gewonnen hat, ist das Spiel beendet.
        infoLabel2Update("win", player)
        top = Toplevel()
        top.title("Gratulation")
        top.geometry("200x100+1500+600")
        Label(top, text="Spieler {} hat gewonnen".format(player)).pack()
        Button(top, text="Neustart", command=restart).pack()
        Button(top, text="Beenden", command=terminate).pack()


# GUI
# Die terminate()-Funktion schliesst das Haupt- und Toplevel-Fenster.
def terminate():
    top.destroy()
    root.destroy()


# Die updateGUI()-Funktion stellt das Hauptfenster neu dar.
def updateGUI():
    refreshCells()  # refrechCells() zeigt die aktuellen Steine auf dem Spielbrett dar
    if turn % 2 == 0:   # Wenn die Anzahl  an Zügen durch zwei teilbar ist, ist "X" am Zug
        infoLabel1Update("X")  # Oben im Fenster steht, dass "X" am Zug ist und welcher Zug gerade ist
    else:
        infoLabel1Update("O")   # Das selbe mit "O"
    info2Label.pack()   # Das untere Label wird zusätzlich auch noch angezeigt.


# Diese Funktion refresht die Felder, welche im GUI dargestellt werden, mit den Werten von "board"
def refreshCells():
    for i in range(0, 7):
        for j in range(0, 7):
            if cells[i][j] != "-":  # Der Text jeder Zelle, welche besetzt werden kann, erhält den Text aus "board"
                c.itemconfigure(cells[i][j], text=board[i][j])


# Die Texte der oberen Label werden erneuert und angezeigt.
def infoLabel1Update(player):
    activePlayer.set("Jetzt ist {} am Zug  ".format(player))    # Die Text-Variabeln werden geändert
    activeTurn.set("Es ist der Zug {}".format(turn+1))
    playerLabel.pack(side=LEFT)     # und dargestellt
    turnLabel.pack(side=RIGHT)


# Das untere Label kann ein paar verschiedene Texte darstellen. Welcher Text unten steht, wird über den "action"-String
# mitgeteilt. Wenn jemand gewonnen hat, ist es auch wichtig, dass mitgeliefert wird, welcher Spieler gewonnen hat.
def infoLabel2Update(action, player):
    if action == "clear":   # Wenn "action" "clear" ist, wird nichts dargestellt.
        info2Text.set("")
        info2Label.pack()   # Wichtig ist, dass man das Label immer neu darstellt, nachdem man es verändert hat.
    elif action == "capture":   # Wenn "action" "capture" ist, darf ein menschlicher Spieler einen Gegner entfernen
        info2Text.set("Du kannst einen Gegner entfernen!")  # Das steht dann unten im Fenster.
        info2Label.pack()
    elif action == "win":   # Bei "win" hat jemand gewonnen, was auchunten steht.
        info2Text.set("{} hat gewonnen!".format(player))
        info2Label.pack()
    elif action == "minimax":   # Falls Minimax am Zug ist, steht, dass er am überlegen ist
        info2Text.set("Minimax überlegt...")
        info2Label.pack()


root = Tk()   # "root" ist der Name des Hauptfenster

root.title("Mühle")     # Der Titel des Fenster ist "Mühle"
root.geometry("550x450+900+450")   # Das Fenster hat die Grösse 550 auf 450 Pixel und das Pixel 0/0 wird an Position
# 900/450 vom Bildschirm dargestellt.
root.resizable(width=False, height=False)   # Das grösse des Fensters ist nicht durch den Benutzer veränderbar

menu = Menu(root)   # Das Fenster hat ein drop-down-Menu, wo man das Spiel neustarten kann oder das Fenster schliessen
root.config(menu=menu)
settings = Menu(menu)
menu.add_cascade(label="Einstellungen", menu=settings)  # Der Name des Menus ist "Einstellungen"

settings.add_command(label="Neustart", command=restart)     # Die zwei Funktionen im Menu werden erstellt und benannt
settings.add_command(label="Beenden", command=root.destroy)

infoFrame = Frame(root, width=550, height=25)   # Um das Fenster schön strukturieren zu können, wird es in kleinere
c = Canvas(root, width=400, height=400)     # zusammengehörige Regionen aufgeteilt, welche alle eine bestimmte grösse
selectPlayerFrame = Frame(root, width=150, height=400)    # haben das Hauptfeld ist ein "Canvas"
infoFrame2 = Frame(root, width=550, height=25)

boardStatus = StringVar()   # Um die Texte ändern zu können, werden sie als Variabeln definiert
activePlayer = StringVar()
activeTurn = StringVar()
info2Text = StringVar()
gameModeX = IntVar()
gameModeO = IntVar()

gameModeX.set(1)    # Als Voreinstellung des aktiven Spielers wird "human" gewählt.
gameModeO.set(1)

playerLabel = Label(infoFrame, textvariable=activePlayer)   # Die 3 Label, welche den kommentiern, was gerade geschieht,
turnLabel = Label(infoFrame, textvariable=activeTurn)   # werden mit ihren Textvariabeln erstellt.
info2Label = Label(infoFrame2, textvariable=info2Text)

Label(selectPlayerFrame, text="Spieler X:").pack()      # Über die Radiobuttons wird gesagt, in welchem Modus ein
Radiobutton(selectPlayerFrame, text="Mensch", variable=gameModeX, value=1, command=askForX).pack()  # Spieler ist
Radiobutton(selectPlayerFrame, text="Minimax", variable=gameModeX, value=2, command=askForX).pack()

Label(selectPlayerFrame, text="Spieler O:").pack()
Radiobutton(selectPlayerFrame, text="Mensch", variable=gameModeO, value=1, command=askForO).pack()
Radiobutton(selectPlayerFrame, text="Minimax", variable=gameModeO, value=2, command=askForO).pack()

c.bind("<Button-1>", getClick)  # Dies ist ein wichtiger Teil des Spieles. Jetzt erkennt der Canvas den Mausklick.

infoFrame.pack(side=TOP)    # Die Frames und der Canvas werden plaziert und dargestellt.
infoFrame2.pack(side=BOTTOM)
c.pack(side=LEFT)
selectPlayerFrame.pack(side=RIGHT)

# Die einzelnen Felder auf dem Brett werden als einzelne Objekte, mit bestimmten Koordinaten, auf dem Canvas definiert.
cell00 = c.create_text(29, 29, text=board[0][0], font="Arial 18")
cell03 = c.create_text(200, 29, text=board[0][3], font="Arial 18")
cell06 = c.create_text(371, 29, text=board[0][6], font="Arial 18")
cell11 = c.create_text(86, 86, text=board[1][1], font="Arial 18")
cell13 = c.create_text(200, 86, text=board[1][3], font="Arial 18")
cell15 = c.create_text(314, 86, text=board[1][5], font="Arial 18")
cell22 = c.create_text(143, 143, text=board[2][2], font="Arial 18")
cell23 = c.create_text(200, 143, text=board[2][3], font="Arial 18")
cell24 = c.create_text(257, 143, text=board[2][4], font="Arial 18")
cell30 = c.create_text(29, 200, text=board[3][0], font="Arial 18")
cell31 = c.create_text(86, 200, text=board[3][1], font="Arial 18")
cell32 = c.create_text(143, 200, text=board[3][2], font="Arial 18")
cell34 = c.create_text(257, 200, text=board[3][4], font="Arial 18")
cell35 = c.create_text(314, 200, text=board[3][5], font="Arial 18")
cell36 = c.create_text(371, 200, text=board[3][6], font="Arial 18")
cell42 = c.create_text(143, 257, text=board[4][2], font="Arial 18")
cell43 = c.create_text(200, 257, text=board[4][3], font="Arial 18")
cell44 = c.create_text(257, 257, text=board[4][4], font="Arial 18")
cell51 = c.create_text(86, 314, text=board[5][1], font="Arial 18")
cell53 = c.create_text(200, 314, text=board[5][3], font="Arial 18")
cell55 = c.create_text(314, 314, text=board[5][5], font="Arial 18")
cell60 = c.create_text(29, 371, text=board[6][0], font="Arial 18")
cell63 = c.create_text(200, 371, text=board[6][3], font="Arial 18")
cell66 = c.create_text(371, 371, text=board[6][6], font="Arial 18")

# Um sie zu verändern muss man auf sie zugreifen können. Am einfachsten geht dies, wenn man sie in einer Matrix an ihren
# Positionen im Feld plaziert.
cells = [[cell00, "-", "-", cell03, "-", "-", cell06],
         ["-", cell11, "-", cell13, "-", cell15, "-"],
         ["-", "-", cell22, cell23, cell24, "-", "-"],
         [cell30, cell31, cell32, "-", cell34, cell35, cell36],
         ["-", "-", cell42, cell43, cell44, "-", "-"],
         ["-", cell51, "-", cell53, "-", cell55, "-"],
         [cell60, "-", "-", cell63, "-", "-", cell66]]

# Der Ort jeder Linie muss auch über die Koordinaten definiert werden.
line1 = c.create_line(43, 29, 186, 29)
line2 = c.create_line(214, 29, 357, 29)
line3 = c.create_line(29, 43, 29, 186)
line4 = c.create_line(29, 214, 29, 357)
line5 = c.create_line(43, 371, 186, 371)
line6 = c.create_line(214, 371, 357, 371)
line7 = c.create_line(371, 43, 371, 186)
line8 = c.create_line(371, 214, 371, 357)
line9 = c.create_line(100, 86, 186, 86)
line10 = c.create_line(214, 86, 300, 86)
line11 = c.create_line(86, 100, 86, 186)
line12 = c.create_line(86, 214, 86, 300)
line13 = c.create_line(100, 314, 186, 314)
line14 = c.create_line(214, 314, 300, 314)
line15 = c.create_line(314, 100, 314, 186)
line16 = c.create_line(314, 214, 314, 300)
line17 = c.create_line(157, 143, 186, 143)
line18 = c.create_line(214, 143, 243, 143)
line19 = c.create_line(143, 157, 143, 186)
line20 = c.create_line(143, 214, 143, 243)
line21 = c.create_line(157, 257, 186, 257)
line22 = c.create_line(214, 257, 243, 257)
line23 = c.create_line(257, 157, 257, 186)
line24 = c.create_line(257, 214, 257, 243)
line25 = c.create_line(200, 43, 200, 72)
line26 = c.create_line(200, 100, 200, 129)
line27 = c.create_line(200, 271, 200, 300)
line28 = c.create_line(200, 328, 200, 357)
line29 = c.create_line(43, 200, 72, 200)
line30 = c.create_line(100, 200, 129, 200)
line31 = c.create_line(271, 200, 300, 200)
line32 = c.create_line(328, 200, 357, 200)

# Das GUI wird nun zum ersten Mal dargestellt.
updateGUI()

# mainloop() braucht man, um das Fenster angezeigt zu lassen.
root.mainloop()

# IMPORT #
import random
import os
import time
from colorama import Fore, Back, Style, init 
init(convert=True)

# CLASSES #

# PLAYER CLASS #
# The player class that gives them the ability to do their game functions #
# Also keeps track if they are a computer #
class Player:
    def __init__(self, player, hand, handsize, comp, win):
        self.player = player
        self.hand = hand
        self.handsize = handsize
        self.comp = comp
        self.win = win
    def drawCard(self, deck):
        try:
            x = deck.cards[0]
            self.hand.append(x)
            deck.cards.remove(x)
        except:
            print("Have to reshuffle the deck!")
            deck.reshuffle()
            self.drawCard(deck)
    def punish(self, x, deck):
        for i in range(x):
            self.drawCard(deck)
    def drawHand(self, deck):
        i = 1
        while i <= self.handsize:
            self.drawCard(deck)
            i = i + 1
    def printHand(self):
        x = 1
        for card in self.hand:
            if card.style == 'reverse':
                print(str(x) + '. ' + card.color + " " + card.style)
            elif card.style == 'skip':
                print(str(x) + '. ' + card.color + " " + card.style)
            else:
                print(str(x) + '. ' + str(card))
            x = x + 1
    def playCard(self, card, game, deck):
        try:
            # x is the selected card
            x = self.hand[int(card)-1]
            # y is the top card 
            y = game.cards[(len(game.cards) - 1)]
            # If the card is a wildcard
            if x.color == 'wild':
                # Removes card
                self.hand.remove(x)
                # Pick color
                print("What color do you want it to be? Type R for red, G for Green, B for Blue, Y for Yellow")
                color = input(">>  ")
                if color.lower() == 'r':
                    color = 'red'
                elif color.lower() == 'b':
                    color = 'blue'
                elif color.lower() == 'g':
                    color = 'green'
                elif color.lower() == 'y':
                    color = 'yellow'
                else:
                    color = 'red'
                x.color = color
                # If its a plus card
                if (x.style == 'wildcard+'):
                    game.cards.append(x)
                    if not self.hand:
                        self.win = True
                    return x.value
                else:
                    #x.value = 10
                    game.cards.append(x)
                    if not self.hand:
                        self.win = True
                    return False
            # If the color or value matches || For number cards
            if x.color is y.color or x.value is y.value:
                game.cards.append(x)
                self.hand.remove(x)
                # Check Win
                if not self.hand:
                    self.win = True
                if x.style == 'skip':
                    return 3
                elif x.style == 'reverse':
                    print("The order is reversed!")
                    return True
                elif x.style == 'plus':
                    return 2
                else :
                    return False
            else:
                print("Sorry that doesn't work!")
                self.drawCard(deck)
                print("You draw!")
                return False
        except:
            print("Sorry not recognized!")
            self.drawCard(deck)
            return False
    def computerPlay(self, game, x):
        # Plays card for computer player
        self.hand.remove(x)
        # Check if wild
        if x.color != 'wild':
            if x.style != 'plus':
                game.cards.append(x)
            else:
                return 2
        # Check Win
        if not self.hand:
            self.win = True
        # Return Statement
        if x.style == 'skip':
            return 3
        elif x.style == 'reverse':
            print("The order has been reversed!")
            return True
        elif x.color == 'wild':
            colors = ['red', 'green', 'blue', 'red']
            x.color = random.choice(colors)
            if x.value == 4:
                game.cards.append(x)
                return x.value
            else:
                game.cards.append(x)
                return False
        else:
            return False
    def __str__(self):
        if self.comp == False:
            return (Fore.BLUE + "Player " + str(self.player)+Fore.WHITE)
        else:
            return (Fore.RED + "Player " + str(self.player)+Fore.WHITE)


# CARD CLASS #
# Main class for all of the UNO cards #
class Card:
    def __init__(self, style, color, value):
        self.style = style
        self.color = color
        self.value = value
    def __str__(self):
        if self.color == 'red':
            if self.style == 'number' or 'wildcard+':
                return (Fore.RED + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.RED + self.color+ " "+self.style+Fore.WHITE+"")
        elif self.color == 'blue':
            if self.style == 'number' or 'wildcard+':
                return (Fore.BLUE + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.BLUE + self.color+ " "+self.style+Fore.WHITE+"")
        elif self.color == 'green':
            if self.style == 'number' or 'wildcard+':
                return (Fore.GREEN + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.GREEN + self.color+ " "+self.style+Fore.WHITE+"")
        elif self.color == 'yellow':
            if self.style == 'number' or 'wildcard+':
                return (Fore.YELLOW + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.YELLOW + self.color+ " "+self.style+Fore.WHITE+"")
        elif self.color == 'wild':
            if self.style == 'number' or 'wildcard+':
                return (Fore.WHITE + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.WHITE + self.color+ " "+self.style+Fore.WHITE+"")
        else:
            if self.style == 'number' or 'wildcard+':
                return (Fore.WHITE + self.color+ " "+str(self.value)+Fore.WHITE+"")
            else:
                return (Fore.WHITE + self.color+ " "+self.style+Fore.WHITE+"")

# DECK CLASS #
# This Class encompasses the decks that are created #
class Deck:
    def __init__(self, cards, size):
        self.cards = cards
        self.size = size
    # Function that creates deck and fills it
    def fill(self):
        styles = ['number']
        colors = ['red', 'green', 'yellow', 'blue']
        numbers = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        # This adds all of the number cards
        self.cards = [Card(style, color, value) for value in numbers for color in colors for style in styles]
        # This adds all the wildcards
        wildcard = Card('wildcard', 'wild', 0)
        wildFour = Card('wildcard+', 'wild', '+4')
        i = 1
        while i <= 4:
            self.cards.append(wildcard)
            self.cards.append(wildFour)
            i += 1
        for i in range(2): 
            for color in colors:
                drawTwo = Card('plus', color, '+2')
                self.cards.append(drawTwo)
        for i in range(2): 
            for color in colors:
                skip = Card('skip', color, 'skip')
                self.cards.append(skip)
        for i in range(2): 
            for color in colors:
                reverse = Card('reverse', color, 'reverse')
                self.cards.append(reverse)
    # Function to sort all of the data
    def shuffleCards(self):
        i = 1
        while i <= 100:
            random.shuffle(self.cards)
            i = i + 1
    # Prints deck
    def printDeck(self):
        x = 1
        for card in self.cards:
            if card.style == 'reverse':
                print(str(x) + '. ' + card.color + " " + card.style)
            elif card.style == 'skip':
                print(str(x) + '. ' + card.color + " " + card.style)
            else:
                print(str(x) + '. ' + card.color + " " + str(card.value))
            x = x +1
    # Prints the size of the deck
    def printSize(self):
        x = len(self.cards)
        print(str(x) + " cards in deck")
    # Reshuffles deck
    def reshuffle(self, game):
        i = 0
        while i != (len(game.cards) - 1):
            x = game.cards
            self.cards.append(x)
            game.cards.remove(x)
            i = i + 1
        self.shuffleCards()

# PLAY AREA CLASS #
# This class encompasses the play area. Essentially the discard pile and what the current cards are. #
# Cards that are played go here #
class PlayArea:
    def __init__(self, cards, list):
        self.cards = cards
        self.list = list
    def startGame(self, deck):
        i = 0
        x = deck.cards[i]
        if x.style == 'wild':
            while x.style == 'wild':
                i += 1
                x = deck.cards[i]
        self.cards.append(x)
        deck.cards.remove(x)
    def show(self):
        x = self.cards[(len(self.cards) - 1)]
        number = (x.value)
        if (number == 10):
            number = x.style
        return str(x)
    def showTop(self):
        x = self.cards[(len(self.cards) - 1)]
        return x

# FUNCTIONS #

# CLear function
def clear():
    os.system('cls')
#Needs a function to show all playable cards
def showPlayable(game, player):
    #Playable cards array
    x = []
    y = game.showTop()
    # Go through the cards
    for card in player.hand:
        # If card is wild, put it in
        if (card.color == 'wild'):
            x.append(card)
        # Check if card matches color
        elif (card.color is y.color):
            x.append(card)
        # Check if card matches number
        elif (card.value is y.value):
            x.append(card)

    #returnshe playable card
    return x


# This function checks if the win condition has been met #
def checkWin(list):
    x = False
    for player in list:
        if player.win is True:
            x = True
    return x

# Function to get winning player
def checkWinner(list):
    for player in list:
        if player.win is True:
            x = player
    return x
# The game menu that is seen every turn #
def gameMenu(game, player, deck):
    print("")
    print(" -- Your Turn --")
    print("")
    player.printHand()
    print("")
    print("Card in Play: -- "+str(game.show())+" --")
    x = input("What card would you like to play? Type "+Fore.YELLOW+"d "+Fore.WHITE+"to "+Fore.YELLOW+"draw a card "+Fore.WHITE+"instead \n\n>>  ")
    if x.lower() == 'd':
        player.drawCard(deck)
        return False
    else:
        y = player.playCard(x, game, deck)
        return y
# This function starts the game #
def startGame(deck, game):
    deck.fill()
    deck.shuffleCards()
    game.startGame(deck)
    for player in game.list:
        player.drawHand(deck)
# Turn for Computer 
def computerTurn(game, player, deck):
    # Show the top card
    game.show()
    p = showPlayable(game, player)
    # If computer has no playable cards, then draw
    if not p:
        player.drawCard(deck)
        print(str(player) + " draws a card and ends their turn.")
        z = len(player.hand)
        print(str(player) + " has a hand size of " + str(z))
        print("")
        return False
    # If computer has playable cards, play a random card
    else:
        played = random.choice(p)
        a = player.computerPlay(game, played)
        print(str(player) + " plays "+ str(played)+" and ends their turn.")
        z = len(player.hand)
        if z == 1:
            print("UNO! " + str(player) + " has a hand size of " + str(z))
        else:
            print(str(player) + " has a hand size of " + str(z))
        print("")
        return a
# Create Players
def createPlayers():
    print(Fore.YELLOW + "Welcome to Uno!")
    print("How many players would you like to have?")
    numb = 1
    x = 2
    z = []
    # Get how many computers there are
    try:
        print(Fore.BLUE + "")
        numb = int(input(">>  "))
        print(Fore.WHITE + "")
    except ValueError:
        print(Back.RED +"Needed a number!" + Back.RESET)
        time.sleep(1)
    # Make sure theres at least one other computer
    if numb < 2:
        print(Back.RED + "Needs at least 2 other players!" + Back.RESET)
        numb = 2
    # Create players
    for player in range(numb):
        z.append(Player(x, [], 7, True, False))
        x += 1
    return z


# Need a function to simulate turns
def turnSystem(game, deck):
    # Diretcion 1 means forward through the array
    # Direction 0 means backwards through the array
    x = 1
    # Maybe game loop here

    # While x = 1, go up one player. if computer, do computer Turn if player do player turn
    # While x = 0, go down one player. If ^^
    # If y is 3, skip turn then continue as x was

    # If something reverses, itll start going backwards. So I need false to keep x as it is, true to change. 3 keeps x the same but adds to index

    # If cant go up one, start at 0
    # If cant go down one, start at len-1

    # The turn functions will return the direction

    # P variable is current player
    # i variable is the index
    # end is the last index
    # This is the start of the game
    i = 0
    end = (len(game.list) - 1)
    p = game.list[i]
    while checkWin(game.list) != True:
        # To give a slight buffer before turns
        time.sleep(0.5)
        # If p is player, do player turn
        if p.comp is False:
            # y variable is the outcome
            y = gameMenu(game, p, deck)
            # Reverse the order
            if y is True:
                # Reverse it if forward, mmake it forward if backwards
                if x == 0:
                    x = 1
                else:
                    x = 0
            # Normal Play
            elif y == False:
                # Do nothing
                pass
            # Skip the next player
            elif y == 3:
                a = p
                if x == 1:
                    try:
                        i += 1
                        p = game.list[i]
                    except:
                        i = 0
                        p = game.list[i]
                else:
                    try:
                        i -= 1
                        p = game.list[i]
                    except:
                        i = end
                        p = game.list[i]
                
                print(str(a)+" skips " + str(p))
            # If the card is plus 2 or plus 4
            elif y == 2 or 4:
                a = p
                if y == 2:
                    d = 2
                else:
                    d = 4
                if x == 1:
                    try:
                        i += 1
                        p = game.list[i]
                    except:
                        i = 0
                        p = game.list[i]
                else:
                    try:
                        i -= 1
                        p = game.list[i]
                    except:
                        i = end
                        p = game.list[i]
                p.punish(d, deck)
                print(str(a) + " makes " + str(p) + " draw " + str(y) + " cards and skips their turn!")

        # -- COMPUTER TURNS -- #
        else:
            y = computerTurn(game, p, deck)
            if y is True:
                # Reverse it if forward, mmake it forward if backwards
                if x == 0:
                    x = 1
                else:
                    x = 0
            elif y == False:
                # Do nothing
                pass
            elif y == 3:
                a = p
                if x == 1:
                    try:
                        i += 1
                        p = game.list[i]
                    except:
                        i = 0
                        p = game.list[i]
                else:
                    try:
                        i -= 1
                        p = game.list[i]
                    except:
                        i = end
                        p = game.list[i]
                
                print(str(a)+" skips " + str(p))
            elif y == 2 or 4:
                a = p
                if y == 2:
                    d = 2
                else:
                    d = 4
                if x == 1:
                    try:
                        i += 1
                        p = game.list[i]
                    except:
                        i = 0
                        p = game.list[i]
                else:
                    try:
                        i -= 1
                        p = game.list[i]
                    except:
                        i = end
                        p = game.list[i]
                p.punish(d, deck)
                print(str(a) + " makes " + str(p) + " draw " + str(y) + " cards and skips their turn!")
        # This is where we will decide to go up or down
        # The try statements make sure if we are at the end of teh order or start, we start again at the other end of the array
        if x == 1:
            try:
                i += 1
                p = game.list[i]
            except:
                i = 0
                p = game.list[0]
        else:
            try:
                i -= 1
                p = game.list[i]
            except:
                i = end
                p = game.list[end]



# MAIN FUNCTION #
def main():
    # Deck Object
    deck = Deck([], 75)
    # Human Player
    me = Player(1, [], 7, False, False)
    # Computer Player
    comp = createPlayers()
    players = [me]
    playerList = players + comp
    # Play Area Object
    game = PlayArea([], playerList)
    startGame(deck, game)
    clear()
    while checkWin(game.list) != True:
        x = turnSystem(game, deck)

    #End game
    a = checkWinner(game.list)
    print(Back.GREEN + Style.BRIGHT + str(a) + " wins!" + Style.RESET_ALL)
    input("Press Enter to close...")

main()

from cardClass import createCardFromString


class Player:
    def __init__(self, name, stackSize, isHuman=False):
        self.name = name
        self.stackSize = stackSize
        self.cards = []
        self.inHand = True
        self.isBusted = False
        self.currentBet = 0
        self.totalContribution = 0
        self.lastAction = None
        self.isHuman = isHuman

    def setCards(self, firstCard, secondCard):
        self.cards = [firstCard, secondCard]

    def getCards(self):
        return self.cards

    # Clears the cards after hand is over
    def clearCards(self):
        self.cards = []

    # Removing player from hand
    def fold(self):
        self.inHand = False
        self.lastAction = 'fold'

    # Marking player as busted
    def bust(self):
        self.isBusted = True

    def bet(self, amount):
        self.stackSize -= amount
        self.currentBet += amount
        self.totalContribution += amount
        self.lastAction = 'bet' if amount > 0 else 'check'

    def call(self, amount):
        self.bet(amount)
        self.lastAction = 'call'

    def raiseBet(self, amount):
        self.bet(amount)
        self.lastAction = 'raise'

    def allIn(self):
        self.bet(self.stackSize)
        self.lastAction = 'all-in'

    def check(self):
        self.lastAction = 'check'

    def __str__(self):
        cardDetails = ', '.join(str(card) for card in self.cards) if self.cards else "No cards"
        status = "Busted" if self.isBusted else "Active"
        inHandStatus = "Folded" if not self.inHand else "Playing"
        return f"Player {self.name}: Cards: {cardDetails} | Stack Size: ${self.stackSize} | Status: {status}, {inHandStatus} | Type: {'Human' if self.isHuman else 'AI'}"


def createPlayersFromDict(playerDict, stackSize):
    players = {}
    for key, value in playerDict.items():
        # Assume 'value' is a list of two card strings
        if len(value) == 2:
            card1 = createCardFromString(value[0])
            card2 = createCardFromString(value[1])
            player = Player(key, stackSize)
            player.setCards(card1, card2)
            players[key] = player
        else:
            raise ValueError("Player must have exactly two cards")
    return players

# Import game phase functions
from preFlop import runPreFlop  # Function handling the pre-flop phase
from flop import runFlop        # Function handling the flop phase
from turn import runTurn        # Function handling the turn phase
from river import runRiver      # Function handling the river phase

# Import other necessary modules or functions
from cardClass import Card, createCardFromString  # Card class for card objects
from handRankings import calculateHandRank, classifyHand  # For hand evaluations
from playerClass import Player  # Assuming you have a Player class defined

# Import functions for player interactions (optional if these exist)
from userInteraction import userMove  # Function for user's move interaction
from computerMove import compMove
import itertools


import random

class GameState:
    def __init__(self, players, initialStack):
        self.players = players  # List of Player objects
        self.hand = []
        self.pot = 0
        self.communityCards = []
        self.current_bet = 0
        self.deck = self.createFullDeck()  # Assumes a method to create a deck
        self.initialStack = initialStack
        self.blinds = self.calculateBlinds(initialStack)  # Method to set blinds
        self.dealerPosition = 0
        self.handCount = 0  # Track the number of hands played
        self.last_aggressive_player = None
        print("Game state initialized.")

    def initializeDeck(self):
        """Initializes a new deck of 52 card objects and shuffles it."""
        self.deck = self.createFullDeck()  # Create a full deck of cards
        random.shuffle(self.deck)  # Shuffle the deck

    def createFullDeck(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return [Card(rank, suit) for rank in ranks for suit in suits]

    def resetRound(self):
        """Resets the game state for the next round."""
        self.pot = 0
        self.current_bet = 0
        self.last_aggressive_player = None

        for player in self.players:
            player.current_bet = 0
            player.is_active = True  # Reactivate all players for the new round

        self.communityCards = []  # Reset community cards for the new round

    def updateGameState(self):
        """Update the game state based on current players' statuses."""
        active_players = [player for player in self.players if player.is_active]

        if len(active_players) == 1:
            winner = active_players[0]
            winner.stack += self.pot
            print(f"{winner.name} wins the pot of {self.pot}!")
            self.pot = 0
            self.resetRound()

    def calculateBlinds(self, stackSize):
        bigBlind = int(0.02 * stackSize)
        smallBlind = bigBlind // 2
        return smallBlind, bigBlind

    def updateBlinds(self):
        self.blinds = (self.blinds[0] * 2, self.blinds[1] * 2)

    def checkAndUpdateBlinds(self):
        if self.handCount % 5 == 0 and self.handCount != 0:
            self.updateBlinds()

    def postBlinds(self):
        smallBlindIndex = (self.dealerPosition + 1) % len(self.players)
        bigBlindIndex = (self.dealerPosition + 2) % len(self.players)
        self.players[smallBlindIndex].bet(self.blinds[0])
        self.players[bigBlindIndex].bet(self.blinds[1])
        self.current_bet = self.blinds[1]

    def dealCommunityCard(self, count=1):
        for _ in range(count):
            card = self.cardGenerator()
            if card:
                self.communityCards.append(card)

    def cardGenerator(self):
        if self.deck:
            return self.deck.pop()  # Pops a card from the shuffled deck list
        return None

    def dealPlayerCards(self):
        for player in self.players:
            firstCard = self.cardGenerator()
            secondCard = self.cardGenerator()
            if firstCard and secondCard:
                player.setCards(firstCard, secondCard)
                print(f"{player.name} has been dealt: {firstCard}, {secondCard}")

    def playHand(self):
        """Manages the overall flow of the game hand."""
        self.initializeDeck()  # Initialize and shuffle the deck at the start of each hand
        runPreFlop(self)

        if self.checkForActivePlayers():
            runFlop(self)
        if self.checkForActivePlayers():
            runTurn(self)
        if self.checkForActivePlayers():
            runRiver(self)
        if self.checkForActivePlayers():
            self.showdown()

    def getPlayerMove(self, currentPlayer):
        if currentPlayer.isHuman:
            betSize, action = userMove(self.current_bet, currentPlayer.stackSize)
        else:
            betSize, action = compMove(currentPlayer.getCards(), self.communityCards, 'preflop',
                                       currentPlayer.stackSize, self.current_bet)
        return betSize, action

    def clearScreen(self):
        if os.name == 'nt':
            os.system('cls')  # Clear screen for Windows
        else:
            os.system('clear')  # Clear screen for Unix/Linux/Mac

    def showdown(self):
        active_players = [p for p in self.players if p.is_active]
        if len(active_players) > 1:
            winner = self.determineWinner(active_players)
            winner.stack += self.pot
            print(f"{winner.name} wins the pot of {self.pot} with {winner.hand}")
        else:
            print("Error: Not enough players in showdown.")

        self.resetRound()

    def prepareNextHand(self):
        self.initializeDeck()  # Reinitialize the deck for the next hand
        self.communityCards.clear()
        self.current_bet = 0
        self.pot = 0
        for player in self.players:
            player.clearCards()
            player.inHand = not player.isBusted
            player.current_bet = 0
        self.dealerPosition = (self.dealerPosition + 1) % len(self.players)
        self.dealPlayerCards()
        self.postBlinds()

    def evaluateBestHand(self, all_cards):
        best_hand = max(itertools.combinations(all_cards, 5), key=lambda hand: calculateHandRank(hand))
        return best_hand, calculateHandRank(best_hand)

    def __str__(self):
        return (f"Current Pot: {self.pot}\n" +
                f"Community Cards: {' '.join(str(card) for card in self.communityCards)}\n" +
                f"Current Bet: {self.current_bet}\n" +
                f"Blinds: {self.blinds[0]} (small), {self.blinds[1]} (big)\n" +
                f"Hand Count: {self.handCount}")


import itertools
import random
import os

from cardClass import createCardFromString
from handRankings import calculateHandRank, classifyHand
from preFlop import runPreFlop
from flop import runFlop
from turn import runTurn
from river import runRiver
from userInteraction import userMove
from computerMove import compMove


class GameState:
    def __init__(self, players, initialStack):
        self.players = players  # List of Player objects
        self.pot = 0
        self.communityCards = []
        self.currentBet = 0
        self.deck = self.createFullDeck()
        self.initialStack = initialStack
        self.blinds = self.calculateBlinds(initialStack)
        self.handCount = 0  # Track the number of hands played
        self.dealerPosition = 0

    def createFullDeck(self):
        suits = {'H': 'Hearts', 'D': 'Diamonds', 'S': 'Spades', 'C': 'Clubs'}
        ranks = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'T': 'T', 'J': 'J',
                 'Q': 'Q', 'K': 'K', 'A': 'A'}
        return {f"{rank}{suit}": 1 for rank in ranks for suit in suits}

    def calculateBlinds(self, stackSize):
        bigBlind = int(0.02 * stackSize)  # Big blind is 2% of initial stack
        smallBlind = bigBlind // 2  # Small blind is half of the big blind
        return smallBlind, bigBlind

    def updateBlinds(self):
        self.blinds = (self.blinds[0] * 2, self.blinds[1] * 2)  # Double the blinds

    def checkAndUpdateBlinds(self):
        if self.handCount % 5 == 0 and self.handCount != 0:  # Update blinds every 5 hands
            self.updateBlinds()

    def postBlinds(self):
        smallBlindIndex = (self.dealerPosition + 1) % len(self.players)
        bigBlindIndex = (self.dealerPosition + 2) % len(self.players)
        self.players[smallBlindIndex].bet(self.blinds[0])
        self.players[bigBlindIndex].bet(self.blinds[1])
        self.currentBet = self.blinds[1]

    def dealCommunityCard(self, count=1):
        for _ in range(count):
            card = self.cardGenerator()
            if card:
                self.communityCards.append(card)

    def cardGenerator(self):
        availableCards = [card for card, isAvailable in self.deck.items() if isAvailable == 1]
        if availableCards:
            chosenCard = random.choice(availableCards)
            self.deck[chosenCard] = 0  # Mark the card as used in the deck
            return chosenCard
        return None

    def dealPlayerCards(self):
        for player in self.players:
            firstCard = self.cardGenerator()
            secondCard = self.cardGenerator()
            if firstCard and secondCard:
                player.setCards(firstCard, secondCard)
                print(f"{player.name} has been dealt: {firstCard}, {secondCard}")

    def playHand(self):
        self.dealPlayerCards()
        self.preflop()
        self.flop()
        self.turn()
        self.river()
        self.handCount += 1  # Increment hand count after playing a hand
        self.checkAndUpdateBlinds()  # Check if blinds need to be updated

    def getPlayerMove(self, currentPlayer):
        if currentPlayer.isHuman:
            betSize, action = userMove(self.currentBet, currentPlayer.stackSize)
        else:
            betSize, action = compMove(currentPlayer.getCards(), self.communityCards, 'preflop',
                                       currentPlayer.stackSize, self.currentBet)
        return betSize, action
    
    def clearScreen(self):
        # Check if the operating system is Windows
        if os.name == 'nt':
            os.system('cls')  # Clear screen for Windows
        else:
            os.system('clear')  # Clear screen for Unix/Linux/Mac

    def preflop(self):
        self.clearScreen()
        print("|           <----------------------------------       FLOP CARDS!!       ----------------------------------------->           |")
        print("\n\n")
        runPreFlop(self)

    def flop(self):
        self.clearScreen()
        print("|           <----------------------------------        TURN CARDS!!         ----------------------------------------->           |")
        print("\n\n")
        runFlop(self)

    def turn(self):
        self.clearScreen()
        print("|           <----------------------------------        RIVER CARDS!!         ----------------------------------------->           |")
        print("\n\n")
        runTurn(self)

    def river(self):
        self.clearScreen()
        print("|           <----------------------------------        BETTING OVER!!        ----------------------------------------->           |")
        print("\n\n")
        runRiver(self)
        self.showdown()

    def playerFold(self, player):
        player.isActive = False  # Mark the player as folded
        self.activePlayers.remove(player)  # Remove from active players list

    def playerCall(self, player):
        callAmount = self.currentBet - player.currentBet
        if player.stackSize > callAmount:
            player.stackSize -= callAmount
            self.pot += callAmount
            player.currentBet = self.currentBet
        else:
            self.playerAllIn(player)

    def playerRaise(self, player, amount):
        if player.stackSize > amount:
            player.stackSize -= amount
            self.pot += amount
            self.currentBet = amount
            player.currentBet = amount
        else:
            self.playerAllIn(player)

    def playerAllIn(self, player):
        allInAmount = player.stackSize
        self.pot += allInAmount
        player.stackSize = 0
        player.isAllIn = True
        self.currentBet = max(self.currentBet, allInAmount)
        player.currentBet = allInAmount

    def playerCheck(self, player):
        if player.currentBet < self.currentBet:
            raise ValueError("Check not allowed, current bet is higher than player's bet.")

    def prepareNextHand(self):
        self.deck = self.createFullDeck()
        self.communityCards.clear()
        self.currentBet = 0
        self.pot = 0
        for player in self.players:
            player.clearCards()
            player.inHand = not player.isBusted
            player.currentBet = 0
        self.dealerPosition = (self.dealerPosition + 1) % len(self.players)
        self.dealPlayerCards()
        self.postBlinds()

    def showdown(self):
        active_players = [player for player in self.players if player.inHand and not player.isBusted]
        if not active_players:
            print("No players available for showdown.")
            return

        # Calculate hand ranks for all remaining players
        for player in active_players:
            player_cards = [createCardFromString(card) if isinstance(card, str) else card for card in player.getCards()]
            all_cards = player_cards + [createCardFromString(card) if isinstance(card, str) else card for card in self.communityCards]
            player.bestHand, player.bestHandRank = self.evaluateBestHand(all_cards)
            player.handType = classifyHand(player.bestHand)
            player.handRank = calculateHandRank(player.bestHand)

        # Determine the winner(s) based on the highest hand rank
        highest_rank = max(player.handRank for player in active_players)
        winners = [player for player in active_players if player.handRank == highest_rank]

        # Pot distribution logic
        if len(winners) == 1:
            winner = winners[0]
            winner.stackSize += self.pot
            print(f"{winner.name} wins the pot of {self.pot} with a {winner.handType}.")
        else:
            # Handle pot split in case of ties
            split_pot = self.pot // len(winners)
            for winner in winners:
                winner.stackSize += split_pot
                print(f"{winner.name} ties and wins {split_pot} with a {winner.handType}.")

        # Reset for the next hand
        self.pot = 0
        self.currentBet = 0
        for player in self.players:
            player.clearCards()
            player.inHand = True if not player.isBusted else False
            player.currentBet = 0

    def evaluateBestHand(self, all_cards):
        best_hand = max(itertools.combinations(all_cards, 5), key=lambda hand: calculateHandRank(hand))
        return best_hand, calculateHandRank(best_hand)

    def __str__(self):
        return (f"Current Pot: {self.pot}\n" +
                f"Community Cards: {' '.join(str(card) for card in self.communityCards)}\n" +
                f"Current Bet: {self.currentBet}\n" +
                f"Blinds: {self.blinds[0]} (small), {self.blinds[1]} (big)\n" +
                f"Hand Count: {self.handCount}")

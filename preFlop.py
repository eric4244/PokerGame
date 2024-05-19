from computerMove import compMove
from userInteraction import userMove


def runPreFlop(gameState):
    currentPlayerIndex = (gameState.dealerPosition + 3) % len(gameState.players)
    firstRound = True
    bettingContinues = True

    smallBlindIndex = (gameState.dealerPosition + 1) % len(gameState.players)
    bigBlindIndex = (gameState.dealerPosition + 2) % len(gameState.players)

    gameState.players[smallBlindIndex].bet(gameState.blinds[0])
    gameState.players[bigBlindIndex].bet(gameState.blinds[1])
    gameState.currentBet = gameState.blinds[1]

    print(f"Small blind of {gameState.blinds[0]} posted by {gameState.players[smallBlindIndex].name}")
    print(f"Big blind of {gameState.blinds[1]} posted by {gameState.players[bigBlindIndex].name}")

    # Tracks the last player to raise or initially post the big blind
    lastAggressivePlayer = bigBlindIndex

    betThisRound = False

    while bettingContinues:
        currentPlayer = gameState.players[currentPlayerIndex]

        if not currentPlayer.inHand or currentPlayer.stackSize == 0:
            print(f"{currentPlayer.name} is not in hand or has 0 stack, skipping...")
            currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
            continue

        print(f"Current bet: {gameState.currentBet}, {currentPlayer.name}'s stack: {currentPlayer.stackSize}")

        # Player move
        amount, move = gameState.getPlayerMove(currentPlayer)
        print(f"{currentPlayer.name} decides to {move} with amount {amount}")

        if move == "fold":
            currentPlayer.fold()
        elif move == "check":
            currentPlayer.check()
        elif move == "call":
            currentPlayer.call(gameState.currentBet - currentPlayer.currentBet)
        elif move == "raise":
            raiseAmount = amount - gameState.currentBet
            currentPlayer.raiseBet(raiseAmount)
            gameState.currentBet = amount
            lastAggressivePlayer = currentPlayerIndex
            betThisRound = True
            print(f"{currentPlayer.name} raises to {gameState.currentBet}. New last aggressive player is index {lastAggressivePlayer}.")
        elif move == "all-in":
            currentPlayer.allIn()
            lastAggressivePlayer = currentPlayerIndex
            betThisRound = True
            print(f"{currentPlayer.name} goes all-in with {currentPlayer.stackSize}.")
        else:
            print("Somehow a move wasn't selected in preflop")

        # Reset firstRound after the big blind has acted once
        if firstRound and currentPlayerIndex == bigBlindIndex:
            firstRound = False

        # Ending betting if currentPlayerIndex is the last player to bet
        if currentPlayerIndex == lastAggressivePlayer and not firstRound and not betThisRound:
            bettingContinues = False

        # Advancing to next player and resting bet variable
        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
        betThisRound = False

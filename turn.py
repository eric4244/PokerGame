from computerMove import compMove
from userInteraction import userMove


def runTurn(gameState):
    # Deal the turn card
    gameState.dealCommunityCard()
    print("Turn card dealt:")
    print(str(gameState.communityCards[-1]))  # Display the newly dealt turn card

    # Begin a round of betting, starting with the player left to the dealer (small blind if active)
    currentPlayerIndex = (gameState.dealerPosition + 1) % len(gameState.players)
    while not gameState.players[currentPlayerIndex].inHand:  # Ensure to start with an active player
        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)

    lastPlayerIndex = (currentPlayerIndex - 1) % len(gameState.players)
    bettingContinues = True
    firstRound = True
    betThisRound = False

    # Tracks the player who played first or the last raise
    lastAggressivePlayer = lastPlayerIndex
    print(f'Last aggressive player is: {lastAggressivePlayer}')

    while bettingContinues:
        currentPlayer = gameState.players[currentPlayerIndex]
        print(f"Player {currentPlayer.name}'s turn. Index: {currentPlayerIndex}")

        # Check if player is still active in the hand
        if not currentPlayer.inHand or currentPlayer.stackSize == 0:
            currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
            continue

        # Player Move
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
            print(
                f"{currentPlayer.name} raises to {gameState.currentBet}. New last aggressive player is index {lastAggressivePlayer}.")
        elif move == "all-in":
            currentPlayer.allIn()
            lastAggressivePlayer = currentPlayerIndex
            betThisRound = True
            print(f"{currentPlayer.name} goes all-in with {currentPlayer.stackSize}.")
        else:
            print("Somehow a move wasn't selected in turn")

        # Reset firstRound after all players have acted once
        if firstRound and currentPlayerIndex == lastPlayerIndex:
            firstRound = False

        # Ending betting if currentPlayerIndex is the last player to bet
        if currentPlayerIndex == lastAggressivePlayer and not firstRound and not betThisRound:
            print("Ending betting round.")
            bettingContinues = False

        # Advancing to next player
        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
        betThisRound = False

    # Prepare for the next stage: the river
    print("Moving to river stage.")
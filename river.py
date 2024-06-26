from computerMove import compMove
from userInteraction import userMove


def runRiver(gameState):
    # Deal the river card
    gameState.dealCommunityCard()
    print(str(gameState.communityCards[-1]))  # Display the newly dealt river card

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

    while bettingContinues:
        currentPlayer = gameState.players[currentPlayerIndex]

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
            print("\nSomehow a move wasn't selected in turn\n")

        # Reset firstRound after all players have acted once
        if firstRound and currentPlayerIndex == lastPlayerIndex:
            firstRound = False

        # Ending betting if currentPlayerIndex is the last player to bet
        if currentPlayerIndex == lastAggressivePlayer and not firstRound and not betThisRound:
            bettingContinues = False

        # Advancing to next player
        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
        betThisRound = False

    # Prepare for showdown if more than one player is still in hand
    if len([p for p in gameState.players if p.inHand]) > 1:
        print("\n\n")
        print("|           <----------------------------------        SHOWDOWN STARTS!!        ----------------------------------------->           |")
        print("\n\n")
        # Call the showdown function to determine the winner
        gameState.showdown()
    else:
        # Only one player remaining, award the pot to them
        winner = next((p for p in gameState.players if p.inHand), None)
        if winner:
            winner.stackSize += gameState.pot
            print(f"{winner.name} wins the pot of {gameState.pot} by default as the last player remaining.")


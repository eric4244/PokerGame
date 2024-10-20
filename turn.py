from computerMove import compMove
from userInteraction import userMove


def runTurn(gameState):
    gameState.gameStage = "turn"
    gameState.currentBet = 0
    # Deal the turn card
    gameState.dealCommunityCard()
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

    while bettingContinues:
        currentPlayer = gameState.players[currentPlayerIndex]

        # Check if player is still active in the hand
        if not currentPlayer.inHand or currentPlayer.stackSize == 0:
            currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
            continue

        # Player Move
        amount, move = gameState.getPlayerMove(currentPlayer)
        print(f"{currentPlayer.name} decides to {move} with amount {amount} \n")

        if move == "fold":
            currentPlayer.is_active = False
            currentPlayer.fold()
        elif move == "check":
            # Check is only allowed if the current bet is 0
            if gameState.currentBet == 0:
                currentPlayer.check()
            else:
                print(f"Error: {currentPlayer.name} tried to check, but the current bet is {gameState.currentBet}.")
        elif move == "call":
            # The player calls the current bet minus what they've already contributed
            callAmount = gameState.currentBet - currentPlayer.currentBet
            currentPlayer.stackSize -= callAmount
            gameState.pot += callAmount
            currentPlayer.currentBet = gameState.currentBet  # Update player's total contribution
            currentPlayer.call(callAmount)
        elif move == "raise":
            if gameState.currentBet == 0:
                additionalContribution = amount
            else:
                # Calculate the additional contribution required for the raise
                additionalContribution = amount - currentPlayer.currentBet  # The difference between new bet and current contribution

            # Check if the raise is valid
            if additionalContribution <= 0:
                print(f"Error: Raise amount {amount} must be greater than the current bet {gameState.currentBet}.")
                continue

            # Deduct only the additional amount from the player's stack
            # currentPlayer.stackSize -= amount

            # Update the player's total bet for this round
            currentPlayer.currentBet = amount

            # Update the game state's current bet to reflect the new raise
            gameState.currentBet = amount

            # Update the pot with the additional contribution
            # gameState.pot += amount

            # Track last aggressive player
            lastAggressivePlayer = currentPlayerIndex
            betThisRound = True

            print(
                f"{currentPlayer.name} raises to {gameState.currentBet}. New stack: {currentPlayer.stackSize}, New pot: {gameState.pot}.")
        elif move == "all-in":
            allInAmount = currentPlayer.stackSize
            currentPlayer.allIn()
            gameState.pot += allInAmount
            lastAggressivePlayer = currentPlayerIndex
            betThisRound = True
            print(f"{currentPlayer.name} goes all-in with {allInAmount}.")
        else:
            print("Somehow a move wasn't selected in turn")

        # Reset firstRound after all players have acted once
        if firstRound and currentPlayerIndex == lastPlayerIndex:
            firstRound = False

        # Ending betting if currentPlayerIndex is the last player to bet
        if currentPlayerIndex == lastAggressivePlayer and not firstRound and not betThisRound:
            bettingContinues = False

        # Advancing to next player
        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
        betThisRound = False
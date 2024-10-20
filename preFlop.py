def runPreFlop(gameState):
    """Runs the pre-flop phase of the game, handling blinds and initial betting."""
    gameState.gameStage = "preflop"

    currentPlayerIndex = (gameState.dealerPosition + 3) % len(gameState.players)
    firstRound = True
    bettingContinues = True

    smallBlindIndex = (gameState.dealerPosition + 1) % len(gameState.players)
    bigBlindIndex = (gameState.dealerPosition + 2) % len(gameState.players)

    # Post blinds
    gameState.players[smallBlindIndex].bet(gameState.blinds[0])
    gameState.players[bigBlindIndex].bet(gameState.blinds[1])
    gameState.currentBet = gameState.blinds[1]

    print(f"Small blind of {gameState.blinds[0]} posted by {gameState.players[smallBlindIndex].name}")
    print(f"Big blind of {gameState.blinds[1]} posted by {gameState.players[bigBlindIndex].name}")

    lastAggressivePlayer = bigBlindIndex
    betThisRound = False

    # Ensure each player has two cards
    for player in gameState.players:
        if player.is_active:
            if len(player.cards) != 2:  # Correct reference to 'cards' instead of 'hand'
                player.cards = [gameState.deck.pop(), gameState.deck.pop()]  # Deal two cards

    while bettingContinues:
        currentPlayer = gameState.players[currentPlayerIndex]

        if not currentPlayer.is_active or currentPlayer.stackSize == 0:
            print(f"{currentPlayer.name} is not in hand or has 0 stack, skipping...")
            currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
            continue

        print(f"Current bet: {gameState.currentBet}, {currentPlayer.name}'s stack: {currentPlayer.stackSize}")

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
            print(f"Error: Invalid move '{move}' in pre-flop phase.")

        # Continue the betting until no new raises are made or players fold
        if firstRound and currentPlayerIndex == bigBlindIndex:
            firstRound = False

        if currentPlayerIndex == lastAggressivePlayer and not firstRound and not betThisRound:
            bettingContinues = False

        currentPlayerIndex = (currentPlayerIndex + 1) % len(gameState.players)
        betThisRound = False
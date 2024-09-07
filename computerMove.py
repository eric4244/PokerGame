def compMove(player, cards, communityCards, gameStage, stack, minBet):
    # Assuming 'cards' is a list of two Card objects
    if len(cards) < 2:
        print(f"Error: {player.name} does not have enough cards.")
        return 0, "fold"  # Safely fold if cards are insufficient

    card_ranks = [card.rank for card in cards]  # Correct way to extract ranks from Card objects
    print(f"{player.name} cards: {', '.join(str(card) for card in cards)}")

    tenth_of_stack = stack / 10
    amountToCall = max(minBet - player.currentBet, 0)  # Ensure amountToCall is never negative

    # Actions
    action = ""
    betSize = 0

    if gameStage == "preflop":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print(f"{player.name} has a pair pre-flop.")
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = amountToCall
                action = "call"
        else:
            print(f"{player.name} does not have a pair pre-flop.")
            # Handle non-pair cards
            if minBet == 0:
                action = "check"
                betSize = 0
            elif stack >= amountToCall > 0:
                betSize = amountToCall
                action = "call"
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "flop":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print(f"{player.name} has a pair on the flop.")
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = amountToCall
                action = "call"
        else:
            print(f"{player.name} does not have a pair on the flop.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet == 0:
                action = "check"
                betSize = 0
            elif stack >= amountToCall > 0:
                betSize = amountToCall
                action = "call"
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "turn":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print(f"{player.name} has a pair on the turn.")
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = amountToCall
                action = "call"
        else:
            print(f"{player.name} does not have a pair on the turn.")
            # Handle non-pair cards
            if minBet == 0:
                action = "check"
                betSize = 0
            elif stack >= amountToCall > 0:
                betSize = amountToCall
                action = "call"
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "river":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print(f"{player.name} has a pair on the river.")
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = amountToCall
                action = "call"
        else:
            print(f"{player.name} does not have a pair on the river.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet == 0:
                action = "check"
                betSize = 0
            elif stack >= amountToCall > 0:
                betSize = amountToCall
                action = "call"
            else:
                action = "fold"
                betSize = 0

    print(f"{player.name} action: {action}, Bet size: {betSize}")
    return betSize, action
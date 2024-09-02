def compMove(cards, communityCards, gameStage, stack, minBet):
    # Assuming 'cards' is a list of two Card objects
    if len(cards) < 2:
        print("Error: Computer player does not have enough cards.")
        return 0, "fold"  # Safely fold if cards are insufficient

    card_ranks = [card.rank for card in cards]  # Correct way to extract ranks from Card objects
    print(f"Computer player's cards: {cards}, Card ranks: {card_ranks}")

    # Actions
    action = ""
    betSize = 0

    if gameStage == "preflop":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print("Computer has a pair pre-flop.")
            tenth_of_stack = stack / 10
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = minBet
                action = "call"
        else:
            print("Computer does not have a pair pre-flop.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet <= tenth_of_stack:
                betSize = minBet
                action = "call"
            elif minBet == 0:
                action = "check"
                betSize = 0
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "flop":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print("Computer has a pair on the flop.")
            tenth_of_stack = stack / 10
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = minBet
                action = "call"
        else:
            print("Computer does not have a pair on the flop.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet <= tenth_of_stack:
                betSize = minBet
                action = "call"
            elif minBet == 0:
                action = "check"
                betSize = 0
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "turn":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print("Computer has a pair on the turn.")
            tenth_of_stack = stack / 10
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = minBet
                action = "call"
        else:
            print("Computer does not have a pair on the turn.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet <= tenth_of_stack:
                betSize = minBet
                action = "call"
            elif minBet == 0:
                action = "check"
                betSize = 0
            else:
                action = "fold"
                betSize = 0

    elif gameStage == "river":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
            print("Computer has a pair on the river.")
            tenth_of_stack = stack / 10
            if tenth_of_stack <= minBet:
                betSize = tenth_of_stack
                action = "raise"
            elif minBet >= stack:
                betSize = stack
                action = "all-in"
            else:
                betSize = minBet
                action = "call"
        else:
            print("Computer does not have a pair on the river.")
            # Handle non-pair cards
            tenth_of_stack = stack / 10
            if minBet <= tenth_of_stack:
                betSize = minBet
                action = "call"
            elif minBet == 0:
                action = "check"
                betSize = 0
            else:
                action = "fold"
                betSize = 0

    print(f"Computer action: {action}, Bet size: {betSize}")
    return betSize, action
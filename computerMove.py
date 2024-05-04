

def compMove(cards, communityCards, gameStage, stack, minBet):
    # Assuming 'cards' is a list of two card objects like ['5H', '5D'] (a pair of fives).
    card_ranks = [card[0:-1] for card in cards]  # Extract just the ranks from the card descriptions.

    # Actions
    action = ""
    betSize = 0

    if gameStage == "preflop":
        if card_ranks[0] == card_ranks[1]:  # Check if it's a pair.
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

    return betSize, action

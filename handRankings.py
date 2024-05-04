import itertools
from collections import Counter


# List of cards including your hand and community cards
def classifyHand(cards):
    ranks = [card.rank for card in cards]
    suits = [card.suit for card in cards]
    rankCounts = Counter(ranks)
    suitCounts = Counter(suits)

    isFlush = max(suitCounts.values()) >= 5
    isStraight = checkStraight(ranks)

    if isFlush and isStraight:
        return 'Royal Flush' if 'A' in ranks and 'T' in ranks else 'Straight Flush'
    elif max(rankCounts.values()) == 4:
        return 'Four of a Kind'
    elif sorted(rankCounts.values(), reverse=True)[:2] == [3, 2]:
        return 'Full House'
    elif isFlush:
        return 'Flush'
    elif isStraight:
        return 'Straight'
    elif 3 in rankCounts.values():
        return 'Three of a Kind'
    elif len([rank for rank, count in rankCounts.items() if count == 2]) == 2:
        return 'Two Pair'
    elif 2 in rankCounts.values():
        return 'One Pair'
    return 'High Card'


def checkStraight(ranks):
    ranksOrder = '23456789TJQKA'  # This defines the order as a string.
    rankSet = set(ranks)  # Ensure that ranks are passed as strings

    # Generate start indexes only for valid starting points of a straight
    startIndexes = {ranksOrder.index(rank) for rank in rankSet if rank in ranksOrder and ranksOrder.index(rank) <= 8}

    for start in startIndexes:
        # Check if five consecutive ranks exist in rankSet
        if all(ranksOrder[i] in rankSet for i in range(start, start + 5)):
            return True
    # Special case for a low Ace straight (A-2-3-4-5)
    if {'A', '2', '3', '4', '5'}.issubset(rankSet):
        return True
    return False


def hand_rank(handType):
    handRanks = {
        'Royal Flush': 1,
        'Straight Flush': 2,
        'Four of a Kind': 3,
        'Full House': 4,
        'Flush': 5,
        'Straight': 6,
        'Three of a Kind': 7,
        'Two Pair': 8,
        'One Pair': 9,
        'High Card': 10
    }
    return handRanks.get(handType, 11)


# function which takes all the cards, it then returns the best hand and the ranking of the hand
def evaluateBestHand(playerCards, communityCards):
    all_cards = playerCards + communityCards
    all_combinations = itertools.combinations(all_cards, 5)
    best_hand = max(all_combinations, key=lambda combo: hand_rank(classifyHand(list(combo))))
    return classifyHand(list(best_hand)), best_hand


RANK_VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, 'T': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

HAND_STRENGTH = {
        'Royal Flush': 100000,
        'Straight Flush': 900000,
        'Four of a Kind': 800000,
        'Full House': 700000,
        'Flush': 600000,
        'Straight': 500000,
        'Three of a Kind': 400000,
        'Two Pair': 300000,
        'One Pair': 200000,
        'High Card': 100000
    }


def calculateSecondaryScore(cards, handType, rankCounts):
    rankValues = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    ranks = [card.rank for card in cards]

    # Sorting ranks based on their value
    sorted_ranks = sorted(ranks, key=lambda rank: rankValues[rank], reverse=True)

    if handType in ['One Pair', 'Two Pair', 'Three of a Kind', 'Four of a Kind', 'Full House']:
        grouped_ranks = sorted(((count, rank) for rank, count in rankCounts.items() if count >= 2), reverse=True,
                               key=lambda x: (x[0], rankValues[x[1]]))
        pair_score = sum(rankValues[rank] * (100 ** (2 * count + idx)) for idx, (count, rank) in enumerate(grouped_ranks))
        kicker_score = sum(rankValues[rank] * (10 ** (5 - idx)) for idx, rank in enumerate(sorted_ranks) if rankCounts[rank] == 1)
        score = pair_score + kicker_score
    elif handType == 'Straight' or handType == 'Straight Flush':
        # Use the highest card in the straight for scoring
        score = sum(rankValues[rank] * (10 ** (5 - idx)) for idx, rank in enumerate(sorted_ranks))
    elif handType == 'Flush':
        score = sum(rankValues[rank] * (100 ** (5 - idx)) for idx, rank in enumerate(sorted_ranks))
    elif handType == 'High Card':
        score = sum(rankValues[rank] * (50 ** (5 - idx)) for idx, rank in enumerate(sorted_ranks))
    else:
        # General fallback for scoring
        score = sum(rankValues[rank] for rank in ranks)

    return score / 1000000000  # Normalize the score to prevent overflow


def calculateHandRank(cards):
    ranks = [card.rank for card in cards]
    suits = [card.suit for card in cards]
    rankCounts = Counter(ranks)
    suitCounts = Counter(suits)

    handType = classifyHand(cards)

    primaryRank = HAND_STRENGTH[handType]
    secondaryRank = calculateSecondaryScore(cards, handType, rankCounts)

    return primaryRank + secondaryRank

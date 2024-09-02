class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit[0]}"

    def to_shorthand(self):
        # Converts rank and suit to shorthand notation
        rank_to_char = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', 'T': 'T', 'J': 'J',
            'Q': 'Q', 'K': 'K', 'A': 'A'
        }
        suit_to_char = {
            'Hearts': 'H', 'Diamonds': 'D', 'Spades': 'S', 'Clubs': 'C'
        }
        return f"{rank_to_char[self.rank]}{suit_to_char[self.suit]}"


def createCardFromString(cardStr):
    suits = {'H': 'Hearts', 'D': 'Diamonds', 'S': 'Spades', 'C': 'Clubs'}
    ranks = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'T': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'}
    rank = cardStr[:-1]
    suit = cardStr[-1]
    if rank in ranks and suit in suits:
        return Card(ranks[rank], suits[suit])
    else:
        raise ValueError("Invalid card string")
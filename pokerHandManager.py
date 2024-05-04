class PokerHandManager:
    def __init__(self, players):
        self.players = players
        self.currentBet = 0

    # Checking that all players have matched bet or folded
    def isRoundOver(self):
        activeBets = [p.currentBet for p in self.players if p.inHand and not p.isBusted]
        if all(bet == self.currentBet for bet in activeBets) or all(not p.inHand for p in self.players):
            return True
        return False

    def processPlayerAction(self, player, action, amount=None):
        """Process player action and update bets accordingly."""
        if action == 'fold':
            player.fold()
        elif action == 'check':
            player.check()
        elif action == 'call':
            callAmount = self.currentBet - player.currentBet
            player.call(callAmount)
        elif action == 'raise':
            player.raiseBet(amount)
            self.currentBet = player.totalContribution
        elif action == 'all-in':
            player.allIn()

    def endRound(self):
        """Reset for a new round of betting."""
        for player in self.players:
            player.currentBet = 0

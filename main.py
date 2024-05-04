from gameState import GameState
from playerClass import Player


def initializePlayers(numPlayers, stackSize):
    players = {}
    # Set the first player as the human user
    players["User"] = Player("User", stackSize, isHuman=True)
    # Set remaining players as computer-controlled players
    for i in range(1, numPlayers):
        players[f"Player{i}"] = Player(f"Player{i}", stackSize, isHuman=False)
    return players


if __name__ == '__main__':
    try:
        playerNumber = int(input("Please enter the number of players in the game including yourself (2-10): "))
        if not 2 <= playerNumber <= 10:
            raise ValueError("Player number must be between 2 and 10.")

        chipStart = int(input("Please enter the number of starting chips (10 to 1,000,000): "))
        if not 10 <= chipStart <= 1000000:
            raise ValueError("Starting chips must be between 10 and 1,000,000.")
    except ValueError as e:
        print(e)
        exit()

    players = initializePlayers(playerNumber, chipStart)
    gameState = GameState(list(players.values()), chipStart)

    # Start the game loop
    while True:
        gameState.playHand()
        activePlayers = [p for p in gameState.players if not p.isBusted and p.stackSize > 0]

        if len(activePlayers) <= 1:
            print("Game over, winner is:", activePlayers[0].name if activePlayers else "No one")
            break

        if input("Continue playing? (yes/no): ").lower() != 'yes':
            print("Game ended.")
            break



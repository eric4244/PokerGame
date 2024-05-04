def userMove(currentBet, playerStack):
    print(f"Current bet to call: {currentBet}")
    print(f"Your stack: {playerStack}")
    print("Choose your action: ")
    print("1: Fold")
    print("2: Check/Call")
    print("3: Raise")
    print("4: All-in")

    while True:
        try:
            choice = int(input("Enter your choice (1-4): "))
            if choice not in range(1, 5):
                raise ValueError("Please select a valid option.")

            if choice == 1:
                return 0, "fold"
            elif choice == 2:
                # Check if the player needs to call a bet or can check
                if currentBet > 0:
                    betSize = min(playerStack, currentBet)
                    action = "call"
                else:
                    betSize = 0
                    action = "check"
                return betSize, action
            elif choice == 3:
                raiseAmount = int(input("Enter your raise amount: "))
                if raiseAmount > playerStack:
                    raise ValueError("Raise amount cannot be more than your stack.")
                if raiseAmount <= currentBet:
                    raise ValueError("Raise must be greater than the current bet.")
                return raiseAmount, "raise"
            elif choice == 4:
                return playerStack, "all-in"
        except ValueError as e:
            print(e)
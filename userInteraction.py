def userMove(currentBet, playerStack):
    print(f"Current bet to call: {currentBet}")
    print(f"Your stack: {playerStack}")

    # Display different options based on whether there's a bet on the table
    print("Choose your action: ")
    print("1: Fold")

    if currentBet == 0:
        print("2: Check")
    else:
        print("2: Call")

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
                if currentBet > 0:
                    # Player must call the current bet
                    betSize = min(playerStack, currentBet)
                    action = "call"
                else:
                    # Player can check if no bet to call
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

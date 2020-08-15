class ScheduleGenerator():
    def __init__(self):
        self.players = []
        self.target_matches = None
        self.n_trials = None

    def init_parameters(self):
        print("Let's generate some 2v2 match schedules!")

        while True:
            player = input("Please enter the name of a player. Enter -1 if you have finished adding all players ")

            if player == '-1' and len(self.players) >= 4:
                break
            elif player == '-1':
                print("You must have at least 4 players in your match schedule!")
            else:
                self.players.append(player)

        while True:
            try:
                self.target_matches = int(input("What is the least amount of matches each team should play? "))
                self.n_trials = int(input("How many candidate match schedules should be generated? "))
                break
            except ValueError:
                print("Make sure you enter an integer value")

        print("============================================================================")
        print(f"Successfully initialized generation parameters!"
              f"\nPlayers: {self.players}"
              f"\nTarget Matches: {self.target_matches} | Number of candidate schedules: {self.n_trials} ")
        print("============================================================================")

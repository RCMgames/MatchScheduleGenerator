import numpy as np
from utils import *
from random import randint


class ScheduleGenerator:
    def __init__(self):
        self.player_names = []
        self.target_matches = 0
        self.n_trials = 0

        self.players_dict = {}
        self.match_schedule_dict = {}

    def init_parameters(self):
        print("Let's generate some 2v2 match schedules!")

        while True:
            player = input("Please enter the name of a player. Enter -1 if you have finished adding all players ")

            if player == '-1' and len(self.player_names) >= 4:
                break
            elif player == '-1':
                print("You must have at least 4 players in your match schedule!")
            else:
                self.player_names.append(player)

        while True:
            try:
                self.target_matches = int(input("What is the least amount of matches each team should play? "))
                self.n_trials = int(input("How many candidate match schedules should be generated? "))
                break
            except ValueError:
                print("Make sure you enter an integer value")

        print("============================================================================")
        print(f"Successfully initialized generation parameters!"
              f"\nPlayers: {self.player_names}"
              f"\nTarget Matches: {self.target_matches} | Number of candidate schedules: {self.n_trials}")
        print("============================================================================")

    def find_optimal_schedule(self):
        pass

    def generate_schedule(self):
        max_num_matches = self.target_matches * len(self.player_names) * 4
        alliance_positions = ['B1', 'B2', 'R1', 'R2']
        match_pos = 0

        self.players_dict = {player_name: {'n_matches': 0, 'match_history': np.zeros(max_num_matches, dtype=np.int16),
                                           'color_history': []} for player_name in self.player_names}
        self.match_schedule_dict = {alliance_pos: [] for alliance_pos in alliance_positions}

        while get_num_matches_played(self.players_dict) < self.target_matches:
            candidates = select_player_candidates(players_dict=self.players_dict.copy())
            for alliance_pos in alliance_positions:
                print(f"Candidates: {candidates}")
                chosen_player = candidates[randint(0, len(candidates) - 1)]
                print(f"Chosen Player: {chosen_player}")
                self.match_schedule_dict[alliance_pos].append(chosen_player)
                self.players_dict[chosen_player]['n_matches'] += 1
                self.players_dict[chosen_player]['match_history'][match_pos] = 1
                self.players_dict[chosen_player]['color_history'] += alliance_pos[0]
                candidates.remove(chosen_player)
            match_pos += 1

        print(self.players_dict)
        print(self.match_schedule_dict)
        print(f"Number of matches in schedule: {match_pos}")

        return self.players_dict, self.match_schedule_dict

    def score_schedule(self):
        color_uniformity_scores = np.zeros(len(self.players_dict))
        match_distance_scores = np.zeros(len(self.players_dict))
        match_number_score = 0

        for (index, (player_name, record)) in enumerate(self.players_dict.items()):
            num_blue = record['color_history'].count('B')
            num_red = record['color_history'].count('R')
            color_uniformity_scores[index] = (num_blue - num_red) ** 2
            print(record)
            print(color_uniformity_scores)

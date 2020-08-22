import numpy as np
from utils import *
from random import randint


class ScheduleGenerator:
    def __init__(self, verbose=False):
        self.player_names = []
        self.target_matches = 0
        self.n_trials = 0

        self.players_dict = {}
        self.match_schedule_dict = {}

        self.verbose = verbose

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
        optimal_schedule = {}
        optimal_players_dict = {}
        # Randomly chosen large number
        lowest_score = 25 ** 4
        lowest_score_breakdown = {}

        for i in range(0, self.n_trials):
            self.generate_schedule()
            schedule_score, score_breakdown = self.score_schedule()

            if schedule_score < lowest_score:
                optimal_schedule = self.match_schedule_dict
                optimal_players_dict = self.players_dict
                lowest_score = schedule_score
                lowest_score_breakdown = score_breakdown

        print(f"Lowest Score: {lowest_score}")
        print(f"Optimal Schedule: {optimal_schedule}")
        print(f"Optimal Player Dict: {optimal_players_dict}")
        print(f"Score Breakdown: {lowest_score_breakdown}")

    def generate_schedule(self):
        max_num_matches = self.target_matches * len(self.player_names) * 100
        alliance_positions = ['B1', 'B2', 'R1', 'R2']
        match_pos = 0

        self.players_dict = {player_name: {'n_matches': 0, 'match_history': np.zeros(max_num_matches, dtype=np.int16),
                                           'color_history': []} for player_name in self.player_names}
        self.match_schedule_dict = {alliance_pos: [] for alliance_pos in alliance_positions}

        while get_num_matches_played(self.players_dict) < self.target_matches:
            candidates = select_player_candidates(players_dict=self.players_dict.copy())
            for alliance_pos in alliance_positions:
                chosen_player = candidates[randint(0, len(candidates) - 1)]

                if self.verbose:
                    print(f"Candidates: {candidates}")
                    print(f"Chosen Player: {chosen_player}")

                self.match_schedule_dict[alliance_pos].append(chosen_player)
                self.players_dict[chosen_player]['n_matches'] += 1
                self.players_dict[chosen_player]['match_history'][match_pos] = 1
                self.players_dict[chosen_player]['color_history'] += alliance_pos[0]
                candidates.remove(chosen_player)
            match_pos += 1

        self.players_dict = strip_match_history(self.players_dict, match_pos)

        if self.verbose:
            print(self.players_dict)
            print(self.match_schedule_dict)
            print(f"Number of matches in schedule: {match_pos}")

        return self.players_dict, self.match_schedule_dict

    def score_schedule(self):
        color_uniformity_scores = np.zeros(len(self.players_dict))
        match_distance_scores = np.zeros(len(self.players_dict))

        for (index, (player_name, record)) in enumerate(self.players_dict.items()):
            match_history = record['match_history']
            color_history = record['color_history']

            num_consecutives = 0
            for i in range(1, len(record['match_history'])):
                if match_history[i - 1] == match_history[i] and match_history[i - 1] * match_history[i] != 0:
                    num_consecutives += 1
            match_distance_scores[index] = num_consecutives ** 2

            num_blue = color_history.count('B')
            num_red = color_history.count('R')
            color_uniformity_scores[index] = (num_blue - num_red) ** 2

        match_number_score = (self.target_matches - record['n_matches']) ** 2

        if self.verbose:
            print(record)
            print(f"Match Distance Scores: {match_distance_scores}")
            print(f"Color Uniformity Scores: {color_uniformity_scores}")
            print(f"Match Number Score: {match_number_score}")

        return sum(match_distance_scores) + sum(color_uniformity_scores) + match_number_score, dict(
            m_d=match_distance_scores, c_u=color_uniformity_scores)

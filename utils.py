# Return the number of matches all teams have played. If teams haven't all played the same number of matches, return -1
def get_num_matches_played(players_dict):
    matches_played = [player['n_matches'] for player in players_dict.values()]
    # Check to see if all players have played the same number of matches
    uniform_match_number = matches_played.count(matches_played[0]) == len(matches_played)

    print(f"Number of matches played for each team: {matches_played}")
    if uniform_match_number:
        return matches_played[0]
    else:
        return -1

# Only players that have played the fewest number of matches are eligible to be put into the next match
def select_player_candidates(players_dict):
    candidate_player_names = []

    # There must be at least four players in a match
    while len(candidate_player_names) < 4:
        matches_played = [player['n_matches'] for player in players_dict.values()]
        min_matches = min(matches_played)
        print(f"Lowest number of matches played: {min_matches}")
        # Iterate off of a copy of player_dict so we can delete players that are already in the candidates list
        iterable_players_dict = players_dict.copy()
        for (player_name, record) in iterable_players_dict.items():
            if record['n_matches'] == min_matches:
                candidate_player_names.append(player_name)
                del players_dict[player_name]
    print(f"Candidate player names:{candidate_player_names}")
    return candidate_player_names

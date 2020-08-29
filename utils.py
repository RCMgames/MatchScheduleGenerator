from collections import OrderedDict

# Return the number of matches all teams have played. If teams haven't all played the same number of matches, return -1
def get_num_matches_played(players_dict):
    matches_played = [player['n_matches'] for player in players_dict.values()]
    # Check to see if all players have played the same number of matches
    uniform_match_number = matches_played.count(matches_played[0]) == len(matches_played)

    # print(f"Number of matches played for each team: {matches_played}")
    if uniform_match_number:
        return matches_played[0]
    else:
        return -1


# Only players that have played the fewest number of matches are eligible to be put into the next match
def select_player_candidates(players_dict):
    candidate_player_names = OrderedDict((rank, []) for rank in range(1, 4 + 1))
    candidate_rank = 1
    current_candidates = 0

    # There must be at least four players in a match
    while current_candidates < 4:
        matches_played = [player['n_matches'] for player in players_dict.values()]
        # print(f"Matches played: {matches_played}")
        min_matches = min(matches_played)
        # print(f"Lowest number of matches played: {min_matches}")
        # Iterate off of a copy of player_dict so we can delete players that are already in the candidates list
        iterable_players_dict = players_dict.copy()
        for (player_name, record) in iterable_players_dict.items():
            if record['n_matches'] == min_matches:
                candidate_player_names[candidate_rank].append(player_name)
                del players_dict[player_name]
        for rank_players in candidate_player_names.values():
            current_candidates += len(rank_players)
        candidate_rank += 1

    # print(candidate_player_names)
    return candidate_player_names


# Shortens the player's match history array to a length equal to the total number of matches in the schedule
def strip_match_history(players_dict, num_matches):
    for player_record in players_dict.values():
        player_record['match_history'] = player_record['match_history'][:num_matches]

    return players_dict

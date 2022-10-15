from helpers import get_money, get_formation, pos_max, get_preferences, best_raw_squad, calculate_chemistry, optimize, calculate_team_rating
import static_data

# The central program of this project. The goal is to take as input a user's budget, their preferred formation,
# and their attribute preferences for each position and output the best possible FIFA 23 Ultimate Team squad.

# Get the user's money and formation
money = get_money()
formation = get_formation()

# Get the unique positions in the squad, the user's preferences, and the maximum spend in each position
positions = static_data.formations[formation]
unique_positions = set(positions)
preferences = get_preferences(positions)
maxes = pos_max(money, unique_positions)

# Calculate the best possible squad without taking chemistry into account, and then calculate each player's chemistry and new rating, taking into account said chemistry
raw_squad = best_raw_squad(positions, static_data.database, maxes, preferences)
raw_players = raw_squad[0]
clubs_nations_leagues = raw_squad[1]
squad_with_chemistry = calculate_chemistry(raw_players, clubs_nations_leagues, preferences)
print(f'Your initial squad is rated {calculate_team_rating(squad_with_chemistry)} by your criteria before optimizing for chemistry. It has the following players:')
for player in squad_with_chemistry:
    print(f'{player} at {squad_with_chemistry[player]["position"]}')
print()

# Optimize the squad and print the results in order of position
final_squad = optimize(squad_with_chemistry, clubs_nations_leagues, preferences, maxes, static_data.database)
print(f'Your final squad is rated {calculate_team_rating(final_squad)} by your criteria after optimizing for chemistry. It has the following players:')
printed = {}
for player in final_squad:
    printed[player] = False

for pos in positions:
    for player in final_squad:
        if final_squad[player]["position"] == pos and printed[player] == False:
            print(f'{player} at {final_squad[player]["position"]}')
            printed[player] = True
print()
print('Note that the final squad should be rated higher based on the criteria you gave earlier due to the chemistry boosts, which are factored into calculations.')
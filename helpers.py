import static_data
import sqlite3
from copy import deepcopy

# Function to get the user's budget. Make sure budget is enough for cheapest possible squad based on the average price of a player in each position. This value can be changed if the program is adjusted for not just gold players.
def get_money():
    while True:
        try:
            money = int(input('How many FIFA coins do you have? '))
            if money >= static_data.minimum_budget:
                return money
            else:
                print('You don\'t have enough money for a full gold squad! Try again.')
        except:
            print('That\'s not a number. Try again.')


# Function to get the user's desired formation:
def get_formation():
    while True:
        formation = input('What formation do you want your team to have? ')
        if formation in static_data.formations:
            print()
            return formation
        else:
            print('That\'s not a formation. Your options:')
            print('\n'.join(static_data.formations))


# Function that assigns a weight to each stat for each position if the user chooses to do so
def get_preferences(positions):
    print('In the process of calculating the best possible team, we need to calculate player ratings from the 6 attributes in FIFA 23 Ultimate Team. Here is how the creator of this program decided to weight each attribute for each position:')
    print()
    preferences = {}
    asked = {}

    # We want to ask for the preferences of each position, but we don't want to repeat ourselves. However, we still want to do it in order.
    # So initialize a dictionary where each key is the position and the value is a boolean representing whether it's been asked already
    for pos in positions:
        asked[pos] = False

    # Iterate over each position and print the weight of each attribute in that position.
    # Then ask the user if they like the attributes for that position
    for pos in positions:
        # If we've already asked, skip this iteration
        if asked[pos] == True:
            continue

        # If not, set the asked value equal to true for this position
        asked[pos] = True

        # Print the default weight of each attribute by getting it from the default_preferences dictionary
        for att in static_data.attributes[pos]:
            print(f'{att.upper()} has a weight {static_data.default_preferences[pos][att]} for {pos}.')

        # Take the user's input
        change = input('Do you want to change the weight of any attribute in this position? Type \'y\' if yes or hit enter for no. ')
        print()

        # If yes, get the user's new preferences, and ensure they are all numerical and total to 100
        if change == 'y':
            print('For each attribute, input the importance as a number from 0 to 100. The weight of all the attributes must sum to 100.')
            print()
            preferences[pos] = {}
            while True:
                i = static_data.n_attributes - 1
                current = 0
                for att in static_data.attributes[pos]:
                    accepted = False
                    while accepted == False:
                        try:
                            preferences[pos][att] = (int(input(f'Importance of {att} for {pos}: ')))

                            # Keep track of how much of the allocation the player has used and print it, as well as how many more attributes there are
                            current += preferences[pos][att]
                            print(f'Current total: {current}\nPoints left: {100 - current}\n{i} more attributes')
                            print()
                            i -= 1
                            accepted = True
                        except:
                            print('That\'s not a number. Try again!')
                if current != 100:
                    print('The sum of the weights is not 100. Try again!')
                else:
                    break

        # If the player changed nothing, then just return the default_preferences dictionary
        else:
            preferences[pos] = static_data.default_preferences[pos]
    return preferences

# Function to determine the proportion of the budget each position should get
def pos_max(budget, positions):
    total = 0
    maxes = {}

    # Iterate over each position and add only the positions present in the formation to the total
    for pos in positions:
        total += static_data.average_prices[pos]

    # Fill the dictionary proportions with the proportion of the cost
    for pos in positions:
        maxes[pos] = int(budget * (static_data.average_prices[pos] / total))

    return maxes

# A function that calculates a player's rating based on the user's preferences and chemistry
def calculate_rating(player, position, position_preferences):
    # Initialize the rating and the attribute values which will be used to calculate the rating
    rating = 0
    attribute_values = {}
    
    if position != 'GK':
        # Calculate the average of the sub attributes that make up a given attribute
        for attribute in static_data.attributes[position]:
            total = 0

            # Iterate over every sub attribute and add its value to the total only if it's in the list of sub attributes for a given attribute
            for sub_attribute in static_data.sub_attributes_internal[attribute]:
                # Take into account the chemistry as well. Formula derived from data from EA Sports.
                if player['chemistry'] != 0:
                    player[sub_attribute] += (static_data.chem_stats[sub_attribute] * (2**(player['chemistry'] - 1)))
                    if player[sub_attribute] > static_data.max_rating:
                        player[sub_attribute] = static_data.max_rating
                    total += player[sub_attribute]
                else:
                    total += player[sub_attribute]

            # After getting the total of the sub attributes within an attribute, divide it by the number of sub attributes to get the attribute's value.
            # Then calculate the rating based on the user's preferences and return it rounded to the nearest integer.
            attribute_values[attribute] = round(total / len(static_data.sub_attributes_internal[attribute]))
            rating += round((position_preferences[attribute]/100) * attribute_values[attribute])
    else:
        for attribute in static_data.attributes[position]:
            if player['chemistry'] != 0:
                player[attribute] += (static_data.chem_stats[attribute] * (2**(player['chemistry'] - 1)))
                if player[attribute] > static_data.max_rating:
                    player[attribute] = static_data.max_rating
            rating += round((position_preferences[attribute]/100) * player[attribute])

    player['rating'] = rating
    return player

# A function that gets the best raw squad (not taking chemistry into account)
def best_raw_squad(positions, db, maxes, preferences):
    # First, establish database connection and initialize the raw squad and clubs_leagues_nations counts we will return
    con = sqlite3.connect(db)
    cur = con.cursor()
    raw_squad = {}
    clubs_leagues_nations = {'club': {}, 'league': {}, 'nation': {}}

    # Iterate over every position and find the best player in that position
    for pos in positions:

        if pos != 'GK':
            # In order to pass in all the sub attributes into a SQL query, we need to make them a list. Store the length for later use
            sub_attributes_list = []
            for attribute in static_data.attributes[pos]:
                for sub_attribute in static_data.sub_attributes_internal[attribute]:
                        sub_attributes_list.append(sub_attribute)
            n_sub_attributes = len(sub_attributes_list)
        else:
            sub_attributes_list = []
            for attribute in static_data.attributes[pos]:
                sub_attributes_list.append(attribute)
            n_sub_attributes = len(sub_attributes_list)

        # Query database for all players in the budget for this position and initialize a dictionary to store the best player
        in_budget = cur.execute(f'SELECT name, club, league, nation, {", ".join(sub_attributes_list)} FROM {pos.lower()} WHERE price <= {maxes[pos]}')
        best = {'name': '', 'position': pos, 'club': 0,
                'league': 0, 'nation': 0, 'rating': 0, 'chemistry': 0}

        # Iterate over every player and set the current player's information to a dictionary called current.
        for player in in_budget:
            current = {'name': player[0], 'position': pos, 'club': player[1],
                       'league': player[2], 'nation': player[3], 'chemistry': 0}

            # Ensure the player isn't in the squad already, then get the player's attributes and calculate his rating, setting him as the best player if his rating is better than the current best
            if current['name'] not in raw_squad:
                sub_att_values = {}
                for i in range(n_sub_attributes):
                    sub_att_values[sub_attributes_list[i]] = player[i + 4]
                for sub_att in sub_att_values:
                    current[sub_att] = sub_att_values[sub_att]
                
                current = calculate_rating(current, pos, preferences[pos])
                if current['rating'] > best['rating']:
                    best = current

        # Now that we have the best player in each position, add his club/nation/league to the dictionary and keep count
        for key in clubs_leagues_nations:
            if best[key] in clubs_leagues_nations[key]:
                clubs_leagues_nations[key][best[key]] += 1
            else:
                clubs_leagues_nations[key][best[key]] = 1

        # Finally, add the player and his info to the raw squad
        raw_squad[best['name']] = {}
        for key in best:
            if key != 'name':
                raw_squad[best['name']][key] = best[key]

    # Commit database changes and close the connection
    con.commit()
    cur.close()
    con.close()

    # Return a list, element 0 is the raw squad and element 1 is the dictionary containing the counts of the clubs/leagues/nations
    return [raw_squad, clubs_leagues_nations]

# A function that calculates each player's chemistry in the squad and returns an updated dictionary of players with the chemistry included
def calculate_chemistry(players, clubs_nations_leagues, preferences):
    for player in players:
        # Initialize a dictionary to store the chemistry in each category
        chemistries = {'club': 0, 'league': 0, 'nation': 0}

        # Iterate over each type of chemistry and, if the number of players that play for a given
        # club, league, or nation is more than the threshold for that chem type, update the chemistry in that category
        for chem_type in chemistries:
            for n_players in static_data.chem_levels[chem_type]:
                player_club_nation_league = players[player][chem_type]
                if clubs_nations_leagues[chem_type][player_club_nation_league] >= n_players:
                    chemistries[chem_type] = static_data.chem_levels[chem_type][n_players]

        # Sum the total chemistry for the player, but ensure it's no greater than 3
        total_chem = sum(chemistries.values())
        if total_chem > 3:
            total_chem = 3

        # Update our dictionary of players with all their chemistry values
        players[player]['chemistry'] = total_chem

        # In order to get players' new ratings, call calculate_rating function again
        players[player] = calculate_rating(players[player], players[player]['position'], preferences[players[player]['position']])
    return players

# A function that recursively optimizes the squad to generate the best possible team
def optimize(old_team, clubs_nations_leagues, preferences, maxes, db, done = []):
    # Find the lowest rated player on the team and start with him
    lowest_rating = static_data.max_rating
    worst = None
    for player in old_team:
        if old_team[player]['rating'] < lowest_rating and old_team[player]['chemistry'] != 3 and player not in done:
            worst = player
            lowest_rating = old_team[worst]['rating']
    
    if worst == None:
        return old_team
    
    # Assign the worst player's position to "position"
    position = old_team[worst]['position']

    # Also get lists of all the clubs, leagues, and nations present in the squad for easier use in querying database
    new_clubs_nations_leagues = deepcopy(clubs_nations_leagues)
    
    # Take out the counts pertaining to the worst player's club/nation/league
    for key in clubs_nations_leagues:
        new_clubs_nations_leagues[key][old_team[worst][key]] -= 1
        if new_clubs_nations_leagues[key][old_team[worst][key]] == 0:
            del new_clubs_nations_leagues[key][old_team[worst][key]]
    
    # Store all the clubs, nations, and leaegues as tuples
    clubs = tuple(new_clubs_nations_leagues['club'].keys())
    leagues = tuple(new_clubs_nations_leagues['league'].keys())
    nations = tuple(new_clubs_nations_leagues['nation'].keys())

    # Establish a database connection and cursor
    con = sqlite3.connect(db)
    cur = con.cursor()

    # Query the database for players in his position, but do not select any players that have the same combination of club, league, and nation
    # since we already found the best player with that combination. Also, do not select any players that don't have at least a club, league, or nation
    # in common with the rest of the squad, since that will be useless as well

    # In order to pass in all the sub attributes into a SQL query, we need to make them a list. Store the length for later use
    if position != 'GK':
        sub_attributes_list = []
        for attribute in static_data.attributes[position]:
            for sub_attribute in static_data.sub_attributes_internal[attribute]:
                    sub_attributes_list.append(sub_attribute)
        n_sub_attributes = len(sub_attributes_list)
    
    # Goalkeepers do not need this treatment because they only have their 6 face attributes
    else:
        sub_attributes_list = []
        for attribute in static_data.attributes[position]:
            sub_attributes_list.append(attribute)
        n_sub_attributes = len(sub_attributes_list)

    # Query database for all in-budget players who have at least a club, league, or nation in common with others in the squad. If not, then they will obviously be useless for optimizing the team's rating with chemistry
    options = cur.execute(f"SELECT name, club, league, nation, {', '.join(sub_attributes_list)} FROM {position.lower()} WHERE price <= {maxes[position]} AND (club IN {clubs} OR league IN {leagues} OR nation IN {nations})")
    for option in options:
        highest_rating = calculate_team_rating(old_team)
        best_team = old_team
        # Fill the player's information into a 'current' dictionary to keep track 
        current = {'name': option[0], 'position': position, 'club': option[1],
                       'league': option[2], 'nation': option[3], 'chemistry': 0}
        sub_attributes = {}
        for i in range(n_sub_attributes):
            sub_attributes[sub_attributes_list[i]] = option[i + 4]
        for sub_attribute in sub_attributes:
            current[sub_attribute] = sub_attributes[sub_attribute]
        
        # Create a copy of the squad, add the new player into the team, removing the worst player and updating the clubs_leagues_nations dictionary
        new_team = deepcopy(old_team)
        del new_team[worst]
        
        new_team[current['name']] = {}
        for key in current:
            if key != 'name':
                new_team[current['name']][key] = current[key]

        for key in clubs_nations_leagues:
            if current[key] in new_clubs_nations_leagues[key]:
                new_clubs_nations_leagues[key][current[key]] += 1
            else:
                new_clubs_nations_leagues[key][current[key]] = 1
        
        # Test if the new team is better than the old team. If so, pass that onto the next iteration of optimize. If not, then keep track of the fact that we tried
        # to find a better replacement for "worst", but we couldn't. Then, try optimizing the team again, but this time, since "worst" is in "done", we will move onto the next worst player.
        new_team = calculate_chemistry(new_team, new_clubs_nations_leagues, preferences)
        new_rating = calculate_team_rating(new_team)
        if new_rating > highest_rating:
            highest_rating = new_rating
            best_team = new_team
    
    done.append(worst)
    if best_team == old_team:
        next_squad = optimize(old_team, clubs_nations_leagues, preferences, maxes, db, done)
    else:
        next_squad = optimize(best_team, new_clubs_nations_leagues, preferences, maxes, db, done)
    
    con.commit()
    cur.close()
    con.close()
    
    # Finally, we will have exhausted all possibilities, meaning we can return the squad
    return next_squad

# A function that takes the average of all the players on the team
def calculate_team_rating(team):
    total = 0
    for player in team:
        total += team[player]['rating']
    team_rating = round(total / 11)
    return team_rating
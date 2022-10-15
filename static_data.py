database = 'dummy.db'

minimum_budget = 10000

API_key = ''

# A list of the available formations in FIFA 23. Source: EA Sports
formations = {'3-1-4-2': ['GK', 'CB', 'CB', 'CB' 'LM', 'RM', 'CM', 'CDM', 'CM', 'ST', 'ST'],
              '3-4-1-2': ['GK', 'CB', 'CB', 'CB' 'LM', 'RM', 'CM', 'CAM', 'CM', 'ST', 'ST'],
              '3-4-2-1': ['GK', 'CB', 'CB', 'CB' 'LM', 'RM', 'CM', 'CM', 'CF', 'CF', 'ST'],
              '3-5-2': ['GK', 'CB', 'CB', 'CB' 'LM', 'RM', 'CDM', 'CDM', 'CAM', 'ST', 'ST'],
              '3-4-3': ['GK', 'CB', 'CB', 'CB', 'LM', 'CM', 'CM', 'RM', 'LW', 'ST', 'RW'],
              '4-1-2-1-2': ['GK', 'LB', 'CB', 'CB', 'RB' 'LM', 'RM', 'CDM', 'CAM', 'ST', 'ST'],
              '4-1-2-1-2 (2)': ['GK', 'LB', 'CB', 'CB', 'RB' 'CM', 'CM', 'CDM', 'CAM', 'ST', 'ST'],
              '4-1-4-1': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CDM', 'CM', 'RM', 'ST'],
              '4-2-3-1': ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CDM', 'CAM', 'CAM', 'CAM', 'ST'],
              '4-2-3-1 (2)': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CDM', 'CDM', 'RM', 'CAM', 'ST'],
              '4-2-2-2': ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CDM', 'CAM', 'CAM', 'ST', 'ST'],
              '4-2-4': ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'LW', 'ST', 'ST', 'RW'],
              '4-3-1-2': ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'CAM', 'ST', 'ST'],
              '4-1-3-2': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CDM', 'RM', 'CM', 'ST', 'ST'],
              '4-3-2-1': ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'CF', 'CF', 'ST'],
              '4-3-3': ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CM', 'LW', 'ST', 'RW'],
              '4-3-3 (2)': ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CM', 'CM', 'LW', 'ST', 'RW'],
              '4-3-3 (3)': ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CDM', 'CM', 'LW', 'ST', 'RW'],
              '4-3-3 (4)': ['GK', 'LB', 'CB', 'CB', 'RB', 'CM', 'CM', 'CAM', 'LW', 'ST', 'RW'],
              '4-3-3 (5)': ['GK', 'LB', 'CB', 'CB', 'RB', 'CDM', 'CM', 'CM', 'LW', 'CF', 'RW'],
              '4-4-1-1': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'CF', 'ST'],
              '4-4-1-1 (2)': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'CAM', 'ST'],
              '4-4-2': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'RM', 'ST', 'ST'],
              '4-4-2 (2)': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CDM', 'CDM', 'RM', 'ST', 'ST'],
              '4-5-1': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'RM', 'CAM', 'CAM', 'ST'],
              '4-5-1 (2)': ['GK', 'LB', 'CB', 'CB', 'RB', 'LM', 'CM', 'CM', 'CM', 'RM', 'ST'],
              '5-2-1-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'CM', 'CM', 'CAM', 'ST', 'ST'],
              '5-2-2-1': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'CM', 'CM', 'LW', 'ST', 'RW'],
              '5-1-2-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'CDM', 'CM', 'CM', 'ST', 'ST'],
              '5-4-1': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB', 'LM', 'CM', 'CM', 'RM', 'ST']}

# A list containing every position in the game. Source: EA Sports
all_positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB', 'LM',
                 'CDM', 'CM', 'CAM', 'RM', 'CF', 'LW', 'ST', 'RW']

# The average cost of each position. Calculated from SQL database queries. Source: futdb.com
average_prices = {'GK': 8034, 'LWB': 12035, 'LB': 12035, 'CB': 10062, 'RB': 6486, 'RWB': 6486, 'LM': 20440,
                  'CDM': 7490, 'CM': 7810, 'CAM': 3228, 'RM': 16189, 'CF': 25384, 'LW': 20440, 'ST': 25384, 'RW': 16189}

# A dictionary that shows which stats are affected by a player having chemistry (with basic style). Source: EA Sports
chem_stats = {'acceleration': 0, 'sprintSpeed': 1, 'positioning': 1, 'finishing': 0, 'shotPower': 1, 'longShots': 0, 'volleys': 1, 'penalties': 1, 'vision': 1,
              'crossing': 0, 'freeKickAccuracy': 0, 'shortPassing': 1, 'longPassing': 1, 'curve': 1, 'agility': 1,
              'balance': 0, 'reactions': 0, 'ballControl': 1, 'dribbling_sub': 1, 'composure': 0,
              'interceptions': 0, 'headingAccuracy': 0, 'defenseAwareness': 1, 'standingTackle': 1,
              'slidingTackle': 4, 'jumping': 1, 'stamina': 0, 'strength': 1, 'aggression': 0,
              'diving': 1, 'handling': 1, 'kicking': 1, 'reflexes': 1, 'speed': 1, 'positioning': 1}

# A dictionary that stores the number of players needed to reach a certain chemistry level for clubs, leagues, and nations.
# The key in each of these dictionaries is the number of players, and the value is the chemistry level a player reaches by hitting that.
# Source: EA Sports
chem_levels = {'club': {2: 1, 4: 2, 7: 3},
               'league': {3: 1, 5: 2, 8: 3},
               'nation': {2: 1, 5: 2, 8: 3}}

# A dictionary of dictionaries storing the default attribute weights, as decided by the creator of this program
default_preferences = {'GK': {'diving': 18, 'handling': 18, 'kicking': 10, 'positioning': 18, 'reflexes': 18},
                       'LWB': {'pace': 25, 'shooting': 5, 'passing': 15, 'dribbling': 15, 'defending': 25, 'physicality': 15},
                       'LB': {'pace': 20, 'shooting': 0, 'passing': 20, 'dribbling': 20, 'defending': 30, 'physicality': 10},
                       'CB': {'pace': 10, 'shooting': 0, 'passing': 15, 'dribbling': 5, 'defending': 40, 'physicality': 30},
                       'RB': {'pace': 20, 'shooting': 0, 'passing': 20, 'dribbling': 20, 'defending': 30, 'physicality': 10},
                       'RWB': {'pace': 25, 'shooting': 5, 'passing': 15, 'dribbling': 15, 'defending': 25, 'physicality': 15},
                       'LM': {'pace': 25, 'shooting': 20, 'passing': 20, 'dribbling': 15, 'defending': 5, 'physicality': 15},
                       'CDM': {'pace': 10, 'shooting': 15, 'passing': 20, 'dribbling': 15, 'defending': 20, 'physicality': 20},
                       'CM': {'pace': 10, 'shooting': 20, 'passing': 30, 'dribbling': 15, 'defending': 10, 'physicality': 15},
                       'CAM': {'pace': 10, 'shooting': 25, 'passing': 30, 'dribbling': 20, 'defending': 5, 'physicality': 10},
                       'RM': {'pace': 25, 'shooting': 20, 'passing': 20, 'dribbling': 15, 'defending': 5, 'physicality': 15},
                       'CF': {'pace': 10, 'shooting': 40, 'passing': 20, 'dribbling': 20, 'defending': 0, 'physicality': 10},
                       'LW': {'pace': 25, 'shooting': 25, 'passing': 15, 'dribbling': 20, 'defending': 0, 'physicality': 15},
                       'ST': {'pace': 20, 'shooting': 35, 'passing': 10, 'dribbling': 20, 'defending': 0, 'physicality': 15},
                       'RW': {'pace': 25, 'shooting': 25, 'passing': 15, 'dribbling': 20, 'defending': 0, 'physicality': 15}}

# The 6 face attributes a player has. Source: EA Sports
attributes = {'GK': ["diving", "handling", "kicking", "positioning", "reflexes"],
              'LWB': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'LB': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'CB': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'RB': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'RWB': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'LM': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'CDM': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'CM': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'CAM': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'RM': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'CF': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'LW': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'],
              'ST': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality'], 'RW': ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality']}

# The sub-attributes used to calculate each of the face attributes. These are modified to match the format and language of FUTdb to allow for easy data retrieval from API
sub_attributes = {"paceAttributes": ["acceleration", "sprintSpeed"],
                  "shootingAttributes": ["positioning", "finishing", "shotPower", "longShots", "volleys", "penalties"],
                  "passingAttributes": ["vision", "crossing", "freeKickAccuracy", "shortPassing", "longPassing", "curve"],
                  "dribblingAttributes": ["agility", "balance", "reactions", "ballControl", "dribbling", "composure"],
                  "defendingAttributes": ["interceptions", "headingAccuracy", "standingTackle", "slidingTackle", "defenseAwareness"],
                  "physicalityAttributes": ["jumping", "stamina", "strength", "aggression"],
                  "goalkeeperAttributes": ["diving", "handling", "kicking", "positioning", "reflexes"]}

# The sub-attributes used to calculate each of the face attributes. These are modified to match the format and language of FUTdb to allow for easy data retrieval from API
sub_attributes_internal = {"pace": ["acceleration", "sprintSpeed"],
                           "shooting": ["positioning", "finishing", "shotPower", "longShots", "volleys", "penalties"],
                           "passing": ["vision", "crossing", "freeKickAccuracy", "shortPassing", "longPassing", "curve"],
                           "dribbling": ["agility", "balance", "reactions", "ballControl", "dribbling_sub", "composure"],
                           "defending": ["interceptions", "headingAccuracy", "standingTackle", "slidingTackle", "defenseAwareness"],
                           "physicality": ["jumping", "stamina", "strength", "aggression"],
                           "goalkeeper": ["diving", "handling", "kicking", "positioning", "reflexes"]}

# The maximum value any attribute or rating might be. Source: EA Sports
max_rating = 99

# The number of face attributes for any given position. Source: EA Sports
n_attributes = 6

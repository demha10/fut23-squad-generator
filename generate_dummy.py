# This program generates a dummy database to use for testing if you do not have an API-key

import sqlite3
import statistics
import static_data
import random

# A program to quickly set up a database with a table for each position and the necessary information. Just to be run once
con = sqlite3.connect('dummy.db')
cur = con.cursor()

names = ['Johm', 'Jane', 'Frank', 'Margaret', 'Adam', 'Eve', 'Juan', 'Juanita', 'Carlos', 'Carlita', 'Jose', 'Roberta', 'Ahmed', 'Nada', 'Raid', 'Fatima', 'Ali', 'Najlaa', 'Said', 'Smith', 'Johnson', 'Delgado', 'Shaarbaf', 'Abdul']

# Create a dictionary of leagues, where the keys are lists of clubs in the league
leagues = {}
for i in range(10):
    leagues[i] = []
    for j in range((i*20), (i*20) + 20):
        leagues[i].append(j)

# 50 nations to choose from
nations = list(range(50))

for pos in static_data.all_positions:
    cur.execute(f'CREATE TABLE {pos.lower()} (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, club INTEGER, league INTEGER, nation INTEGER)')
    for attribute in static_data.attributes[pos]:
        cur.execute(f'ALTER TABLE {pos.lower()} ADD {attribute.lower()} INTEGER')
        if pos != 'GK':
            for sub_attribute in static_data.sub_attributes[f'{attribute}Attributes']:
                if sub_attribute != attribute:
                    cur.execute(f'ALTER TABLE {pos.lower()} ADD {sub_attribute} INTEGER')
                else:
                    cur.execute(f'ALTER TABLE {pos.lower()} ADD {sub_attribute}_sub INTEGER')
    
    # Assign 200 players per position for a distrbution of roughly 11 players per club
    for i in range(200):
        name = f'{random.choice(names)} {random.choice(names)} {random.choice(names)}'
        id = i
        league = random.choice(list(leagues.keys()))
        club = random.choice(leagues[league])
        nation = random.choice(nations)
        player_sub_attribute_values = {}
        player_attribute_values = {}

        if pos != 'GK':
            # Iterate over each attribute and and get the value of the attribute for the given player from the data returned by the API
            for attribute in static_data.attributes[pos]:  
                relevant_sub_attributes = []
                # Each attribute also has several sub-attributes. Iterate over every sub-attribute within the attribute and get the data as well
                for sub_attribute in static_data.sub_attributes[f'{attribute}Attributes']:
                    # There is a special case where the 'dribbling' attribute actually has a 'dribbling' sub-attribute, which wil not allow for proper database entry
                    if sub_attribute != attribute:
                        # Some of the sub-attributes for some players are simply not filled in, so make sure this edge case is taken care of
                        player_sub_attribute_values[sub_attribute] = random.choice(list(range(100)))
                        relevant_sub_attributes.append(player_sub_attribute_values[sub_attribute])
                    
                    # This is the case for 'dribbling'. Here, append the suffic '_sub' to 'dribbling' to make it have a separate name for the SQL table 
                    else:
                        player_sub_attribute_values[f'{sub_attribute}_sub'] = random.choice(list(range(100)))
                        relevant_sub_attributes.append(player_sub_attribute_values[f'{sub_attribute}_sub'])
                
                player_attribute_values[attribute] = int(statistics.mean(relevant_sub_attributes))
        
        # If the player is in fact a goalkeeper, then we just need to worry about the 6 face attributes
        else:
            for attribute in static_data.attributes[pos]:
                player_attribute_values[attribute] = random.choice(list(range(100)))
        
        rating = round(statistics.mean(player_attribute_values.values()))
        price = rating * 1000
        
        # Now that we have the player's ID, name, club, league, nation, and price, insert it into his position's table and print his information as a confirmation
        data_for_table = (id, name, club, league, nation, price)
        cur.execute(f'INSERT INTO {pos} (id, name, club, league, nation, price) VALUES (?, ?, ?, ?, ?, ?)', data_for_table)
        
        # We also need to insert the player's attribute values
        for attribute in static_data.attributes[pos]:
            cur.execute(f'UPDATE {pos} SET ({attribute}) = {player_attribute_values[attribute]} WHERE id = {id}')
            
            # Insert the player's sub-attribte values if he is not a goalkeeper
            if pos != 'GK':
                for sub_attribute in static_data.sub_attributes[f'{attribute}Attributes']:
                    if sub_attribute != attribute:
                        cur.execute(f'UPDATE {pos} SET ({sub_attribute}) = {player_sub_attribute_values[sub_attribute]} WHERE id = {id}')
                    else:
                        cur.execute(f'UPDATE {pos} SET ({sub_attribute}_sub) = {player_sub_attribute_values[f"{sub_attribute}_sub"]} WHERE id = {id}')

con.commit()
cur.close()
con.close()
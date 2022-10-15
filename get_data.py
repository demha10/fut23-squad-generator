import requests
import sqlite3
import static_data

# This program utilizes the FUTdb API to get all the data of interest in this project. It then takes this data and inserts it into pre-generated SQL tables.

# Prerequiste data before getting data from API and saving to database. This prerequisite data can be changed to get different categories of players.
# Right now, the program is limited to rare gold players for simplicity, but the data retrieval can be expanded to get all the players along with their
# rarities so that the ideal squad can be built from more options. See futdb.app for more information about how to use the API.
API_KEY = static_data.API_key
url = 'https://futdb.app/api/players'
header = {'X-AUTH-TOKEN': API_KEY}
first_page = 3
n_pages = 114
platform = 'playstation'
non_standard_clubs = [112658, 114605]
desired_level = 'gold'
desired_rarity = 1

# Open a connection to the databse we will be filling
con = sqlite3.connect('players.db')
cur = con.cursor()

# Iterate over every page number and make a request to the API
for i in range(first_page, n_pages):
    payload_1 = {'page' : str(i)}
    r_1 = requests.get(url, headers=header, params=payload_1)
    player_data = r_1.json()

    # Iterate over every player in the request (which should be 20) and get all his information
    for player in player_data['items']:
        club = player['club']
        color = player['color']
        rarity = player['rarity']
        if club in non_standard_clubs or color != desired_level or rarity != desired_rarity:
            continue
        id = player['id']
        name = player['name']
        position = player['position']
        league = player['league']
        nation = player['nation']
        player_attribute_values = {}
        player_sub_attribute_values = {}
        
        # Goalkeepers and outfield players require different handling since goalkeepers have no sub-attributes
        if position != 'GK':
            # Iterate over each attribute and and get the value of the attribute for the given player from the data returned by the API
            for attribute in static_data.attributes[position]:
                player_attribute_values[attribute] = player[attribute]
                
                # Each attribute also has several sub-attributes. Iterate over every sub-attribute within the attribute and get the data as well
                for sub_attribute in static_data.sub_attributes[f'{attribute}Attributes']:
                    # There is a special case where the 'dribbling' attribute actually has a 'dribbling' sub-attribute, which wil not allow for proper database entry
                    if sub_attribute != attribute:
                        
                        # Some of the sub-attributes for some players are simply not filled in, so make sure this edge case is taken care of
                        if player[f'{attribute}Attributes'][sub_attribute] != None:
                            player_sub_attribute_values[sub_attribute] = player[f'{attribute}Attributes'][sub_attribute]
                        else:
                            player_sub_attribute_values[sub_attribute] = player_attribute_values[attribute]
                    
                    # This is the case for 'dribbling'. Here, append the suffic '_sub' to 'dribbling' to make it have a separate name for the SQL table 
                    else:
                        if player[f'{attribute}Attributes'][sub_attribute] != None:
                            player_sub_attribute_values[f'{sub_attribute}_sub'] = player[f'{attribute}Attributes'][sub_attribute]
                        else:
                            player_sub_attribute_values[f'{sub_attribute}_sub'] = player_attribute_values[attribute]
        
        # If the player is in fact a goalkeeper, then we just need to worry about the 6 face attributes
        else:
            for attribute in static_data.attributes[position]:
                player_attribute_values[attribute] = player['goalkeeperAttributes'][attribute]
        
        # We also want each player's price, and we need to make a separate request for that
        r_2 = requests.get(f'{url}/{id}/price', headers=header)
        
        # Get the data from the request
        price_data = r_2.json()
        price = price_data[platform]['price']
        
        # Now that we have the player's ID, name, club, league, nation, and price, insert it into his position's table and print his information as a confirmation
        data_for_table = (id, name, club, league, nation, price)
        cur.execute(f'INSERT INTO {position} (id, name, club, league, nation, price) VALUES (?, ?, ?, ?, ?, ?)', data_for_table)
        print(data_for_table)
        
        # We also need to insert the player's attribute values
        for attribute in static_data.attributes[position]:
            cur.execute(f'UPDATE {position} SET ({attribute}) = {player_attribute_values[attribute]} WHERE id = {id}')
            
            # Insert the player's sub-attribte values if he is not a goalkeeper
            if position != 'GK':
                for sub_attribute in static_data.sub_attributes[f'{attribute}Attributes']:
                    if sub_attribute != attribute:
                        cur.execute(f'UPDATE {position} SET ({sub_attribute}) = {player_sub_attribute_values[sub_attribute]} WHERE id = {id}')
                    else:
                        cur.execute(f'UPDATE {position} SET ({sub_attribute}_sub) = {player_sub_attribute_values[f"{sub_attribute}_sub"]} WHERE id = {id}')
        
        # Print a success statement
        print('Succesfully added')

# Commit the changes to the database and close the connection
con.commit()
cur.close()
con.close()
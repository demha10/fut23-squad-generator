import sqlite3
import static_data
# A program to quickly set up a database with a table for each position and the necessary information. Just to be run once
con = sqlite3.connect('players.db')
cur = con.cursor()

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

con.commit()
cur.close()
con.close()
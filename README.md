# **FIFA 23 Ultimate Team Squad Generator**
## **Introduction to EA Sports FIFA 23**

**Feel free to skip this section if you're well acquanited with EA Sports *FIFA* and *Ultimate Team*.**

**Jump to [running the program](#how-to-run-the-program)**

[*FIFA 23*](https://en.wikipedia.org/wiki/FIFA_23) is an immensely popular soccer simulation videogame by EA Sports, within which is a mode called *Ultimate Team* (*FUT*). In *FUT*, users (defined from here forward as a person playing *FIFA 23*) around the world play games against each other using custom-built squads, which feature virtual versions of real-life soccer players. *FUT* allows users to create a squad with players from a variety of real-life clubs, leagues, and nationalities.

Each soccer player has an overall rating, a set of 6 face attributes, and a set of 29 sub-attributes divided into the face attribute categories (unless the player is a goalkeeper, in which case there are only the 6 face attributes). For example, [Lionel Messi](https://www.futbin.com/23/player/26265/lionel-messi) is rated 91 overall, and he has 81 pace (among  6 face attributes we could pick). This 81 pace is the average of the two sub-attributes that make up pace: Acceleration (87) and sprint speed (76). Other attributes, like shooting, might have more constituent sub-attributes. Note that all ratings are out of 99.

A user has two main ways of acquiring a soccer player to build their squad. 
1. The user might get the player in a digital "pack", akin to a real-life card game, where you won't know what you'll get until you buy the pack and open it up. The user spends their "*FIFA* Coins", earned by winning games against other users or selling their players, to buy packs in hopes of getting good players. More highly rated players do not appear as frequently in packs, making them more scarce. 
2. A user might also buy a player from the "market", which is where users sell their players to each other for a price of their choosing. Broadly speaking, more highly rated players are more rare, and thus cost more on the market.

Of course, the goal is to acquire the best possible players to win more games, get more *FIFA* Coins, and buy better players (or packs), so you can win more games, etc. However, it's not so simple. *FUT* has a chemistry system, in which players' sub-attributes (and hence their performance in-game) are boosted by the presence of other players in the squad who share a real-life club, league, or nationality. The chemistry system is explained in detail [here](https://www.ea.com/games/fifa/pitch-notes/news/pitch-notes-fifa-23-fut-chemistry-update). This adds complexity in that a player in one squad can perform differently from a player in another squad due to his real-life relationships with other players.

Additionally, different *FUT* users might have different preferences in play style. For example, one user might prefer defenders who are fast and strong, not worrying so much about their passing ability. Another user might prefer defenders who are excellent passers and tacklers, not worrying about other attributes. When you put it all together, *FUT*'s popularity stems partly from the fact that it gives each user a unique question to answer every single time they play: 

>**What is the best squad I can make given my budget and my preferred play style?**

## **Enter: FIFA 23 Ultimate Team Best Squad Creator**
The goal of this program is to answer that question. It takes as input
- The amount of **money** the user has (in *FIFA* Coins)
- Their preferred **formation** (or team tactics)
- Their attribute **preferences** for each position

Then, it calculates the best possible squad you can buy with that amount of money - *best* as defined by the user's input. How does the program do that? There are basically 6 steps:

### 1. **Get user input**
First, the program gets the user's **budget, desired formation, and attribute preferences** by way of [`get_money`](#get_money), [`get_preferences`](#get_preferences), and [`get_formation`](#get_formation), all defined in [`helpers.py`](/helpers.py) and called by [`ultimate_team.py`](/ultimate_team.py).

### 2. **Allocate funds**
Next, [`pos_max`](#pos_max), another helper function, allocates the funds proportional to the average price of a player on the market in a given position, since some positions tend to cost more than others. Read the considerations that went into this decision [here](#how-to-allocate-funds). 

### 3. **Generating the best raw squad**
Now that we have a budget for each position, it's time to generate a squad. The function helper function [`best_raw_squad`](#best_raw_squad) takes care of this while also keeping a tally of all the clubs, leagues, and nations present in the squad (which will be of use later). Since there are no players yet, chemistry cannot be considered; as such the goal is simply to find the best player in each position, "best" as defined by the user's earlier input. Read how that is calculated [here](#calculate_rating).

### 4. **Calculating chemistry**
Now that we actually have 11 players, we can calculate each player's chemistry value, the boosts he receives as a result, and his new rating (according to the user's preferences). Passing in the raw team and the aforementioned tallies into [`calculate_chemistry`](#calculate_chemistry) takes care of this.

### 5. **Optimizing for chemistry**
Now we have a raw squad, and we know each player's rating as a combination of his base attributes and their boosts due to chemistry. The goal is now to figure out if we can do better than our current raw squad by considering chemistry. The question here is: *what players can we add who will improve the squad due to their club/nation/league?*

The helper function [`optimize`](#optimize) takes care of this recursively. In short, it finds the worst player in the raw squad, tries all his replacements, and picks the best one (if any replacement is in fact better than him). Then, the function moves onto the next worst player, repeating until there are no improvements made to the squad. Read more about the details [here](#optimize).

### 6. **Delivering results**
Finally, we print the results, showing the initial raw squad for funsies and the final squad, as well as each player's position. From start to finish, the command-line program looks like the following, which is run by running `python3 ultimate_team.py` in the terminal. In this example, we have 500,000 FIFA coins, and we'd like to play a 4-3-3, and we want a super fast LB but don't mind every other position's default preferences.
    
    How many FIFA coins do you have? 500000
    What formation do you want your team to have? 4-3-3

    In the process of calculating the best possible team, we need to calculate player ratings from the 6 attributes in FIFA 23 Ultimate Team. Here is how the creator of this program decided to weight each attribute for each position:

    DIVING has a weight 18 for GK.
    HANDLING has a weight 18 for GK.
    KICKING has a weight 10 for GK.
    POSITIONING has a weight 18 for GK.
    REFLEXES has a weight 18 for GK.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 20 for LB.
    SHOOTING has a weight 0 for LB.
    PASSING has a weight 20 for LB.
    DRIBBLING has a weight 20 for LB.
    DEFENDING has a weight 30 for LB.
    PHYSICALITY has a weight 10 for LB.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. y

    For each attribute, input the importance as a number from 0 to 100. The weight of all the attributes must sum to 100.

    Importance of pace for LB: 70
    Current total: 70
    Points left: 30
    5 more attributes

    Importance of shooting for LB: 6
    Current total: 76
    Points left: 24
    4 more attributes

    Importance of passing for LB: 6
    Current total: 82
    Points left: 18
    3 more attributes

    Importance of dribbling for LB: 6
    Current total: 88
    Points left: 12
    2 more attributes

    Importance of defending for LB: 6
    Current total: 94
    Points left: 6
    1 more attributes

    Importance of physicality for LB: 6
    Current total: 100
    Points left: 0
    0 more attributes

    PACE has a weight 10 for CB.
    SHOOTING has a weight 0 for CB.
    PASSING has a weight 15 for CB.
    DRIBBLING has a weight 5 for CB.
    DEFENDING has a weight 40 for CB.
    PHYSICALITY has a weight 30 for CB.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 20 for RB.
    SHOOTING has a weight 0 for RB.
    PASSING has a weight 20 for RB.
    DRIBBLING has a weight 20 for RB.
    DEFENDING has a weight 30 for RB.
    PHYSICALITY has a weight 10 for RB.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 10 for CM.
    SHOOTING has a weight 20 for CM.
    PASSING has a weight 30 for CM.
    DRIBBLING has a weight 15 for CM.
    DEFENDING has a weight 10 for CM.
    PHYSICALITY has a weight 15 for CM.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 25 for LW.
    SHOOTING has a weight 25 for LW.
    PASSING has a weight 15 for LW.
    DRIBBLING has a weight 20 for LW.
    DEFENDING has a weight 0 for LW.
    PHYSICALITY has a weight 15 for LW.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 20 for ST.
    SHOOTING has a weight 35 for ST.
    PASSING has a weight 10 for ST.
    DRIBBLING has a weight 20 for ST.
    DEFENDING has a weight 0 for ST.
    PHYSICALITY has a weight 15 for ST.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    PACE has a weight 25 for RW.
    SHOOTING has a weight 25 for RW.
    PASSING has a weight 15 for RW.
    DRIBBLING has a weight 20 for RW.
    DEFENDING has a weight 0 for RW.
    PHYSICALITY has a weight 15 for RW.
    Do you want to change the weight of any attribute in this position? Type 'y' if yes or hit enter for no. 

    Your initial squad is rated 82 by your criteria before optimizing for chemistry. It has the following players:
    Ederson at GK
    Alphonso Davies at LB
    Marquinhos at CB
    David Alaba at CB
    Juan Cuadrado at RB
    Nicolò Barella at CM
    Luka Modric at CM
    Paul Pogba at CM
    Raheem Sterling at LW
    Lautaro Martínez at ST
    Raphinha at RW

    Your final squad is rated 83 by your criteria after optimizing for chemistry. It has the following players:
    Juan Musso at GK
    Alphonso Davies at LB
    Marquinhos at CB
    David Alaba at CB
    Juan Cuadrado at RB
    Nicolò Barella at CM
    Luka Modric at CM
    Paul Pogba at CM
    Raheem Sterling at LW
    Lautaro Martínez at ST
    Raphinha at RW

    Note that the final squad should be rated higher based on the criteria you gave earlier due to the chemistry boosts, which are factored into calculations.

So, in this case, the program only changed one player. That's because for this test example, I downloaded a small subset of all of the players in *FUT*, namely, only *gold*, *rare*, *standard* players. *FUT* frequently creates new instances of players with boosted attributes depending on their real-life performances, and these players coexist with their normal base instances. These complexities are easily dealt with with minor tweaks to the program.

## Functions

### `get_money`
This function gets the user's budget in *FIFA* Coins, ensuring there are enough for a full squad of *gold* players and that the input is indeed an integer.

### `get_preferences`
This function getss the user's preferred weighting of each attribute for each position, ensuring that the weights add up to 100 for each position. These weights are then used by [`calculate_rating`](#calculate_rating) to calculate a player's overall rating, rather than using *FUT*'s default ratings. This allows for extra customizability on the user's part.

### `get_formation`
This function takes the user's desired formation, ensuring that it is indeed one of the formations in *FIFA* 23.

### `pos_max`
This function takes as input the user's budget and their formation and returns the maximum spend for each position, allocating the money proportional to the average price of each position. This data, along with other pieces of static data (like all of the positions, formations, etc), are in [`static_data.py`](/static_data.py). To make the program more dynamic, a future extension would get the live price of each player in a position and calculate the average. See [data collection](#data-collection) for more information.

### `calculate_rating`
This function takes as input a `player`, defined as a `dict` where each key is a player's name, and the value is another `dict` storing his data, like his club, league, nation, price, current chemistry level attributes, and sub-attributes. The chemistry affects the sub-attributes as defined [here](https://www.ea.com/games/fifa/pitch-notes/news/pitch-notes-fifa-23-fut-chemistry-update), whch in turn affect the attributes, which in turn affects the rating as determined by the player's preferences.

### `best_raw_squad`
This is the first interesting function in the program. Essentially, it takes as input the `positions` in the user's formation of choice, the maximum spend in each position (`maxes`), the database from which to pull information from, and the player's `preferences` in rating a player in a given position.

Then, it iterates over every position, querying the databse for all players in that position under the maximum spend (defined by `maxes[pos]`, where `pos` is the current `position`). Then, it iterates over every `player` returned by the query, calling `calculate_rating` to calculate his `rating`. It stores the highest rating it's seen for that position; if the current `player`'s `rating` is higher, than it stores that. After iterating over all the `player`s returned by the query, we have the highest rated `player` in that `pos`.

It then exists the loop which iterated over every `player` returned by the query and, from the data returned by the query, adds his club, league, and nation to a `dict` if not already present. If the club, league, or nation is present (meaning that we have already added a `player` to our squad that has one of these), it adds to the tally of that club, league, or nation.

Finally, it adds the `player` to the `raw_squad` `dict`, using his name as the key and a `dict` containing his information as the value. Then, it moves onto the next `pos` until we have completed all `positions` in the given formation.

### `calculate_chemistry`
This function takes as input a squad and all of the clubs, leagues, and nations present in the squad, as well as their counts. It iterates over every `player` in the squad and keeps track of the number of chemistry points a player gains from a given category of chemistry (the categories are `club`, `league`, and `nation`). These points are calculated with a [formula provided by EA Sports](https://www.ea.com/games/fifa/pitch-notes/news/pitch-notes-fifa-23-fut-chemistry-update). The maximum number of chemistry points a player can have is 3, so anything above that is set to 3. Then, the function calls [`calculate_rating`](#calculate_rating) to update the player's rating, now that he has a chemistry value.

### `optimize`
Finally, the meat of this project. The overall methodology of the function is as follows:
1. Iterate over each player in the squad and store the one with the worst `rating` (recall that `rating` now takes into account a player's chemistry). The player's `rating` is stored in `old_team[player]['rating']` in the context of `optimize`. If a player has maximum chemistry already (3), then he cannot possibly be improved, so we do not store players with 3 chemistry. Also, if we have already tried to replace this player (meaning he is in the list `done`) in a previous call of `optimize`, we do not consider him. This will likely not be the case for the first call of `optimize`.
2. If we did not assign any player as `worst`, then the function is done and we can return the input team (`old_team`).
3. If that's not the case, then we have a `worst` player. Get his `position` from the `old_team` `dict` and store it in `position` for easier manipulation later in the function.
4. Make a copy of the `dict` that stores the tallies of all the clubs, leagues, and nations in the team, and update the copy to reflect the removal of the `worst` player.
5. Then, we query the database for all the players in the `worst` player's position, storing them in a list called `options`. Iterate over every option, adding him into the new team and then testing the team's new rating via `calculate_team_rating`. If this new team rating is better than the old team rating, then we store the rating and the team. After iterating over every `option`, we have the best team we could get by substituting the player in that position. We can now pass this team into another call of `optimize` and repeat the process until we have the best team. 

## **How to run the program**
In order for this program to work as intended, you need a premium API key from [futdb.app](futdb.app). This allows you to get pricing data for each player. If you're interested in running the program with dummy data, I've provided a dummy database called `dummy.db` and the program I used to set up the database (`generate_dummy.py`) If you do have an API key, put it in `static_data.py` as the value for `API_key`.

If you don't have an API-key, follow these steps (the program is pre-configured with a dummy database):
1. Run `ultimate_team.py` in the terminal and follow the prompts.

If you do have an API-key, follow these steps:
1. Run `db_setup.py` to set up a database called `players.db`.
2. In `get_data.py`, adjust the parameters to your liking (or keep them as I have them to get only *gold*, *rare*, standard players).
3. Run `get_data.py` to get all the data from FutDB.
4. Finally, run `ultimate_team.py`. Follow the prompts the program gives you.

### **Dependencies**
This program requires the modules `sqlite3`, `random`, `statistics`, `random`, and `requests`, and it requires Python3.

## **Considerations**

### **How to allocate funds**
The first major challenge is how to allocate a user's money. You might say "well there are 11 positions, so just use 1/11 of the money for each position!" That'll work, but it might provide an imbalanced team because certain positions tend to have more expensive players. If you spend the same amount of money on your center back as you do on your striker, you'll end up with a disproportionately strong center back. Another way to tackle (pun-intended) the problem would be to implement a solution to the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem). This solution is not simple because you can only have one of each player, you need one of each position, and you need 11 players. Furthermore, solutions to the knapsack problem are typically time-complex. With roughly 16,000+ soccer players in *FUT*, it would surely slow the program (and probably unnecessarily, as the current algorithm generates satisfying results based on the intuitions of a lifelong soccer and *FIFA* fan). Nonetheless, implementing a proper, mathematically rigorous solution is an interesting extension to the program, one I'd like to try in the near future.

Instead, I went with the reasonable heuristic that I should allocate the funds proportional to the average cost of a player in a given position. For example, if strikers generally cost double what defenders cost, then I'll allocate double the money for a striker compared to what I would for a defender. As such, I set a cap on the spend for each position, the caps adding up to the total budget of the user.

## **Conclusion**
If you made it this far, I appreciate your interest! I hope this project was at least half as interesting to read about as it was to make for me, as it provided me with a lot of questions about how to maximize certain things. I know that this isn't a mathematically perfect way of implementing a solution; that probably requires some graph theory. In the future, I'd like to try tweaking this program to make it solve the problem perfectly.

## **Copyright Notice**
If you are a potential employer, feel free to test this program out and see how it works, adjusting whatever you like. However, please do not share it with anyone outside of your organization.
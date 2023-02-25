# POKEMON MOVE OPTIMIZER


## Video Demo:  

---

https://youtu.be/VsYbOWM-6NE

## Description

---

Pokemon is a video game where you train creatures and use them to battle AI or human trainers. Pokemon themselves have types and they can learn moves which have types, such as fire, grass and water. Moves can be "super-effective" against Pokemon and will do double the damage. Think of it kind of like rocks-paper-scissors. 

Pokemon can have up to 4 moves at a time, and when they learn a new one, it's up to the player to decide which to overwrite. The term "optimizer" is used with caution here, because what makes a Pokemon moveset optimal is highly dependent on the context. For this program, we're looking at what 4 types a Pokemon's moves should be in order to cover the most types super-effectively. Pokemon can have two types at once, but this program only considers single type cases. 

This is a command-line tool that takes in a Pokemon name and game version and prints to the console:
- List of damaging moves the Pokemon can learn, as well as how they learn them
- Which 4 types it should learn to cover the most types super-effectively as possible
- Which types are covered super-effectively
- Which types are not covered super-effectively

If there are multiple type sets that cover the maximum, they will all be printed.

This project is using [PokeAPI](https://pokeapi.co/), a RESTful API. All functions are contained to `project.py`. It starts by checking if the Pokemon name and version names given by the user are valid. To find out if the version name is valid, it makes a request to PokeAPI for the version-group subdirectory at the input. If it's not found, the program exits. It does the same for the Pokemon, by requesting the PokeAPI pokemon subdirectory for the given Pokemon, and if it's not found, it exits. If both of them are valid, the program successfully requests the Pokemon data from PokeAPI. Then it will get the list of types available in the input game version. In the first Pokemon game, there are 15 types. But some of the subsequent mainline games, refered to as *generations*, introduced new types. So the program checks which generation the input version is a part of and gets the applicable types. Sometimes generations also introduce changes to the double-damage relationship between types, so the program checks for that later as well.

Next, the program gets the move data for the Pokemon. It checks for special Pokemon cases, which is just Smeargle in this case. If the Pokemon is any Pokemon but Smeargle, the project goes through the moves key from the retrieved Pokemon data and does some work. It checks if the move can be learned by the Pokemon in the given version, then if so, it will make a request to PokeAPI for the move data and find out the type and if the move does damage. If a move gets through all those checks it's added to a dictionary which maps the move type to a list of moves. Each list item contains the name along with other meta data on the move such as how the Pokemon learns the move and the level it learns the move at, if applicable. The types and moves are printed out to the user. Originally, I was going to just print the types and moves for the final optimal sets, but in the case there are multiple optimal sets, printing out all the moves once felt less redundant, and it's cooler for the user to see.

From the dictionary in the above paragraph, the program makes a set of types, and then uses that set to calculate the different type combinations a Pokemon can have. If the Pokemon is Smeargle, the above step generating the types to moves dictionary is skipped, and it just uses all the available types in the generation for the next step. Then it finds the super-effective coverage for each combination. Finally, the sets with the maximum coverage are found and printed to the user. 

The `classify_moves` function is very central to this project. Originally, I had a separate function to find out the move types a Pokemon could learn, but I realized that if I do a dictionary of move types to the moves, I can just make a set out of the keys. It also allows for easy lookup of the moves later to print them out later. In this function, I originally created the class Move with attributes name, method and level. But I changed this to a simple list of the three attributes since it was easier to work with tabulate.

I used several pip-installable packages in this project. The `requests` package was used to make requests to the RESTful PokeApi, though I only needed to make get requests. `argparse` was used to make programming for the command line arguments easier. `sys` was used for exception handling. `roman` was used because the API provides generation numbers in roman numeral format, and I needed to convert them to integers. `itertools` was used to calculate the types combinations. I wanted to come up with my own function to find the type combinations, but I spent more time than expected on it and felt like I needed to heed the courses' advice of not reinventing the wheel if someone already came up with a good solution. `tabulate` was used to make the console output look nicer.

## Usage

---

Make sure to pip install the packages in requirements.txt, then in the console run:

```
python project.py -p pokemon_name -v version_name
```

#### Example

```
python project.py -p treecko -v emerald


Getting list of available types in given version...
Getting Pokemon information...
Getting moves information...
Checking move types...

╭─────────┬─────────╮
│ Pokemon │ Treecko │
├─────────┼─────────┤
│ Game    │ EMERALD │
╰─────────┴─────────╯

ALL DAMAGING MOVE TYPES FOR TREECKO:
['bug', 'dark', 'dragon', 'electric', 'fighting', 'flying', 'grass', 'ground', 'normal', 'rock', 'steel']

DAMAGING MOVES LEARNED BY TREECKO:

BUG
┌─────────────┬─────────────────┬──────────┐
│ Name        │ Level Learned   │ Method   │
├─────────────┼─────────────────┼──────────┤
│ Fury-Cutter │ N/A             │ Tutor    │
└─────────────┴─────────────────┴──────────┘

DARK
┌─────────┬─────────────────┬──────────┐
│ Name    │ Level Learned   │ Method   │
├─────────┼─────────────────┼──────────┤
│ Crunch  │ N/A             │ Egg      │
├─────────┼─────────────────┼──────────┤
│ Pursuit │ 16              │ Level-Up │
└─────────┴─────────────────┴──────────┘

DRAGON
┌───────────────┬─────────────────┬──────────┐
│ Name          │ Level Learned   │ Method   │
├───────────────┼─────────────────┼──────────┤
│ Dragon-Breath │ N/A             │ Egg      │
└───────────────┴─────────────────┴──────────┘

ELECTRIC
┌───────────────┬─────────────────┬──────────┐
│ Name          │ Level Learned   │ Method   │
├───────────────┼─────────────────┼──────────┤
│ Thunder-Punch │ N/A             │ Tutor    │
└───────────────┴─────────────────┴──────────┘

FIGHTING
┌───────────────┬─────────────────┬──────────┐
│ Name          │ Level Learned   │ Method   │
├───────────────┼─────────────────┼──────────┤
│ Rock-Smash    │ N/A             │ Machine  │
├───────────────┼─────────────────┼──────────┤
│ Focus-Punch   │ N/A             │ Machine  │
├───────────────┼─────────────────┼──────────┤
│ Brick-Break   │ N/A             │ Machine  │
├───────────────┼─────────────────┼──────────┤
│ Dynamic-Punch │ N/A             │ Tutor    │
└───────────────┴─────────────────┴──────────┘

FLYING
┌────────────┬─────────────────┬──────────┐
│ Name       │ Level Learned   │ Method   │
├────────────┼─────────────────┼──────────┤
│ Aerial-Ace │ N/A             │ Machine  │
└────────────┴─────────────────┴──────────┘

GRASS
┌─────────────┬─────────────────┬──────────┐
│ Name        │ Level Learned   │ Method   │
├─────────────┼─────────────────┼──────────┤
│ Absorb      │ 6               │ Level-Up │
├─────────────┼─────────────────┼──────────┤
│ Mega-Drain  │ 26              │ Level-Up │
├─────────────┼─────────────────┼──────────┤
│ Giga-Drain  │ 46              │ Level-Up │
├─────────────┼─────────────────┼──────────┤
│ Solar-Beam  │ N/A             │ Machine  │
├─────────────┼─────────────────┼──────────┤
│ Giga-Drain  │ N/A             │ Machine  │
├─────────────┼─────────────────┼──────────┤
│ Bullet-Seed │ N/A             │ Machine  │
└─────────────┴─────────────────┴──────────┘

GROUND
┌──────────┬─────────────────┬──────────┐
│ Name     │ Level Learned   │ Method   │
├──────────┼─────────────────┼──────────┤
│ Dig      │ N/A             │ Machine  │
├──────────┼─────────────────┼──────────┤
│ Mud-Slap │ N/A             │ Tutor    │
└──────────┴─────────────────┴──────────┘

NORMAL
┌──────────────┬─────────────────┬──────────┐
│ Name         │ Level Learned   │ Method   │
├──────────────┼─────────────────┼──────────┤
│ Crush-Claw   │ N/A             │ Egg      │
├──────────────┼─────────────────┼──────────┤
│ Pound        │ 1               │ Level-Up │
├──────────────┼─────────────────┼──────────┤
│ Slam         │ 36              │ Level-Up │
├──────────────┼─────────────────┼──────────┤
│ Quick-Attack │ 11              │ Level-Up │
├──────────────┼─────────────────┼──────────┤
│ Cut          │ N/A             │ Machine  │
├──────────────┼─────────────────┼──────────┤
│ Strength     │ N/A             │ Machine  │
├──────────────┼─────────────────┼──────────┤
│ Hidden-Power │ N/A             │ Machine  │
├──────────────┼─────────────────┼──────────┤
│ Facade       │ N/A             │ Machine  │
├──────────────┼─────────────────┼──────────┤
│ Secret-Power │ N/A             │ Machine  │
├──────────────┼─────────────────┼──────────┤
│ Mega-Punch   │ N/A             │ Tutor    │
├──────────────┼─────────────────┼──────────┤
│ Mega-Kick    │ N/A             │ Tutor    │
├──────────────┼─────────────────┼──────────┤
│ Body-Slam    │ N/A             │ Tutor    │
├──────────────┼─────────────────┼──────────┤
│ Double-Edge  │ N/A             │ Tutor    │
├──────────────┼─────────────────┼──────────┤
│ Swift        │ N/A             │ Tutor    │
├──────────────┼─────────────────┼──────────┤
│ Snore        │ N/A             │ Tutor    │
└──────────────┴─────────────────┴──────────┘

ROCK
┌───────────┬─────────────────┬──────────┐
│ Name      │ Level Learned   │ Method   │
├───────────┼─────────────────┼──────────┤
│ Rock-Tomb │ N/A             │ Machine  │
└───────────┴─────────────────┴──────────┘

STEEL
┌───────────┬─────────────────┬──────────┐
│ Name      │ Level Learned   │ Method   │
├───────────┼─────────────────┼──────────┤
│ Iron-Tail │ N/A             │ Machine  │
└───────────┴─────────────────┴──────────┘

Option 1
╔═════════════╦════╦═════════════════════════════════════════════════════════════════════════════════════════════╗
║ Types       ║    ║ fighting, flying, grass, ground                                                             ║
╠═════════════╬════╬═════════════════════════════════════════════════════════════════════════════════════════════╣
║ Covered     ║ 13 ║ bug, dark, electric, fighting, fire, grass, ground, ice, normal, poison, rock, steel, water ║
╠═════════════╬════╬═════════════════════════════════════════════════════════════════════════════════════════════╣
║ Not covered ║ 4  ║ dragon, flying, ghost, psychic                                                              ║
╚═════════════╩════╩═════════════════════════════════════════════════════════════════════════════════════════════╝
Option 2
╔═════════════╦════╦══════════════════════════════════════════════════════════════════════════════════════════════╗
║ Types       ║    ║ dark, fighting, flying, ground                                                               ║
╠═════════════╬════╬══════════════════════════════════════════════════════════════════════════════════════════════╣
║ Covered     ║ 13 ║ bug, dark, electric, fighting, fire, ghost, grass, ice, normal, poison, psychic, rock, steel ║
╠═════════════╬════╬══════════════════════════════════════════════════════════════════════════════════════════════╣
║ Not covered ║ 4  ║ dragon, flying, ground, water                                                                ║
╚═════════════╩════╩══════════════════════════════════════════════════════════════════════════════════════════════╝
Option 3
╔═════════════╦════╦════════════════════════════════════════════════════════════════════════════════════════════╗
║ Types       ║    ║ bug, grass, ground, rock                                                                   ║
╠═════════════╬════╬════════════════════════════════════════════════════════════════════════════════════════════╣
║ Covered     ║ 13 ║ bug, dark, electric, fire, flying, grass, ground, ice, poison, psychic, rock, steel, water ║
╠═════════════╬════╬════════════════════════════════════════════════════════════════════════════════════════════╣
║ Not covered ║ 4  ║ dragon, fighting, ghost, normal                                                            ║
╚═════════════╩════╩════════════════════════════════════════════════════════════════════════════════════════════╝
Option 4
╔═════════════╦════╦═════════════════════════════════════════════════════════════════════════════════════════════╗
║ Types       ║    ║ electric, fighting, flying, ground                                                          ║
╠═════════════╬════╬═════════════════════════════════════════════════════════════════════════════════════════════╣
║ Covered     ║ 13 ║ bug, dark, electric, fighting, fire, flying, grass, ice, normal, poison, rock, steel, water ║
╠═════════════╬════╬═════════════════════════════════════════════════════════════════════════════════════════════╣
║ Not covered ║ 4  ║ dragon, ghost, ground, psychic                                                              ║
╚═════════════╩════╩═════════════════════════════════════════════════════════════════════════════════════════════╝ 

```

For a list of Pokemon, check [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number).

For the valid list of version names, use:

```
python project.py -h
```

There may be a slight delay since this calls the API to check the available version data.

## Future Updates
Some future updates I'm thinking about
- Decoupling functions
- More prompts such as, does this Pokemon learn any ___ type moves?

## Contributing
Feel free to make any pull requests, but please update the tests as well.

## License
[MIT](https://choosealicense.com/licenses/mit/)

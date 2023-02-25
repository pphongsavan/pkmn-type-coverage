import requests
import argparse
import sys
import roman
from itertools import combinations
from tabulate import tabulate

'''
Prinyavong Phongsavan
CS50P Final Project
Pokemon Moveset Optimizer

This is a command-line tool that takes in a Pokemon name and game version and prints to the console:
    List of damaging moves the Pokemon can learn, as well as their learn methods
    Which 4 types it should learn to cover as many types super-effectively as possible
    Which types are covered super-effectively
    Which types are not covered super-effectively
'''


def main():

    # Instantiate list of versions from PokeAPI
    versions = get_valid_versions()

    # Set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help=f"Game version. Valid args: {versions}")
    parser.add_argument("-p", help="Name of Pokemon") 
    args = parser.parse_args()

    # Set cli args to variables
    GAME_VERSION = args.v
    PKMN_NAME = args.p.lower()

    # Headers for the tabulate tables of moves we print later
    HEADERS = ["Name", "Level Learned", "Method"]

    # Check if version is valid and Pokemon is valid and available in given game
    try:
        if valid_version(GAME_VERSION, versions):
            GEN = get_gen_num(get_generation(GAME_VERSION))

            print("Getting list of available types in given version...")
            TYPES_IN_GEN = get_available_types(GEN)

            print("Getting Pokemon information...")
            
            pkmn_json = get_pkmn_json(PKMN_NAME)

            print("Getting moves information...")

            # Smeargle is a special Pokemon that can copy almost all moves
            if PKMN_NAME == "smeargle":
                move_types = set(TYPES_IN_GEN)
            else:
                types_to_moves_dict = classify_moves(pkmn_json, GAME_VERSION)

                # In the case of no damaging moves found (Ditto, Wobbufett, etc.) return early
                if types_to_moves_dict == {}:
                    print("")
                    pkmn_table = ["Pokemon", PKMN_NAME.title()], ["Game", GAME_VERSION.upper()]
                    print(tabulate(pkmn_table, tablefmt="rounded_grid"))
                    print("")
                    print(f"{PKMN_NAME.title()} cannot learn any damaging moves.")
                    return

                move_types = set(types_to_moves_dict.keys())

            print("Checking move types...")
            print("")

            # Print out a small table with the Pokemon name and input version
            pkmn_table = ["Pokemon", PKMN_NAME.title()], ["Game", GAME_VERSION.upper()]
            print(tabulate(pkmn_table, tablefmt="rounded_grid"))
            print("")
        
            # Print out tables of moves if the input Pokemon isn't Smeargle
            if PKMN_NAME != "smeargle":
                print(f"ALL DAMAGING MOVE TYPES FOR {PKMN_NAME.upper()}: ")
                print(f"{sorted(list(move_types))}")
                print("")

                print(f"DAMAGING MOVES LEARNED BY {PKMN_NAME.upper()}: ")
                print("")

                # Print out each type and the corresponding moves in ABC order
                types_alphabatized = sorted(list(types_to_moves_dict.keys()))
                for k in types_alphabatized:
                    print(k.upper())
                    moves_sorted_by_method = sorted(types_to_moves_dict[k], key = lambda x: x[2])
                    print(tabulate(moves_sorted_by_method, HEADERS, tablefmt="simple_grid"))
                    print("")

            # Get all possible type combos
            types_to_se = create_type_to_se_dict(move_types, GEN)
            combos = get_type_combos(move_types)

            # Check what each type combo covers super-effectively, then find the ones with most coverage
            len_to_combos, combos_to_se = create_se_sets(combos, types_to_se)
            max_combos = len_to_combos[max(len_to_combos)]

            # Special output for Smeargle
            if PKMN_NAME == "smeargle":
                print("Smeargle can learn all move types by using its special move Sketch.")
                print("Use Sketch to copy any of these type combos: ")
                print("")

            # Print out the combos with the most coverage, then the types they cover, then the ones they don't
            for i, c in enumerate(max_combos):
                print(f"Option {i + 1}")
                not_covered = TYPES_IN_GEN - combos_to_se[c]
                types_str = ', '.join(sorted(list(c)))
                covered_str = ', '.join(sorted(list(combos_to_se[c])))
                not_covered_str = ', '.join(sorted(list(not_covered)))
                table = [["Types", "", types_str], ["Covered", len(combos_to_se[c]), covered_str], ["Not covered", len(not_covered), not_covered_str]]
                print(tabulate(table, tablefmt="double_grid"))

        else:
            # Input Pokemon name not found
            sys.exit(f"Pokemon '{PKMN_NAME.title()}' is not available in version '{GAME_VERSION}'")
    except ValueError:
        # Input game version not found
        sys.exit(f"'{GAME_VERSION}' is not a valid game version. Please use 'project.py -h' to view valid options")

'''
Call API and get a list of valid game versions

:return: A list of game version names
:rtype: list
'''
def get_valid_versions():
    valid = []
    versions = url_to_json("https://pokeapi.co/api/v2/version-group")
    for v in versions['results']:
        valid.append(v['name'])
    return valid

'''
Gets a set of available types in a given generation

:param gen: Generation number of a game
:type gen: int
:return: A set of strs representing types
:rtype: set
'''
def get_available_types(gen):
    types = set()
    for i in range(1 ,gen + 1):
        generation = url_to_json(f"https://pokeapi.co/api/v2/generation/{i}/")
        for t in generation["types"]:
            # Some generations have special types. After the /type/ portion of the URL, these have values greater than double digits
            t_url = t["url"]
            # Cut off the beginning of the type URL and the last character, "/"
            # Ex: https://pokeapi.co/api/v2/type/10002/
            # Turns into 10002
            t_url = t_url[31:-1]
            t_url = int(t_url)
            if t_url < 20:
                types.add(t["name"])
    
    return types

# Check if a passed version arg is valid
'''
Check if a passed version arg is valid

:param version: Game version
:type version: str
:param valid_versions: A list of game version names
:type
:raise ValueError: If version not found in valid versions
:return: True if valid
:rtype: bool
'''
def valid_version(version, valid_versions):
    if version in valid_versions:
        return True
    else:
        raise ValueError()

'''
Get the generation a game came from based on version-group

:param version: Game version
:type version: str
:return: "generation-xyz" where xyz is a roman numeral
:rtype: str
'''
def get_generation(version):
    version_group_json = url_to_json(f"https://pokeapi.co/api/v2/version-group/{version}")
    return version_group_json["generation"]["name"]

'''
Get the number of a generation from the string "generation-xyz" where xyz is the generation no.

:param generation: "generation-xyz" where xyz is a roman numeral
:return: Integer generation number converted from roman numeral
:rtype: int
'''
def get_gen_num(generation):
    rn = generation[11:].upper()
    return(roman.fromRoman(rn))

'''
Get JSON from URL

:param url: request URL
:type url: str
:return: JSON data from get request
:rtype: dict (in most cases for this program)
'''
def url_to_json(url):
    j = requests.get(url).json()
    return j

'''
Retrive a single Pokemon from the API and return JSON

:param pkmn_name: Name of Pokemon. Must be lowercase.
:type pkmn_name: str
:except ValueError: If request URL not valid
:return: JSON data for Pokemon
:rtype: dict
'''
def get_pkmn_json(pkmn_name):
    try:
        j = url_to_json(f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}")
    except ValueError:
        sys.exit(f"Pokemon named '{pkmn_name}' not found.")
    return j

'''
Check if a Pokemon is available in a given version

:param pkmn_json: Pokemon data from API
:type pkmn_json: dict
:param version: Game version
:type version: str
:return: True if obtainable, False if not
:r type: bool 
'''
def available_in_version(pkmn_json, version):
    for v in pkmn_json['game_indices']:
        if v['version']['name'] == version:
            return True
    return False

'''
Get the type of a Pokemon move as string

:param move_json: Move data from API
:type move_json: dict
:return: The move's type
:rtype: str
''' 
def get_move_type(move_json):
    return(move_json['type']['name'])

'''
Check if a move does damage

:param move_json: Move data from API
:type move_json: dict
:return: True if move does damage, False if not
:rtype: bool
'''
def does_damage(move_json):
    return True if move_json["power"] else False

'''
Check if a move is learnable by a Pokemon in the given version

:param move: Move item from the move property from a Pokemon JSON
:type move: dict
:param version: Game version
:type version: str
:return: True if learnable, False if not
:r type: bool
'''
def learnable_in_version(move, version):
    for k in move['version_group_details']:
        if k['version_group']['name'] == version:
            return True
    return False

'''
Create a dict of move type to list of lists containing move attributes
Each item in the dict list goes: [move name, move learn method, level learned]

:param pkmn_json: Pokemon data from API
:type pkmn_json: dict
:param version: Game version
:type version: str
:return: Dict of move type to a list of move names
:r type: dict
'''
def classify_moves(pkmn_json, version):
    moves_dict = {}

    # move is the move info from the Pokemon moves json, which only includes name and learn details
    for move in pkmn_json['moves']:
        if learnable_in_version(move, version):
            # move_json is the url to the move details including damange and type
            move_json = url_to_json(move['move']['url'])
            if does_damage(move_json):
                type_ = get_move_type(move_json)
                if type_ not in moves_dict:
                    moves_dict[type_] = []
                
                # Find the version group that matches input version
                for vgd_idx in move['version_group_details']:
                    if vgd_idx['version_group']['name'] == version:
                        name = move['move']['name'].title()
                        method = vgd_idx['move_learn_method']['name'].title()
                        if method != "Level-Up":
                            level = "N/A"
                        else:
                            level = vgd_idx['level_learned_at']
                        new_move = [name, level, method]
                        moves_dict[type_].append(new_move)
                        continue

    return moves_dict

'''
Determine which generation's damage relations to use
Returning (0,0) indicates we need to use the latest type effectiveness available

:param gen: Integer generation number
:type gen: int
:param past_drs: The past_damage_relations attribute from a type's API data
:type past_drs: list
:return: A tuple of (index in past_damage_relations to look into, generation number for the damage relation)
:rtype: tuple
'''
def get_dr_to_use(gen, past_drs):
    i = 0
    while gen > past_drs[i]:
        if i + 1 > len(past_drs) - 1:
            return (0,0)
        else:
            i += 1
    
    return (i,past_drs[i])

'''
Given the type API info, return a list of generation numbers where the damage relations changed

:param type_json: Type info from API
:type type_json: dict
:return: List of generation numbers where damage relations changed for that type
:rtype: list
'''
def get_past_dr_list(type_json):
    gens = []
    for dr in type_json["past_damage_relations"]:
        gens.append(dr["generation"]["name"])
    for i in range(len(gens)):
        gen_num = get_gen_num(gens[i])
        gens[i] = gen_num

    return gens

'''
Create a dictionary of type to type coverage

:param types: Each type in the given gen
:type types: set
:param gen: Integer generation number
:type gen: int
:return: Types to a set of types that the type is super effective against
:rtype: dict 
'''
def create_type_to_se_dict(types, gen):
    type_to_se = {}
    for type in types:
        type_json = url_to_json(f"https://pokeapi.co/api/v2/type/{type}")
        type_to_se[type] = get_super_effective(type_json, gen)
    return type_to_se

'''
Get a set of super effective coverage for a single type

:param type_json: Type info from API
:type type_json: dict
:param gen: Integer generation number
:type gen: int
:return: Set of types the input type is super effective against
:rtype: set
'''
def get_super_effective(type_json, gen):
    super_effective = set()

    # Normal type moves are not super effective to anything, so return an empty set
    if type_json['name'] == "normal":
        return super_effective

    if type_json['past_damage_relations']:
        past_drs = get_past_dr_list(type_json)
        gen_to_use = get_dr_to_use(gen, past_drs)
        if gen_to_use != (0,0):
            double_prop = type_json['past_damage_relations'][gen_to_use[0]]["damage_relations"]["double_damage_to"]
        else:
            double_prop = type_json['damage_relations']['double_damage_to']
    else:
        double_prop = type_json['damage_relations']['double_damage_to']
    for d in double_prop:
        super_effective.add(d['name'])
    return super_effective

'''
Given a set of types, get all possible combinations of 4 (Pokemon can only have 4 moves at a time max)

:param types: Set of types
:type types: set
:return: Set of tuples representing type combos for each combination of 4
:return type: set
'''
def get_type_combos(types):
    if len(types) <= 4:
        # itertools.combinations returns a tuple so we need to convert types to a tuple 
        # for create_se_set to work properly later
        # if we just do set(list(types)) it will loop over letters of each type instead of each type
        tc = set()
        types = tuple(types)
        tc.add(types)
        return tc
    else:
        return set(list(combinations(types, 4)))

'''
Given a list of types, create a set of types the list is super-effective to

:param types: Set of types
:type types: set
:param type_to_se_dict: Types to a set of types that the type is super effective against
:type type_to_se_dict: dict
:return: set of types the types set covers super effectively 
:rtype: set
'''
def create_se_set(types, type_to_se_dict):
    se = set()
    for t in types:
        for i in type_to_se_dict[t]:
            se.add(i)
    return se


'''
Creates two dicts out of a set of type combinations
types_to_se: A type combination to a set of types the combo covers super effectively
se_lens: The number of types the combo covers super effectively to a list of the combos

:param combos: Set of tuples representing type combos for each combination of 4
:param type: set
:param type_to_se_dict: Types to a set of types that the type is super effective against
:type type_to_se_dict: dict
:return: Two dicts, noted above
:rtype: dict, dict
'''
def create_se_sets(combos, type_to_se_dict):
    types_to_se = {}
    se_lens = {}

    for c in combos:
        curr = create_se_set(c, type_to_se_dict)
        if len(curr) in se_lens:
            se_lens[len(curr)].append(c)
        else:
            se_lens[len(curr)] = [c]
        types_to_se[c] = curr
    
    return se_lens, types_to_se

if __name__ == "__main__":
    main()
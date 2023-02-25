import project

def test_get_move_type():
    thunder_punch = project.url_to_json("https://pokeapi.co/api/v2/move/9/")
    assert project.get_move_type(thunder_punch) == 'electric'

def test_learnable_in_version():
    pikachu = project.get_pkmn_json("pikachu")
    # Pikachu can't learn Surf in Ruby and Sapphire
    assert project.learnable_in_version(pikachu['moves'][12], "ruby-sapphire") == False
    # But it can learn it in Yellow
    assert project.learnable_in_version(pikachu['moves'][12], "yellow") == True

def test_available_in_version():
    totodile = project.get_pkmn_json("totodile")
    assert project.available_in_version(totodile, "gold") == True
    assert project.available_in_version(totodile, "red") == False

def test_get_super_effective():
    ghost = project.url_to_json("https://pokeapi.co/api/v2/type/ghost")

    # Ghost is super effective to Psychic in gen 6 but not gen 1
    assert project.get_super_effective(ghost, 6) == {'psychic', 'ghost'}
    assert project.get_super_effective(ghost, 1) == {'ghost'}

    # Normal is not super effective against anything, so we expect an empty set
    normal = project.url_to_json("https://pokeapi.co/api/v2/type/1")
    assert project.get_super_effective(normal, 6) == set()

def test_does_damage():
    tbolt = project.url_to_json("https://pokeapi.co/api/v2/move/85/")
    assert(project.does_damage(tbolt)) == True

    sand_attack = project.url_to_json("https://pokeapi.co/api/v2/move/28/")
    assert(project.does_damage(sand_attack)) == False

def test_get_generation():
    assert(project.get_generation("red-blue")) == "generation-i"
    assert(project.get_generation("ruby-sapphire")) == "generation-iii"

def test_get_gen_num():
    assert(project.get_gen_num("generation-i")) == 1
    assert(project.get_gen_num("generation-v")) == 5
    assert(project.get_gen_num("generation-viii")) == 8
    assert(project.get_gen_num("generation-x")) == 10

def test_get_past_dr_list():
    ghost = project.url_to_json("https://pokeapi.co/api/v2/type/ghost")
    assert(project.get_past_dr_list(ghost)) == [1,5]
    dark = project.url_to_json("https://pokeapi.co/api/v2/type/dark")
    assert(project.get_past_dr_list(dark)) == [5]

def test_get_dr_to_use():
    assert(project.get_dr_to_use(1, [1,2,5])) == (0,1)
    assert(project.get_dr_to_use(2, [1,2,5])) == (1,2)
    assert(project.get_dr_to_use(5, [1,2,5])) == (2,5)
    assert(project.get_dr_to_use(3, [1,2,5])) == (2,5)
    assert(project.get_dr_to_use(6, [1,2,5])) == (0,0)

def test_get_available_types():
    # Gen 1 starts with the original 15 types
    assert(project.get_available_types(1)) == {"normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "fire", "water", "grass", "electric", "psychic", "ice", "dragon"}
    # Gen 2 introduces steel and dark types
    assert(project.get_available_types(2)) == {"normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "steel"}
    # Gen 3 has a special type, Shadow, but we don't want to include it
    assert(project.get_available_types(3)) == {"normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "steel"}
    # Gen 6 introduces fairy type
    assert(project.get_available_types(6)) == {"normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "steel", "fairy"}
    # Gen 7 doesn't introduce any types. Should match Gen 6
    assert(project.get_available_types(7)) == {"normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "steel", "fairy"}
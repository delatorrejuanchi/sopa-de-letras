#!usr/bin/python3

import pytest
from random import shuffle, seed
from main import *

dictionary = ["MANY", "DAFFY", "INCREDIBLE", "MATCH", "PENITENT", "ADMIT",
                "DECOROUS", "BROAD", "STUPID", "AGONIZING", "DISGUSTED",
                "DROP", "FORGETFUL", "RULE", "OBESE", "CATS", "TYPICAL",
                "SPACE", "BOTTLE", "RARE", "FILTHY", "SMOKE", "WOOZY",
                "YOUTHFUL", "CROWDED", "RACE", "ITCHY", "SOUND", "PUNCH",
                "MESS", "EARTH", "SOFT", "MEAL", "ANNOYED", "HOME",
                "DETERMINED", "FINICKY", "CLOISTERED", "FEAR", "MUTE",
                "FRESH", "ZANY", "HELP", "OVEN", "SILLY", "PIE", "DAM",
                "ALARM", "WILD", "WAVE", "NIGHT", "ACOUSTIC", "CREEPY",
                "WHOLESALE", "BLINK", "NEIGHBORLY", "WONDERFUL", "RUN",
                "SLEEPY", "EXUBERANT", "TWIST", "BALANCE", "STATEMENT",
                "BLACK", "DISTANCE", "AWFUL", "MILITARY", "OBSERVATION",
                "PLUCKY", "WAX", "SKINNY", "BEHAVIOR", "FLIGHT", "ROT",
                "VALUE", "FINE", "TOY", "CELLAR", "GLIB", "DOGS", "KILL",
                "MEND", "APPROVE", "RAIN", "ELEGANT", "ANXIOUS", "SHOE",
                "SUSPEND", "IRATE", "SORT", "EXCLUSIVE", "ROOF", "CAN",
                "HOOK", "BUZZ", "CONFUSED", "EMPLOY", "VALUABLE", "RESCUE",
                "SUIT"]

seed(1234)


def test_get_wordlist_input():
    pass


def test_is_wordlist_valid():
    valid_wordlist = ["PERRO", "GATO", "AUSTRALIA"]
    invalid_wordlist_not_uppercase = ["perro", "gato", "australia"]
    invalid_wordlist_single_character_word = ["PERRO", "GATO", "A"]
    invalid_wordlist_not_alphabetic = ["PERRO", "GATO", "14", "5", "%"]

    assert(is_wordlist_valid(valid_wordlist))
    assert(not is_wordlist_valid(invalid_wordlist_not_uppercase))
    assert(not is_wordlist_valid(invalid_wordlist_single_character_word))
    assert(not is_wordlist_valid(invalid_wordlist_not_alphabetic))                


def test_generate_soup():
    n_words = 10
    
    for i in range(1000):
        shuffle(dictionary)        
        wordlist = dictionary[:n_words]
        soup = generate_soup(wordlist)

        assert(type(soup) == list)
        assert(all([type(row) == list for row in soup]))
        assert(all([type(letter) == str for row in soup for letter in row ]))


def test_calculate_soup_size():
    wordlist_1 = ["PERRO", "ELECTRON", "COMIDA", "RELOJ", "TERMO"]
    wordlist_2 = ["GUINNESS", "QUILMES", "STELLA", "SANTAFE"]
    wordlist_3 = ["EMPANDA", "ASADO", "GUIZO", "SPAGHETTI"]

    assert(calculate_soup_size(wordlist_1) == 10)
    assert(calculate_soup_size(wordlist_2) == 10)
    assert(calculate_soup_size(wordlist_3) == 11)                


def test_generate_word_placements():
    n_words = 10
    
    for i in range(1000):
        shuffle(dictionary)   
        wordlist = dictionary[:n_words]
        soup_size = calculate_soup_size(wordlist)

        word_placements = generate_word_placements(wordlist, soup_size)

        assert(type(word_placements) == dict)
        assert(all([type(key) == str for key in word_placements]))
        assert(all([type(value) == dict for value in word_placements.values()]))
    

def test_try_to_place():
    pass


def test_is_placement_valid():
    word = "PERRO"
    word_placements = {
        "GATO": {
            "row": 2,
            "col": 2,
            "orientation": Orientation.DIAGONAL
        },
        "AUTO": {
            "row": 6,
            "col": 0,
            "orientation": Orientation.HORIZONTAL_REVERSED
        }
    }
    size = 7

    placement_1 = {
        "row": 0,
        "col": 0,
        "orientation": Orientation.HORIZONTAL
    }

    placement_2 = {
        "row": 6,
        "col": 6,
        "orientation": Orientation.DIAGONAL
    }

    placement_3 = {
        "row": 1,
        "col": 5,
        "orientation": Orientation.VERTICAL
    }

    placement_4 = {
        "row": 1,
        "col": 2,
        "orientation": Orientation.VERTICAL_REVERSED
    }

    assert(is_placement_valid(word, placement_1, word_placements, size))
    assert(not is_placement_valid(word, placement_2, word_placements, size))
    assert(is_placement_valid(word, placement_3, word_placements, size))
    assert(not is_placement_valid(word, placement_4, word_placements, size))
    

def test_get_letter_positions():
    word_1 = "PERRO"
    placement_1 = {
        "row": 4,
        "col": 6,
        "orientation": Orientation.HORIZONTAL
    }

    letter_postions_1 = {
        (4, 6): "P",
        (4, 7): "E",
        (4, 8): "R",
        (4, 9): "R",
        (4, 10): "O"
    }
    
    word_2 = "GATO"
    placement_2 = {
        "row": 0,
        "col": 0,
        "orientation": Orientation.DIAGONAL
    }

    letter_postions_2 = {
        (0, 0): "G",
        (1, 1): "A",
        (2, 2): "T",
        (3, 3): "O"
    }

    word_3 = "ELECTRON"
    placement_3 = {
        "row": 9,
        "col": 5,
        "orientation": Orientation.VERTICAL_REVERSED
    }

    letter_postions_3 = {
        (9, 5): "N",
        (10, 5): "O",
        (11, 5): "R",
        (12, 5): "T",
        (13, 5): "C",
        (14, 5): "E",
        (15, 5): "L",
        (16, 5): "E",                
    }

    assert(get_letter_positions(word_1, placement_1) == letter_postions_1)
    assert(get_letter_positions(word_2, placement_2) == letter_postions_2)
    assert(get_letter_positions(word_3, placement_3) == letter_postions_3)
            

def test_create_soup_matrix():
    size = 7
    word_placements = {
        "PERRO": {
            "row": 1,
            "col": 5,
            "orientation": Orientation.VERTICAL
        },
        "GATO": {
            "row": 2,
            "col": 2,
            "orientation": Orientation.DIAGONAL
        },
        "AUTO": {
            "row": 6,
            "col": 0,
            "orientation": Orientation.HORIZONTAL_REVERSED
        }
    }
    soup = create_soup_matrix(size, word_placements)

    assert(type(soup) == list)
    assert(all([type(row) == list for row in soup]))
    assert(all([type(letter) == str for row in soup for letter in row]))


def test_random_letter():
    pass


def test_display_soup():
    pass


def test_color_soup():
    pass


def test_solve_soup():
    pass


def test_find_word_placement():
    pass


def test_find_first_letter_candidates():
    pass


def test_parse_soups():
    pass

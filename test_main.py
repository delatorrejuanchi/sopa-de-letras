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

    for _ in range(1000):
        shuffle(dictionary)
        wordlist = dictionary[:n_words]
        soup = generate_soup(wordlist)

        assert(type(soup) == list)
        assert(all([type(row) == list for row in soup]))
        assert(all([type(letter) == str for row in soup for letter in row]))


def test_calculate_soup_size():
    wordlist_1 = ["PERRO", "ELECTRON", "COMIDA", "RELOJ", "TERMO"]
    wordlist_2 = ["GUINNESS", "QUILMES", "STELLA", "SANTAFE"]
    wordlist_3 = ["EMPANDA", "ASADO", "GUIZO", "SPAGHETTI"]

    assert(calculate_soup_size(wordlist_1) == 10)
    assert(calculate_soup_size(wordlist_2) == 10)
    assert(calculate_soup_size(wordlist_3) == 11)


def test_generate_word_placements():
    n_words = 10

    for _ in range(1000):
        shuffle(dictionary)
        wordlist = dictionary[:n_words]
        soup_size = calculate_soup_size(wordlist)

        word_placements = generate_word_placements(wordlist, soup_size)

        assert(type(word_placements) == dict)
        assert(all([type(key) == str for key in word_placements]))
        assert(all([type(val) == dict for val in word_placements.values()]))


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
    soup = [["P", "A", "E", "N", "J", "Y", "U", "K", "I", "F", "C"],
            ["E", "X", "Y", "L", "P", "C", "Y", "W", "V", "A", "L"],
            ["E", "J", "V", "Q", "B", "J", "X", "I", "C", "G", "F"],
            ["E", "S", "T", "O", "R", "N", "U", "D", "O", "N", "U"],
            ["U", "D", "N", "W", "Z", "M", "D", "O", "R", "U", "T"],
            ["Y", "R", "S", "E", "Ñ", "A", "Ñ", "C", "R", "S", "B"],
            ["L", "O", "Y", "H", "L", "T", "D", "O", "I", "M", "O"],
            ["E", "X", "V", "P", "H", "E", "Y", "N", "E", "A", "L"],
            ["Q", "V", "X", "U", "H", "R", "V", "A", "N", "S", "X"],
            ["C", "I", "N", "T", "A", "A", "C", "I", "T", "J", "K"],
            ["B", "X", "K", "X", "G", "O", "P", "P", "E", "E", "S"]]

    wordlist = {"PIANO", "MATERA", "FUTBOL", "CORRIENTE",
                "CINTA", "ESTORNUDO", "SAMSUNG"}

    word_placements = {
        "PIANO": {
            "row": 6,
            "col": 7,
            "orientation": Orientation.VERTICAL_REVERSED
        },
        "MATERA": {
            "row": 4,
            "col": 5,
            "orientation": Orientation.VERTICAL
        },
        "FUTBOL": {
            "row": 2,
            "col": 10,
            "orientation": Orientation.VERTICAL
        },
        "CORRIENTE": {
            "row": 2,
            "col": 8,
            "orientation": Orientation.VERTICAL
        },
        "CINTA": {
            "row": 9,
            "col": 0,
            "orientation": Orientation.HORIZONTAL
        },
        "ESTORNUDO": {
            "row": 3,
            "col": 0,
            "orientation": Orientation.HORIZONTAL
        },
        "SAMSUNG": {
            "row": 2,
            "col": 9,
            "orientation": Orientation.VERTICAL_REVERSED
        }
    }

    assert(solve_soup(soup, wordlist) == word_placements)


def test_find_word_placement():
    soup = [["P", "A", "E", "N", "J", "Y", "U", "K", "I", "F", "C"],
            ["E", "X", "Y", "L", "P", "C", "Y", "W", "V", "A", "L"],
            ["E", "J", "V", "Q", "B", "J", "X", "I", "C", "G", "F"],
            ["E", "S", "T", "O", "R", "N", "U", "D", "O", "N", "U"],
            ["U", "D", "N", "W", "Z", "M", "D", "O", "R", "U", "T"],
            ["Y", "R", "S", "E", "Ñ", "A", "Ñ", "C", "R", "S", "B"],
            ["L", "O", "Y", "H", "L", "T", "D", "O", "I", "M", "O"],
            ["E", "X", "V", "P", "H", "E", "Y", "N", "E", "A", "L"],
            ["Q", "V", "X", "U", "H", "R", "V", "A", "N", "S", "X"],
            ["C", "I", "N", "T", "A", "A", "C", "I", "T", "J", "K"],
            ["B", "X", "K", "X", "G", "O", "P", "P", "E", "E", "S"]]

    word_1 = "ESTORNUDO"
    word_2 = "MATERA"
    word_3 = "PIANO"

    placement_1 = {
        "row": 3,
        "col": 0,
        "orientation": Orientation.HORIZONTAL
    }
    placement_2 = {
        "row": 4,
        "col": 5,
        "orientation": Orientation.VERTICAL
    }
    placement_3 = {
        "row": 6,
        "col": 7,
        "orientation": Orientation.VERTICAL_REVERSED
    }

    assert(find_word_placement(word_1, soup) == placement_1)
    assert(find_word_placement(word_2, soup) == placement_2)
    assert(find_word_placement(word_3, soup) == placement_3)


def test_find_first_letter_candidates():
    soup = [["P", "A", "E", "N", "J", "Y", "U", "K", "I", "F", "C"],
            ["E", "X", "Y", "L", "P", "C", "Y", "W", "V", "A", "L"],
            ["E", "J", "V", "Q", "B", "J", "X", "I", "C", "G", "F"],
            ["E", "S", "T", "O", "R", "N", "U", "D", "O", "N", "U"],
            ["U", "D", "N", "W", "Z", "M", "D", "O", "R", "U", "T"],
            ["Y", "R", "S", "E", "Ñ", "A", "Ñ", "C", "R", "S", "B"],
            ["L", "O", "Y", "H", "L", "T", "D", "O", "I", "M", "O"],
            ["E", "X", "V", "P", "H", "E", "Y", "N", "E", "A", "L"],
            ["Q", "V", "X", "U", "H", "R", "V", "A", "N", "S", "X"],
            ["C", "I", "N", "T", "A", "A", "C", "I", "T", "J", "K"],
            ["B", "X", "K", "X", "G", "O", "P", "P", "E", "E", "S"]]

    word_1 = "ESTORNUDO"
    word_2 = "MATERA"
    word_3 = "PIANO"

    candidates_1 = [(1, 0), (2, 0), (3, 0), (7, 0), (0, 2),
                    (5, 3), (7, 5), (7, 8), (10, 8), (10, 9)]
    candidates_2 = [(4, 5), (6, 9)]
    candidates_3 = [(0, 0), (7, 3), (1, 4), (10, 6), (10, 7)]

    assert(find_first_letter_candidates(word_1, soup) == candidates_1)
    assert(find_first_letter_candidates(word_2, soup) == candidates_2)
    assert(find_first_letter_candidates(word_3, soup) == candidates_3)


def test_parse_soups():
    filename = "text_sopas"
    f = open(filename, "r")

    wordlist = ["ESTO", "ES", "UN", "EJEMPLO",
                "PARA", "PROBAR", "LA", "FUNCION"]
    soup = [["I", "Ñ", "H", "Z", "T", "G", "Y", "H", "U", "O"],
            ["B", "M", "P", "E", "J", "E", "M", "P", "L", "O"],
            ["T", "Y", "E", "F", "B", "C", "Y", "E", "D", "C"],
            ["C", "E", "F", "U", "N", "C", "I", "O", "N", "X"],
            ["P", "B", "O", "T", "S", "E", "B", "M", "Q", "L"],
            ["N", "U", "M", "V", "B", "N", "P", "S", "B", "A"],
            ["E", "T", "U", "I", "W", "V", "I", "Q", "L", "M"],
            ["D", "Y", "P", "A", "R", "A", "B", "O", "R", "P"],
            ["V", "U", "E", "S", "E", "I", "T", "E", "R", "B"],
            ["H", "S", "M", "T", "V", "H", "H", "V", "P", "W"]]

    assert(parse_soups(f) == [(soup, wordlist)])

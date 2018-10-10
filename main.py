import re
from enum import Enum, unique
from random import choice, randint, random, shuffle

DEBUG = False


def log(message):
    if DEBUG:
        print(message)


# TODO: Valido el uso
@unique
class Orientation(Enum):
    HORIZONTAL = 1
    HORIZONTAL_REVERSED = 2
    VERTICAL = 3
    VERTICAL_REVERSED = 4
    DIAGONAL = 5


# Representamos listas de palabras con listas de strings
# get_wordlist_input: -> list(str)
# Recibe una string con palabras separadas por espacios. Si es válida, elimina
# los duplicados, transforma a mayúsculas las palabras y las devuelve en una
# lista. Si no lo es, advierte la string es inválida y vuelve al inicio.
def get_wordlist_input():
    while True:
        wordlist = input("Enter words separated by a space: ").split(" ")
        # TODO: preguntar si es necesario
        wordlist = set(wordlist)  # elimina duplicados
        wordlist = [word.upper() for word in wordlist]  # a mayúsculas

        if is_wordlist_valid(wordlist):
            return wordlist
        else:
            print("Invalid input.")


# Representamos listas de palabras con listas de strings
# is_wordlist_valid: list(str) -> bool
# Recibe una lista de palabras y retorna True si todas coinciden con
# WORD_PATTERN o False en caso contrario.
def is_wordlist_valid(wordlist):
    # Coincide con strings con más de un caracter que solo contienen letras del
    # abecedario español.
    # TODO: preguntar si se puede usar
    WORD_PATTERN = re.compile("^[A-ZÑ]{2,}$")
    return all([WORD_PATTERN.match(word) for word in wordlist])


# Representamos la sopa de letras con una matriz (lista de listas de strings)
# create_soup: list(str) -> list(list(str))
# Recibe una lista de palabras y devuelve una sopa de letras que tiene las
# palabras recibidas.
def create_soup(wordlist):
    size = calculate_soup_size(wordlist)
    word_placements = generate_word_placements(wordlist, size)
    soup_matrix = create_soup_matrix(size, word_placements)

    return soup_matrix


# calculate_soup_size: list(str) -> int
# Recibe una lista de palabras y devuelve el tamaño que se debe usar para
# generar la sopa de letras.
# El calculo realizado es: TODO:
def calculate_soup_size(wordlist):
    # print("Calculating soup size")
    c = 2
    max_len_word = max([len(word) for word in wordlist])
    max_size = max(max_len_word, len(wordlist)) + c
    return max_size


# Representamos
# generate_word_placements: list(str) int -> TODO: preguntar como es
# Recibe lalista de palabras a esconder y el tamaño de la sopa de letras y
# devuelve un diccionario con las palabras, su posicion y direccion.
def generate_word_placements(wordlist, size):
    # print("Generating word placements")

    word_placements = {}
    current_word_index = 0

    while current_word_index != len(wordlist):
        word = wordlist[current_word_index]
        # print(f"Current word: {word}")
        placement = try_to_place(word, word_placements, size)
        if placement:
            current_word_index += 1
            word_placements[word] = placement
        else:
            current_word_index = max(0, current_word_index - 1)
            if wordlist[current_word_index] in word_placements:
                del word_placements[wordlist[current_word_index]]

    return word_placements


# Representamos un placement con un dict<str>(int / Orientation):
# placement =  {
#   "row": int,
#   "col": int
#   "orientation": string,
# }
# try_to_place: string dict int -> placement

def try_to_place(word, word_placements, size):
    possible_orientations = list(Orientation)
    possible_positions = [(row, col)
                          for col in range(size)
                          for row in range(size)]

    shuffle(possible_orientations)
    shuffle(possible_positions)
    for row, col in possible_positions:
        for orientation in possible_orientations:
            placement = {
                "row": row,
                "col": col,
                "orientation": orientation
            }
            # print("Trying placement: ", placement)
            if is_placement_valid(word, placement, word_placements, size):
                # print("Valid!")
                return placement

    return False


def is_placement_valid(word, placement, word_placements, size):
    row = placement["row"]
    col = placement["col"]
    orientation = placement["orientation"]

    if (orientation in [Orientation.HORIZONTAL,
                        Orientation.HORIZONTAL_REVERSED,
                        Orientation.DIAGONAL]):
        if col + len(word) > size:
            return False

    if (orientation in [Orientation.VERTICAL,
                        Orientation.VERTICAL_REVERSED,
                        Orientation.DIAGONAL]):
        if row + len(word) > size:
            return False

    letter_positions = get_letter_positions(word, placement)
    for _word, _placement in word_placements.items():
        other_positions = get_letter_positions(_word, _placement)

        for position, letter in letter_positions.items():
            if (position in other_positions and
                    other_positions[position] != letter):
                return False
    return True


def get_letter_positions(word, placement):
        row = placement["row"]
        col = placement["col"]
        orientation = placement["orientation"]

        if (orientation in [Orientation.HORIZONTAL_REVERSED,
                            Orientation.VERTICAL_REVERSED]):
            word = reversed(word)

        letter_positions = {}
        for i, letter in enumerate(word):
            if (orientation in [Orientation.HORIZONTAL,
                                Orientation.HORIZONTAL_REVERSED]):
                letter_positions[(row, col+i)] = letter

            elif (orientation in [Orientation.VERTICAL,
                                  Orientation.VERTICAL_REVERSED]):
                letter_positions[(row+i, col)] = letter

            elif orientation == Orientation.DIAGONAL:
                letter_positions[(row+i, col+i)] = letter

            else:
                raise NotImplementedError

        return letter_positions


# Representamos sopa de letras con una lista de listas de strings
# create_soup_matrix: int dict -> list(list(str))
# Recibe el tamaño de la sopa de letras y un diccionario con las palabras y sus
# posiciones y crea una sopa de letras
def create_soup_matrix(size, word_placements):
    soup_matrix = [['-' for j in range(size)] for i in range(size)]

    for word, placement in word_placements.items():
        row = placement["row"]
        col = placement["col"]
        orientation = placement["orientation"]

        if (orientation in [Orientation.HORIZONTAL_REVERSED,
                            Orientation.VERTICAL_REVERSED]):
            word = reversed(word)

        for i, letter in enumerate(word):
            if (orientation in [Orientation.HORIZONTAL,
                                Orientation.HORIZONTAL_REVERSED]):
                soup_matrix[row][col+i] = letter
            elif (orientation in [Orientation.VERTICAL,
                                  Orientation.VERTICAL_REVERSED]):
                soup_matrix[row+i][col] = letter
            elif orientation == Orientation.DIAGONAL:
                soup_matrix[row+i][col+i] = letter
            else:
                raise NotImplementedError

    return soup_matrix


def display_soup(soup_matrix):
    print("\n".join([" ".join(row) for row in soup_matrix]))

# TODO: Preguntar si es válido inglés
if __name__ == "__main__":
    # 1) Generar sopa de letras
    # wordlist = get_wordlist_input()
    words = ["this", "is", "as", "big", "car", "love", "red", "blue", "dark", "grey", "cool", "dark", "sos", "whale", "time", "casa", "epe", "trial", "fire"]
    for i in range(10000):
        wordlist = list(set(choice(words) for _ in range(8)))
        print(i+1, wordlist)
        soup = create_soup(wordlist)
        display_soup(soup)
    print("Finished!")

    # 2) Resolver sopa de letras

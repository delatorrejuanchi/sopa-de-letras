#!usr/bin/python3
#-- coding: utf-8 --

import re
from enum import Enum
from random import choice, randint, random, shuffle
from termcolor import colored


DEBUG = False

# Representamos una sopa de letras como:
# sopa_de_letras: list(list(str))
# Por ejemplo:
# [["a", "b", "x", "s", "w"],
# [["s", "a", "o", "s", "u"],
# [["t", "r", "v", "c", "t"],
# [["e", "c", "n", "s", "a"],
# [["p", "o", "e", "i", "r"]]

# Representamos un diccionario de word_placements como:
# word_placements: dict<str>(placement)
# Por ejemplo:
# {
#   "word_1": placement, -----------> placement de la palabra 1
#   "word_2": placement, -----------> placement de la palabra 2
#   ...
#   "word_n": placement ------------> placement de la palabra n
# }

# Representamos un placement de una palabra como:
# placement: dict<str>(int / Orientation)
# Por ejemplo:
# placement =  {
#   "row": int, -----------------> fila donde comienza la palabra
#   "col": int, -----------------> columna donde comienza la palabra
#   "orientation": Orientation --> tipo de orientación de la palabra
# }


# Representamos las 5 orientaciones con números:
# Orientation.HORIZONTAL = 1
# Orientation.HORIZONTAL_REVERSED = 5
# Orientation.VERTICAL = 5
# Orientation.VERTICAL_REVERSED = 5
# Orientation.DIAGONAL = 5
class Orientation(Enum):
    HORIZONTAL = 1
    HORIZONTAL_REVERSED = 2
    VERTICAL = 3
    VERTICAL_REVERSED = 4
    DIAGONAL = 5


# get_wordlist_input: -> list(str)
# Pide como input una string con palabras separadas por espacios. Si es
# válida, elimina los duplicados, transforma a mayúsculas las palabras y las
# devuelve en una lista. Si no lo es, advierte que la string es inválida y
# vuelve a pedirla.
def get_wordlist_input():
    while True:
        words = input("Ingresa las palabras separadas por espacios: ")
        wordlist = words.split(" ")  # crea una lista con las palabras
        wordlist = set(wordlist)  # elimina duplicados
        wordlist = [word.upper() for word in wordlist]  # a mayúsculas

        if is_wordlist_valid(wordlist):
            return wordlist
        else:
            print(colored("Input inválido", color="red"))


# is_wordlist_valid: list(str) -> bool
# Recibe una lista de palabras y retorna True si todas coinciden con
# WORD_PATTERN o False en caso contrario.
def is_wordlist_valid(wordlist):
    # Coincide con strings con más de un caracter que solo contienen letras del
    # abecedario español.
    WORD_PATTERN = re.compile("^[A-ZÑ]{2,}$")

    return all([WORD_PATTERN.match(word) for word in wordlist])


# generate_soup: list(str) -> sopa_de_letras
# Recibe una lista de palabras y devuelve una sopa de letras con ellas.
def generate_soup(wordlist):
    size = calculate_soup_size(wordlist)
    word_placements = generate_word_placements(wordlist, size)
    soup_matrix = create_soup_matrix(size, word_placements)

    if DEBUG:
        display_soup(soup_matrix, word_placements)
    else:
        display_soup(soup_matrix)
    return soup_matrix


# calculate_soup_size: list(str) -> int
# Recibe una lista de palabras y devuelve el tamaño que se debe usar para
# generar la sopa de letras. Tiene en cuenta la longitud de la palabra más
# larga, la cantidad de palabras recibidas y un paddong extra (2).
def calculate_soup_size(wordlist):
    return max([len(word) for word in wordlist] + [len(wordlist)]) + 2


# generate_word_placements: list(str) int -> word_placements
# Recibe una lista de palabras y el tamaño de la sopa de letras, genera para
# cada palabra un placement al azar y los devuelve en un diccionario de
# word_placements.
def generate_word_placements(wordlist, size):  # TODO: improve
    word_placements = {}
    current_word_index = 0

    while current_word_index != len(wordlist):
        word = wordlist[current_word_index]
        placement = try_to_place(word, word_placements, size)
        if placement:
            current_word_index += 1
            word_placements[word] = placement
        else:
            current_word_index = max(0, current_word_index - 1)
            if wordlist[current_word_index] in word_placements:
                del word_placements[wordlist[current_word_index]]

    return word_placements


# try_to_place: string word_placements int -> placement / bool
# Recibe una palabra, un diccionario de word_placements y el tamaño de la sopa
# de letras. Devuelve un placement para la palabra si existe uno posible, y
# False en caso contrario.
def try_to_place(word, word_placements, size):
    possible_orientations = list(Orientation)
    possible_positions = [(row, col)
                          for col in range(size) for row in range(size)]

    shuffle(possible_orientations)
    shuffle(possible_positions)
    for row, col in possible_positions:
        for orientation in possible_orientations:
            placement = {
                "row": row,
                "col": col,
                "orientation": orientation
            }
            if is_placement_valid(word, placement, word_placements, size):
                return placement

    return False


# is_placement_valid: str placement word_placements int -> bool
# Recibe una palabra, un posible placement para la misma, un diccionario de
# word_placements con las palabras ya ubicadas, y el tamaño de la sopa de
# letras.
# Devuelve True si el placement es válido, False en caso contrario.
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


# get_letter_positions: str placement -> letter_positions
# Recibe una palabra y el placement de la misma, devuelve un diccionario donde
# las keys son las ubicaciones de cada letra de la palabra, y los values son
# cada letra.
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


# create_soup_matrix: int word_placements -> sopa_de_letras
# Recibe el tamaño de la sopa de letras y un diccionario de word_placements,
# y devuelve una sopa de letras usando el diccionario de word_placements.
def create_soup_matrix(size, word_placements):
    soup_matrix = [[random_letter() for j in range(size)] for i in range(size)]

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


# random_letter -> str
# Devuelve una letra mayúscula al azar del abecedario español.
def random_letter():
    return choice(list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"))


# display_soup: sopa_de_letras (word_placements) -> None
# Recibe una sopa de letras y un diccionario de word_placements opcional,
# y la muestra. Si recibe el diccionario de word_placements, colorea las
# palabras para que sea más fácil visualizar la sopa.
def display_soup(soup_matrix, word_placements=None):
    if word_placements:
        soup_matrix = color_soup(soup_matrix, word_placements)
    print("")
    print("\n".join([" ".join(row) for row in soup_matrix]))
    print("")


# color_soup: sopa_de_letra word_placementes -> sopa_de_letras
# Recibe una sopa_de_letras y un diccionario de word_placements, devuelve
# una sopa_de_letras en la que las letras de cada palabra son verdes.
def color_soup(soup_matrix, word_placements):
    for word, placement in word_placements.items():
        row = placement["row"]
        col = placement["col"]
        orientation = placement["orientation"]

        if orientation == Orientation.HORIZONTAL:
            for i in range(len(word)):
                soup_matrix[row][col+i] = colored(word[i], color="green")

        if orientation == Orientation.HORIZONTAL_REVERSED:
            word = word[::-1]
            for i in range(len(word)):
                soup_matrix[row][col+i] = colored(word[i], color="green")

        if orientation == Orientation.VERTICAL:
            for i in range(len(word)):
                soup_matrix[row+i][col] = colored(word[i], color="green")

        if orientation == Orientation.VERTICAL_REVERSED:
            word = word[::-1]
            for i in range(len(word)):
                soup_matrix[row+i][col] = colored(word[i], color="green")

        if orientation == Orientation.DIAGONAL:
            for i in range(len(word)):
                soup_matrix[row+i][col+i] = colored(word[i], color="green")

    return soup_matrix


# solve_soup: sopa_de_letras list(str) -> word_placements
# Recibe una sopa_de_letras y una lista de palabras. La resuelve, la muestra
# y devuelve un diccionario de word_placements con los placements de las
# palabras de la wordlist. Si alguna de las palabras no fue encontrada, avisa
# al usuario.
def solve_soup(soup, wordlist):
    word_placements = {word: find_word_placement(word, soup)
                       for word in wordlist}

    for word, placement in word_placements.items():
        if placement is None:
            del word_placements[word]
            print(colored(f"No se encontró la palabra: {word}"))

    soup = color_soup(soup, word_placements)
    display_soup(soup, word_placements)
    return word_placements


# find_word_placement: str sopa_de_letras -> placement / None
# Recibe una palabra y una sopa_de_letras, busca la palabra y devuelve su
# placement en la sopa. Si no la encuentra, devuelve None.
def find_word_placement(word, soup):
    size = len(soup)

    candidates = find_first_letter_candidates(word, soup)
    for position in candidates:
        row = position[0]
        col = position[1]

        if col + len(word) <= size:
            match = "".join([soup[row][col+i] for i in range(len(word))])
            if word == match:
                return {
                    "row": row,
                    "col": col,
                    "orientation": Orientation.HORIZONTAL
                }

        if col - len(word) + 1 >= 0:
            match = "".join([soup[row][col-i] for i in range(len(word))])
            if word == match:
                return {
                    "row": row,
                    "col": col - len(word) + 1,
                    "orientation": Orientation.HORIZONTAL_REVERSED
                }

        if row + len(word) <= size:
            match = "".join([soup[row+i][col] for i in range(len(word))])
            if word == match:
                return {
                    "row": row,
                    "col": col,
                    "orientation": Orientation.VERTICAL
                }

        if row - len(word) + 1 >= 0:
            match = "".join([soup[row-i][col] for i in range(len(word))])
            if word == match:
                return {
                    "row": row - len(word) + 1,
                    "col": col,
                    "orientation": Orientation.VERTICAL_REVERSED
                }

        if row + len(word) <= size and col + len(word) <= size:
            match = "".join([soup[row+i][col+i] for i in range(len(word))])
            if word == match:
                return {
                    "row": row,
                    "col": col,
                    "orientation": Orientation.DIAGONAL
                }


# find_first_letter_candidates: str sopa_de_letras -> list(tuple(int, int))
# Recibe una palabra y una sopa_de_letras, devuelve una lista de las posiciones
# que contienen la primera letra de la palabra.
def find_first_letter_candidates(word, soup):
    return [(row, col)
            for col in range(len(soup)) for row in range(len(soup))
            if word[0] == soup[row][col]]


# parse_soups: file -> list(tuple(sopa_de_letras, list(str)))
# Recibe un archivo, devuelve una lista con tuplas de sopa_de_letras y lista
# de palabras.
def parse_soups(f):
    soups = []
    wordlists = []

    reading_soup = False
    current_soup = []
    current_wordlist = []
    for line in f.readlines():
        line = line.strip("\n")
        if line == "# INICIO":
            reading_soup = True
        elif line == "# FIN":
            reading_soup = False
            soups.append(current_soup)
            wordlists.append(current_wordlist)
            current_soup = []
            current_wordlist = []

        elif reading_soup:
            if (len(current_soup) == 0 or
                    len(current_soup) < len(current_soup[0])):
                current_soup.append(line.split(" "))
            else:
                current_wordlist = line.split(" ")

    return list(zip(soups, wordlists))

if __name__ == "__main__":
    print("Trabajo Práctico: sopa-de-letras")
    print("Integrantes: Bautista Marelli y Juan Cruz de La Torre")

    done = False
    while not done:
        print("")
        print("Selecciona una opción:")
        print("1) Generar sopa de letras")
        print("2) Generar N sopas de letras")
        print("3) Resolver sopa de letras")
        print("4) Activar/Desactivar modo depuración")
        print("5) Salir")

        option = input(">>> ")
        if option == "1":
            wordlist = get_wordlist_input()
            generate_soup(wordlist)
        elif option == "2":
            try:
                N = int(input("N: "))
                wordlist = get_wordlist_input()
                for _ in range(N):
                    generate_soup(wordlist)
            except ValueError:
                print(colored("El valor no es un número", color="red"))
        elif option == "3":
            filename = input("Ingresa el nombre del archivo: ")
            try:
                with open(filename, "r") as f:
                    soups = parse_soups(f)
                    for soup, wordlist in soups:
                        solve_soup(soup, wordlist)
            except FileNotFoundError:
                print(colored("El archivo no existe", color="red"))
        elif option == "4":
            DEBUG = not DEBUG
            print(f"Modo depuración: {'Activado' if DEBUG else 'Desactivado'}")
        elif option == "5":
            done = True
        else:
            print(colored("Opción inválida", color="red"))

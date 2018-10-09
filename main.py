import re
from enum import Enum, unique
from random import choice, randint, random
from termcolor import colored

DEBUG_MODE = True


@unique
class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3


class WordSoup:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.board = []
        self.word_placements = {}
        self.generate_placements()
        self.generate_empty_board()
        self.fill_board()

    def generate_placements(self):
        for word in wordlist:
            self.place_random(word)
        if DEBUG_MODE:
            print(self.word_placements)

    def generate_empty_board(self):
        size = self.get_current_size()
        self.board = [['-' for j in range(size)] for i in range(size)]

    def fill_board(self):
        for word, placement in self.word_placements.items():
            for i, letter in enumerate(word):
                if placement["orientation"] == Orientation.HORIZONTAL:
                    self.board[placement["row"]][placement["col"]+i] = letter
                elif placement["orientation"] == Orientation.VERTICAL:
                    self.board[placement["row"]+i][placement["col"]] = letter
                elif placement["orientation"] == Orientation.DIAGONAL:
                    self.board[placement["row"]+i][placement["col"]+i] = letter
                else:
                    raise NotImplementedError

    def place_random(self, word):
        current_size = self.get_current_size()
        while True:
            size = current_size
            if random() <= 0.2:
                size -= len(word)
            self.word_placements[word] = {
                "row": randint(0, size),
                "col": randint(0, size),
                "orientation": choice(list(Orientation)),
            } 

    def get_current_size(self):
        candidates = [max(map(len, self.wordlist))]
        for word, placement in self.word_placements.items():
            if placement["orientation"] == Orientation.HORIZONTAL:
                candidates.append(placement["col"] + len(word))
            elif placement["orientation"] == Orientation.VERTICAL:
                candidates.append(placement["row"] + len(word))
            elif placement["orientation"] == Orientation.DIAGONAL:
                max_diagonal = max(placement["row"], placement["col"])
                candidates.append(max_diagonal + len(word))
            else:
                raise NotImplementedError
        return max(candidates)

    def __str__(self):
        board_str = ''
        for row in self.board:
            board_str += ' '.join(row)
            board_str += "\n"
        return board_str


def get_wordlist_input():
    valid_word_pattern = re.compile("^[A-ZÑ]{2,}$")
    while True:
        wordlist = input("Enter words separated by a dash (-): ").split("-")
        wordlist = set([word.upper().replace(' ', '') for word in wordlist])
        if all(map(lambda word: valid_word_pattern.match(word), wordlist)):
            break
        else:
            print(colored("Invalid input.", "red"))
    return wordlist

if __name__ == "__main__":
    wordlist = get_wordlist_input()
    if DEBUG_MODE:
        for index, word in enumerate(wordlist):
            print("{0}) {1}".format(index, word))

    soup = WordSoup(wordlist)
    print(soup)

class WordSoup:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.word_placements = {}
        self.board = []

        self.generate_word_placements()
        self.generate_empty_board()
        self.fill_board()

    def generate_word_placements(self):
        for word in self.wordlist:
            self.word_placements[word] = self.generate_placement(word)

    def generate_placement(self, word):
        num_iters = 0
        while True:
            num_iters += 1
            if num_iters > 100:
                print(num_iters)
                print("Well")

            placement = {
                "position": self.generate_random_position(word),
                "orientation": choice(list(Orientation)),
            }

            if self.is_placement_valid(word, placement):
                return placement

    def is_placement_valid(self, word, placement):
        letter_positions = self.get_letter_positions(word, placement)
        for _word, _placement in self.word_placements.items():
            other_positions = self.get_letter_positions(_word, _placement)

            for position, letter in letter_positions.items():
                if (position in other_positions and
                        other_positions[position] != letter):
                    return False
        return True

    def get_letter_positions(self, word, placement):
        row = placement["position"]["row"]
        col = placement["position"]["col"]
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

    def generate_random_position(self, word):
        current_size = self.get_current_size()
        # if random() <= extend_rate:
        #     current_size += 2

        return {
            "row": randint(0, current_size-1),
            "col": randint(0, current_size-1)
        }

    def generate_empty_board(self):
        size = self.get_current_size()
        self.board = [['-' for j in range(size)] for i in range(size)]

    def fill_board(self):
        for word, placement in self.word_placements.items():
            row = placement["position"]["row"]
            col = placement["position"]["col"]
            orientation = placement["orientation"]

            if (orientation in [Orientation.HORIZONTAL_REVERSED,
                                Orientation.VERTICAL_REVERSED]):
                word = reversed(word)

            for i, letter in enumerate(word):
                if (orientation in [Orientation.HORIZONTAL,
                                    Orientation.HORIZONTAL_REVERSED]):
                    self.board[row][col+i] = letter
                elif (orientation in [Orientation.VERTICAL,
                                      Orientation.VERTICAL_REVERSED]):
                    self.board[row+i][col] = letter
                elif orientation == Orientation.DIAGONAL:
                    self.board[row+i][col+i] = letter
                else:
                    raise NotImplementedError

    # def checkIntersection(self):
    #     lista_de_cordenadas = []
    #     for word, placement in self.word_placements.items():
    #         if placement["orientation"] == Orientation.HORIZONTAL:
    #             cordenadas = []
    #             for i in range(len(word)):
    #                 cordenadas.append((placement["row"], placement["col"]+i))
    #             lista_de_cordenadas.append(cordenadas)
    #         elif placement["orientation"] == Orientation.VERTICAL:
    #             cordenadas = []
    #             for i in range(len(word)):
    #                 cordenadas.append((placement["row"]+i, placement["col"]))
    #             lista_de_cordenadas.append(cordenadas)
    #         elif placement["orientation"] == Orientation.HORIZONTAL:
    #             cordenadas = []
    #             for i in range(len(word)):
    #                 cordenadas.append((placement["row"]+i, placement["col"]+i))
    #             lista_de_cordenadas.append(cordenadas)
    #     return lista_de_cordenadas

    def get_current_size(self):
        candidates = [max(map(len, self.wordlist))]
        for word, placement in self.word_placements.items():
            row = placement["position"]["row"]
            col = placement["position"]["col"]
            orientation = placement["orientation"]

            if (orientation in [Orientation.HORIZONTAL,
                                Orientation.HORIZONTAL_REVERSED]):
                candidates.append(col + len(word))
                candidates.append(row + 1)

            elif (orientation in [Orientation.VERTICAL,
                                  Orientation.VERTICAL_REVERSED]):
                candidates.append(row + len(word))
                candidates.append(col + 1)

            elif orientation == Orientation.DIAGONAL:
                candidates.append(max(row, col) + len(word))

            else:
                raise NotImplementedError
        return max(candidates)

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])

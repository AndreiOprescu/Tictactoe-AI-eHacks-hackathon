from random import choice


class ImpossibleAI:
    def __init__(self, squares, winning_formations, first):
        self.squares = squares
        self.winning_formations = winning_formations
        self.first = first
        self.first_edge_placed = False

        if self.first:
            self.player_symbol, self.opponent_symbol = "x", "o"
        else:
            self.player_symbol, self.opponent_symbol = "o", "x"

        self.corners = [squares[0][0], squares[0][2], squares[2][0], squares[2][2]]
        self.edges = [squares[0][1], squares[1][0], squares[1][2], squares[2][1]]

        self.first_square = None
        self.corner_between = None

    def next_move_first(self):
        if self.step == 1:
            # Mark random corner
            return self.random_corner

        if self.step == 2:
            # Mark opposite corner
            if self.opponent_possible_formation[0]:
                return self.opponent_possible_formation[1]
            else:
                if self.opposite_corner(self.first_square)['text'] == '':
                    return self.opposite_corner(self.first_square)
                else:
                    return self.random_corner

        if self.step == 3:
            # Place corner in between
            if self.ai_possible_formation[0]:
                return self.ai_possible_formation[1]
            elif self.opponent_possible_formation[0]:
                return self.opponent_possible_formation[1]
            else:
                if self.corner_available[0]:
                    return self.corner_available[1]
                elif self.edge_available[0]:
                    return self.edge_available[1]

        if self.step == 4:
            # Place logically
            if self.ai_possible_formation[0]:
                return self.ai_possible_formation[1]
            elif self.opponent_possible_formation[0]:
                return self.opponent_possible_formation[1]
            else:
                if self.corner_available[0]:
                    return self.corner_available[1]
                elif self.edge_available[0]:
                    return self.edge_available[1]

        if self.step == 5:
            # Place last square
            return self.last_square

    def next_move_second(self):
        if not self.is_middle_square_marked:
            if self.diagonal_squares_marked and not self.first_edge_placed and self.squares_marked < 5:
                return self.random_edge
            elif self.l_move and not bool(self.corner_between) and self.squares_marked < 5:
                self.corner_between = self.l_move
                return self.l_move
            elif self.ai_possible_formation[0]:
                # Mark winning square
                return self.ai_possible_formation[1]
            elif self.opponent_possible_formation[0]:
                # Block Opponent
                return self.opponent_possible_formation[1]
            else:
                if self.corner_available[0]:
                    return self.corner_available[1]
                elif self.edge_available[0]:
                    return self.edge_available[1]
        else:
            return self.squares[1][1]

    @property
    def next_move(self):
        if self.first:
            return self.next_move_first()
        else:
            return self.next_move_second()

    @property
    def random_corner(self):
        random_corner = choice(self.corners)
        while random_corner['text'] != '':
            random_corner = choice(self.corners)
        self.first_square = random_corner
        return random_corner

    @property
    def random_edge(self):
        random_edge = choice(self.edges)
        while random_edge['text'] != '':
            random_edge = choice(self.edges)
        self.first_square = random_edge
        self.first_edge_placed = True
        return random_edge

    @property
    def step(self):
        squares_placed = 0
        for _set in self.squares:
            for square in _set:
                if square['text'] == self.player_symbol:
                    squares_placed += 1
        return squares_placed + 1

    def opposite_corner(self, corner):
        if corner == self.corners[0]:
            return self.corners[3]
        elif corner == self.corners[1]:
            return self.corners[2]
        elif corner == self.corners[2]:
            return self.corners[1]
        elif corner == self.corners[3]:
            return self.corners[0]

    @property
    def last_square(self):
        for _set in self.squares:
            for square in _set:
                if square['text'] == '':
                    return square

    @property
    def opponent_possible_formation(self):
        # For every formation in winning formations...
        if (self.squares[1][2]['text'] == self.opponent_symbol) & \
                (self.squares[2][1]['text'] == self.opponent_symbol) & \
                (self.squares[2][2]['text'] != self.player_symbol):
            return True, self.squares[2][2]
        for formation in self.winning_formations:
            # If the opponent can win...
            opponent_marks = 0
            total_marked = 0
            for square in formation:
                if square['text'] == self.opponent_symbol:
                    opponent_marks += 1
                total_marked += 1
            if opponent_marks == 2 & total_marked != 3:
                for square in formation:
                    if square['text'] == "":
                        return True, square
                        # Return True and square
        # Else, return False
        return False, 0

    @property
    def ai_possible_formation(self):
        # For every formation in winning formations...
        for formation in self.winning_formations:
            # If AI can win...
            AI_marks = 0
            total_marked = 0
            for square in formation:
                if square['text'] == self.player_symbol:
                    AI_marks += 1
                total_marked += 1
            if AI_marks == 2 & total_marked != 3:
                for square in formation:
                    if square['text'] == "":
                        return True, square
                        # Return True and square
        # Else, return False
        return False, 0

    @property
    def corner_available(self):
        for corner in self.corners:
            if corner['text'] == "":
                return True, corner
        return False, 0

    @property
    def edge_available(self):
        for edge in self.edges:
            if edge['text'] == "":
                return True, edge
        return False, 0

    @property
    def is_middle_square_marked(self):
        # If middle square is marked
        if self.squares[1][1]['text'] == "":
            # Return True
            return True
        # Return False
        return False

    @property
    def diagonal_squares_marked(self):
        if (self.corners[0]['text'] == self.opposite_corner(self.corners[0])['text'] == self.opponent_symbol) or \
                (self.corners[1]['text'] == self.opposite_corner(self.corners[1])['text'] == self.opponent_symbol):
            return True

    @property
    def l_move(self):
        corner_between = None
        if self.corners[0]['text'] == self.edges[2]['text'] == self.opponent_symbol:
            corner_between = self.corners[1]
        if self.corners[0]['text'] == self.edges[3]['text'] == self.opponent_symbol:
            corner_between = self.corners[2]
        if self.corners[1]['text'] == self.edges[1]['text'] == self.opponent_symbol:
            corner_between = self.corners[0]
        if self.corners[1]['text'] == self.edges[3]['text'] == self.opponent_symbol:
            corner_between = self.corners[3]
        if self.corners[2]['text'] == self.edges[0]['text'] == self.opponent_symbol:
            corner_between = self.corners[0]
        if self.corners[2]['text'] == self.edges[2]['text'] == self.opponent_symbol:
            corner_between = self.corners[3]
        if self.corners[3]['text'] == self.edges[0]['text'] == self.opponent_symbol:
            corner_between = self.corners[1]
        if self.corners[3]['text'] == self.edges[1]['text'] == self.opponent_symbol:
            corner_between = self.corners[2]
        return corner_between

    @property
    def squares_marked(self):
        total_marked = 0
        for _set in self.squares:
            for square in _set:
                if square['text'] != '':
                    total_marked += 1
        return total_marked


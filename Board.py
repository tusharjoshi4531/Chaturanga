from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup

from kivy.graphics import *

from kivy.properties import *

from Logic import *

import datetime


class PromotionPopup(Popup):
    promoting_square = ListProperty()
    promotion_piece_color = StringProperty()


class Board(Widget):
    '''Handles the input and logic of the game and loading saved games'''
    square_side_length = NumericProperty(0)
    piece_padding = NumericProperty(0.95)

    pallete = ObjectProperty(None)

    # values: ('game', 'load')
    is_playing = True

    board_matrix = {}

    # format: [board_matrices]
    game = [{}]
    move_number = 1

    # bottom left of every square
    file_to_x = {}
    rank_to_y = {}

    piece_textures = {'white': {'pawn': 'assets/w_pawn_1x.png',
                                'bishop': 'assets/w_bishop_1x.png',
                                'knight': 'assets/w_knight_1x.png',
                                'queen': 'assets/w_queen_1x.png',
                                'king': 'assets/w_king_1x.png',
                                'rook': 'assets/w_rook_1x.png'},
                      'black': {'pawn': 'assets/b_pawn_1x.png',
                                'bishop': 'assets/b_bishop_1x.png',
                                'knight': 'assets/b_knight_1x.png',
                                'queen': 'assets/b_queen_1x.png',
                                'king': 'assets/b_king_1x.png',
                                'rook': 'assets/b_rook_1x.png'}}

    pieces = []

    valid_moves = []

    chosen_square = ()

    turn = 'white'

    result = 'draw'

    legal_move_squares = []
    check = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_info(self):
        '''info needed to save the game'''
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        return date, self.result, self.game

    def set_info(self, name, date, result, game):
        '''info needed to load the game'''
        self.game = game
        self.init_board_load()

        self.pallete.text = f'Name: {name}\nDate: {date}\n'
        if result == 'draw':
            self.pallete.text += 'The game was a draw\n'
        else:
            self.pallete.text += f'Winner: {result}\n'

    def init_board_play(self):
        '''Initialize the board on the screen.
           This function is called just before entering the game screen.
           This function is called in GameScreen.on_pre_enter in main.py'''

        # Sets file_to_x
        for i in 'abcdefgh':
            file = i
            x = self.get_square_pos((file, 1))[0]
            self.file_to_x[file] = x

        # Sets rank_to_y
        for i in range(8):
            rank = i + 1
            y = self.get_square_pos(('a', rank))[1]
            self.rank_to_y[rank] = y

        self.init_board_matrix()
        self.set_pieces()

        self.turn = 'white'
        self.check = False
        self.is_playing = True
        self.pallete.text = ''

    def init_board_load(self):
        '''Initializes the board on the screen when a game is loaded'''
        self.move_number = 1
        self.board_matrix = self.game[self.move_number - 1]
        self.set_pieces()

        self.is_playing = False
        self.pallete.text = ''

    def init_board_matrix(self):
        '''Initialize the board_matrix variable'''
        for i in 'abcdefgh':
            file = i
            for j in range(8):
                rank = j + 1
                self.board_matrix[(file, rank)] = ('none', 'none')

        # Pawns
        for i in 'abcdefgh':
            self.board_matrix[(i, 2)] = ('white', 'pawn')
            self.board_matrix[(i, 7)] = ('black', 'pawn')

        # Rooks
        self.board_matrix[('a', 1)] = ('white', 'rook')
        self.board_matrix[('h', 1)] = ('white', 'rook')
        self.board_matrix[('a', 8)] = ('black', 'rook')
        self.board_matrix[('h', 8)] = ('black', 'rook')

        # Knights
        self.board_matrix[('b', 1)] = ('white', 'knight')
        self.board_matrix[('g', 1)] = ('white', 'knight')
        self.board_matrix[('b', 8)] = ('black', 'knight')
        self.board_matrix[('g', 8)] = ('black', 'knight')

        # Bishop
        self.board_matrix[('c', 1)] = ('white', 'bishop')
        self.board_matrix[('f', 1)] = ('white', 'bishop')
        self.board_matrix[('c', 8)] = ('black', 'bishop')
        self.board_matrix[('f', 8)] = ('black', 'bishop')

        # Queen
        self.board_matrix[('d', 1)] = ('white', 'queen')
        self.board_matrix[('d', 8)] = ('black', 'queen')

        # King
        self.board_matrix[('e', 1)] = ('white', 'king')
        self.board_matrix[('e', 8)] = ('black', 'king')

        # Python dictionaries can form aliases, therefore copy()
        # function is used to prevent aliasing
        self.game = [self.board_matrix.copy()]

    def change_position(self, dir):
        '''Change position of board.
           Called vhen next or previous button in load screen is clicked'''
        self.move_number += dir

        if self.move_number > len(self.game) or self.move_number < 1:
            self.move_number -= dir

        self.board_matrix = self.game[self.move_number - 1]
        self.set_pieces()

    def set_pieces(self):
        '''Puts pieces on board in the screen based on board_matrix'''
        for i in self.pieces:
            self.remove_widget(i)

        self.pieces = []

        # Removes highloghts and pieces from the screen
        self.canvas.clear()

        for i in self.board_matrix.items():
            '''i[0] = (file, rank), i[1] = (color, type)'''
            if i[1][0] != 'none':
                x, y = self.get_square_pos(i[0])
                _color, _type = i[1]

                pos = (x + (1 - self.piece_padding) * self.square_side_length / 2,
                       y + (1 - self.piece_padding) * self.square_side_length / 2)

                size = (self.square_side_length * self.piece_padding,
                        self.square_side_length * self.piece_padding)

                img = Image(source=self.piece_textures[_color][_type], size_hint=(
                    None, None), size=size, pos=pos)

                self.pieces.append(img)
                self.add_widget(img)

    def add_square_highlight(self, square, color):
        '''adds highlight to guven square on the board'''
        file, rank = square

        highlight_size = (self.square_side_length, self.square_side_length)
        highlight_pos = (self.file_to_x[file], self.rank_to_y[rank])

        highlight = Rectangle(pos=highlight_pos, size=highlight_size)

        self.canvas.add(Color(rgba=color))
        self.canvas.add(highlight)

    def get_square_pos(self, square):
        '''Returns the position of bottom left of the input square'''
        file = square[0]
        rank = square[1]

        pos = (self.x + (ord(file) - ord('a')) *
               self.square_side_length, self.y + (rank - 1) * self.square_side_length)

        return pos

    def get_king_square(self):
        '''Returns the square of both the kings in the form of a dictionary'''
        white_king = ()
        black_king = ()

        for i in self.board_matrix.items():

            if i[1] == ('white', 'king'):
                white_king = i[0]
            elif i[1] == ('black', 'king'):
                black_king = i[0]

        return {'white': white_king, 'black': black_king}

    def promote(self, promoting_square, promoted_piece, promoted_piece_color):
        '''Adds promoted piece in board matrix.
           tuple() is used because promoting square in PromotionPopup is a list'''
        self.board_matrix[tuple(promoting_square)] = (
            promoted_piece_color, promoted_piece)

        # Checks
        self.scan_for_check()

        self.set_pieces()

        # update game: if this is not done then promoted piece
        # will be shown as a pawn in load screen
        self.game[-1] = self.board_matrix.copy()

    def resign(self):
        '''Called when resign button is clicked'''
        winner = 'white' if self.turn == 'black' else 'black'
        self.pallete.text += f'{self.turn} resigned'
        self.is_playing = False

        self.result = winner

    def draw(self):
        '''Called when draw button in clicked'''
        self.pallete.text += 'both players agreed to a draw'
        self.is_playing = False

        self.result = 'draw'

    def scan_for_check(self):
        '''To check if there is a check to the king'''
        self.check = in_check(
            self.board_matrix, self.turn, self.get_king_square()[self.turn])[1]

        if self.check:
            '''Restricting inputs in case of a check'''

            # Holds the squares of all the pieces which can stop checks
            legal_move_squares = []

            king_pos = self.get_king_square()[self.turn]

            # Squares whrere the pieces giving check are present
            checking_squares = in_check(
                self.board_matrix, self.turn, king_pos)[0]

            if len(checking_squares) >= 2:
                print('double check')
            else:
                checking_square = checking_squares[0]
                checking_piece = self.board_matrix[checking_square][1]

                opponent_turn = 'white' if self.turn == 'black' else 'black'

                legal_move_squares = in_check(
                    self.board_matrix, opponent_turn, checking_square)[0]

                if checking_piece == 'rook':
                    '''For getting all the moves that can intercept the line of sight of rook'''

                    # Horizontal rook check
                    low = ord(min(checking_square[0], king_pos[0]))
                    high = ord(max(checking_square[0], king_pos[0]))

                    for i in range(low + 1, high):
                        t = in_check(
                            self.board_matrix, opponent_turn, (chr(i), checking_square[1]))[0]

                        for j in t:
                            '''1. Remove pawns from legal_move_squares because in_check considers
                               diagonal moves for pawns but for intercepting, pawns move straight, not diagonally
                               2. Removing king from legal_move_squares because king cannot intercept its own check'''
                            if self.board_matrix[j][1] == 'pawn':
                                t.remove(j)

                            if self.board_matrix[j][1] == 'king':
                                t.remove(j)

                        '''Adding pawns if they can intercept the check'''
                        if self.turn == 'white':
                            if (chr(i), checking_square[1] - 1) in self.board_matrix:
                                if self.board_matrix[(chr(i), checking_square[1] - 1)] == ('white', 'pawn'):
                                    legal_move_squares.append(
                                        (chr(i), checking_square[1] - 1))

                        elif self.turn == 'black':
                            if (chr(i), checking_square[1] + 1) in self.board_matrix:
                                if self.board_matrix[(chr(i), checking_square[1] + 1)] == ('black', 'pawn'):
                                    legal_move_squares.append(
                                        (chr(i), checking_square[1] + 1))

                        legal_move_squares.extend(t)

                    # Vertical rook check
                    low = min(checking_square[1], king_pos[1])
                    high = max(checking_square[1], king_pos[1])

                    for i in range(low + 1, high):
                        t = in_check(
                            self.board_matrix, opponent_turn, (checking_square[0], i))[0]

                        for j in t:
                            '''Remove pawns from legal_move_squares because in_check considers
                               diagonal moves for pawns but for intercepting, pawns move straight, not diagonally'''
                            if self.board_matrix[j][1] == 'pawn':
                                t.remove(j)

                        legal_move_squares.extend(t)

                        # Vertical checks cannot be interceped by pawns

            if king_moves(self.board_matrix, self.turn, king_pos) != []:
                legal_move_squares.append(king_pos)

            if legal_move_squares == []:
                '''If there is a checkmate'''
                self.pallete.text += 'Checkmate\n'

                winner = 'white' if self.turn == 'black' else 'black'
                self.pallete.text += f'{winner} has won'
                self.is_playing = False

                self.result = winner

            self.legal_move_squares = legal_move_squares

    def on_touch_down(self, touch):
        '''Called when mouse is clicked.
           touch: givs information about click like position of the click'''

        if not self.is_playing:
            return

        x, y = touch.pos
        file, rank = None, None

        # Get the file of the click
        for i in self.file_to_x.items():
            if x > i[1] and x < i[1] + self.square_side_length:
                file = i[0]
                break

        # Get the rank of the click
        for i in self.rank_to_y.items():
            if y > i[1] and y < i[1] + self.square_side_length:
                rank = i[0]
                break

        # if click is outside the board
        if file == None or rank == None:
            return

        '''Taking in and handeling input of the user'''

        if self.chosen_square == ():
            '''If user has given input for choosing the piece they want to piece'''

            if self.check:

                if (file, rank) not in self.legal_move_squares:
                    return

            # Getting Valid moves
            self.valid_moves = get_valid_moves(
                self.board_matrix, self.turn, (file, rank))

            if self.valid_moves == []:
                return
            else:
                '''If the chosen piece have legal moves'''
                self.chosen_square = (file, rank)

                # Highlighting legal squares
                for i in self.valid_moves:
                    self.add_square_highlight(i, (0, 0, 1, 0.5))

                # Highlighting chosen square
                self.add_square_highlight(self.chosen_square, (1, 1, 0, 0.5))

                return

        else:
            '''If user has given input for moving the piece they have already chosen'''

            piece = ()
            if (file, rank) in self.valid_moves:
                '''If the square chosen by the user is a valid square(lagal move is made)'''
                piece = self.board_matrix[self.chosen_square]

                self.board_matrix[self.chosen_square] = ('none', 'none')

                self.board_matrix[(file, rank)] = piece

                self.pallete.text += f'{self.chosen_square[0]}{self.chosen_square[1]} to {file}{rank}\n'

                # Changing turns
                self.turn = 'white' if self.turn == 'black' else 'black'

                # Updating game
                self.game.append(self.board_matrix.copy())

            # promotion
            if piece == ('white', 'pawn') and rank == 8:

                popup = PromotionPopup(promoting_square=(
                    file, rank), promotion_piece_color='white')
                popup.open()

            # Checks
            self.scan_for_check()

            self.set_pieces()

            # Resseting important variables
            self.chosen_square = ()
            self.valid_moves = ()

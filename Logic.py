def get_valid_moves(board_matrix, turn, inp):
    color = board_matrix[inp][0]
    piece = board_matrix[inp][1]
    if color == turn:
        if piece == "bishop":
            return bishop_moves(board_matrix, turn, inp)
        if piece == "knight":
            return knight_moves(board_matrix, turn, inp)
        if piece == 'rook':
            return rook_moves(board_matrix, turn, inp)
        if piece == 'queen':
            return queen_moves(board_matrix, turn, inp)
        if piece == 'king':
            return king_moves(board_matrix, turn, inp)
        if piece == 'pawn':
            return pawn_moves(board_matrix, turn, inp)

    else:
        return []


def bishop_moves(board_matrix, turn, inp):
    file = inp[0]
    rank = inp[1]
    valid_moves = []
    if check_square(board_matrix, turn, (chr(ord(file) + 2), rank + 2)) == True:
        valid_moves.append((chr(ord(file) + 2), rank + 2))
    if check_square(board_matrix, turn, (chr(ord(file) + 2), rank - 2)) == True:
        valid_moves.append((chr(ord(file) + 2), rank - 2))
    if check_square(board_matrix, turn, (chr(ord(file) - 2), rank + 2)) == True:
        valid_moves.append((chr(ord(file) - 2), rank + 2))
    if check_square(board_matrix, turn, (chr(ord(file) - 2), rank - 2)) == True:
        valid_moves.append((chr(ord(file) - 2), rank - 2))
    return valid_moves


def knight_moves(board_matrix, turn, inp):
    file = inp[0]
    rank = inp[1]
    valid_moves = []
    if check_square(board_matrix, turn, (chr(ord(file) + 2), rank + 1)) == True:
        valid_moves.append((chr(ord(file) + 2), rank + 1))
    if check_square(board_matrix, turn, (chr(ord(file) + 2), rank - 1)) == True:
        valid_moves.append((chr(ord(file) + 2), rank - 1))
    if check_square(board_matrix, turn, (chr(ord(file) - 2), rank + 1)) == True:
        valid_moves.append((chr(ord(file) - 2), rank + 1))
    if check_square(board_matrix, turn, (chr(ord(file) - 2), rank - 1)) == True:
        valid_moves.append((chr(ord(file) - 2), rank - 1))
    if check_square(board_matrix, turn, (chr(ord(file) + 1), rank + 2)) == True:
        valid_moves.append((chr(ord(file) + 1), rank + 2))
    if check_square(board_matrix, turn, (chr(ord(file) + 1), rank - 2)) == True:
        valid_moves.append((chr(ord(file) + 1), rank - 2))
    if check_square(board_matrix, turn, (chr(ord(file) - 1), rank + 2)) == True:
        valid_moves.append((chr(ord(file) - 1), rank + 2))
    if check_square(board_matrix, turn, (chr(ord(file) - 1), rank - 2)) == True:
        valid_moves.append((chr(ord(file) - 1), rank - 2))
    return valid_moves


def queen_moves(board_matrix, turn, inp):
    file = inp[0]
    rank = inp[1]
    valid_moves = []
    if check_square(board_matrix, turn, (chr(ord(file) + 1), rank + 1)) == True:
        valid_moves.append((chr(ord(file) + 1), rank + 1))
    if check_square(board_matrix, turn, (chr(ord(file) + 1), rank - 1)) == True:
        valid_moves.append((chr(ord(file) + 1), rank - 1))
    if check_square(board_matrix, turn, (chr(ord(file) - 1), rank + 1)) == True:
        valid_moves.append((chr(ord(file) - 1), rank + 1))
    if check_square(board_matrix, turn, (chr(ord(file) - 1), rank - 1)) == True:
        valid_moves.append((chr(ord(file) - 1), rank - 1))
    return valid_moves


def rook_moves(board_matrix, turn, inp):
    file = inp[0]
    rank = inp[1]
    valid_moves = []
    for i in range(rank + 1, 9):
        if check_square(board_matrix, turn, (file, i)) == True:
            valid_moves.append((file, i))
        else:
            break

        if board_matrix[(file, i)][0] != 'none':
            break

    for i in range(rank - 1, 0, -1):
        if check_square(board_matrix, turn, (file, i)) == True:
            valid_moves.append((file, i))
        else:
            break

        if board_matrix[(file, i)][0] != 'none':
            break

    for i in range(ord(file) - 1, ord("a") - 1, -1):
        if check_square(board_matrix, turn, (chr(i), rank)) == True:
            valid_moves.append((chr(i), rank))
        else:
            break

        if board_matrix[(chr(i), rank)][0] != 'none':
            break

    for i in range(ord(file) + 1, ord("h") + 1):
        if check_square(board_matrix, turn, (chr(i), rank)) == True:
            valid_moves.append((chr(i), rank))
        else:
            break

        if board_matrix[(chr(i), rank)][0] != 'none':
            break

    return(valid_moves)


def king_moves(board_matrix, turn, inp):

    lip = normal_king_moves(board_matrix, turn, inp)
    valid_moves = []

    for i in lip:
        if in_check(board_matrix, turn, i)[1] == True:
            continue
        elif in_check(board_matrix, turn, i)[1] == False:
            valid_moves.append(i)
    return valid_moves


def normal_king_moves(board_matrix, turn, inp):
    temp = queen_moves(board_matrix, turn, inp)

    file = inp[0]
    rank = inp[1]

    if check_square(board_matrix, turn, (chr(ord(file) + 1), rank)) == True:
        temp.append((chr(ord(file) + 1), rank))
    if check_square(board_matrix, turn, (chr(ord(file)), rank - 1)) == True:
        temp.append((chr(ord(file)), rank - 1))
    if check_square(board_matrix, turn, (chr(ord(file)), rank + 1)) == True:
        temp.append((chr(ord(file)), rank + 1))
    if check_square(board_matrix, turn, (chr(ord(file) - 1), rank)) == True:
        temp.append((chr(ord(file) - 1), rank))

    return temp


def pawn_moves(board_matrix, turn, inp):
    if turn == 'white':
        return white_pawn_moves(board_matrix, inp)

    if turn == 'black':
        return black_pawn_moves(board_matrix, inp)


def white_pawn_moves(board_matrix, inp):
    rank = inp[1]
    file = inp[0]
    valid_moves = []

    if (file, rank + 1) in board_matrix:
        if board_matrix[(file, rank + 1)] == ("none", "none"):
            valid_moves.append((file, rank + 1))

    if (chr(ord(file) + 1), rank + 1) in board_matrix:
        if board_matrix[(chr(ord(file) + 1), rank + 1)][0] == 'black':
            valid_moves.append((chr(ord(file) + 1), rank + 1))

    if (chr(ord(file) - 1), rank + 1) in board_matrix:
        if board_matrix[(chr(ord(file) - 1), rank + 1)][0] == 'black':
            valid_moves.append((chr(ord(file) - 1), rank + 1))

    return valid_moves


def black_pawn_moves(board_matrix, inp):
    rank = inp[1]
    file = inp[0]
    valid_moves = []

    if (file, rank - 1) in board_matrix:
        if board_matrix[(file, rank - 1)] == ("none", "none"):
            valid_moves.append((file, rank - 1))

    if (chr(ord(file) + 1), rank - 1) in board_matrix:
        if board_matrix[(chr(ord(file) + 1), rank - 1)][0] == 'white':
            valid_moves.append((chr(ord(file) + 1), rank - 1))

    if (chr(ord(file) - 1), rank - 1) in board_matrix:
        if board_matrix[(chr(ord(file) - 1), rank - 1)][0] == 'white':
            valid_moves.append((chr(ord(file) - 1), rank - 1))

    return valid_moves


def check_square(board_matrix, turn, square):
    if square in board_matrix:
        if board_matrix[square][0] == turn:
            return False
        else:
            return True
    else:
        return False


def in_check(board_matrix, turn, square):

    rank = square[1]
    file = square[0]
    checking_squares = []

    rook_board_matrix = {}

    for i in board_matrix:
        if board_matrix[i] == (turn, 'king'):
            rook_board_matrix[i] = ('none', 'none')
        else:
            rook_board_matrix[i] = board_matrix[i]

    l = rook_moves(rook_board_matrix, turn, square)
    for i in l:
        if board_matrix[i][1] == "rook":
            checking_squares.append(i)
        else:
            continue

    l = bishop_moves(board_matrix, turn, square)
    for i in l:
        if board_matrix[i][1] == "bishop":
            checking_squares.append(i)
        else:
            continue

    l = knight_moves(board_matrix, turn, square)
    for i in l:
        if board_matrix[i][1] == "knight":
            checking_squares.append(i)
        else:
            continue

    l = queen_moves(board_matrix, turn, square)
    for i in l:
        if board_matrix[i][1] == "queen":
            checking_squares.append(i)
        else:
            continue

    l = normal_king_moves(board_matrix, turn, square)
    for i in l:
        if board_matrix[i][1] == "king":
            checking_squares.append(i)
        else:
            continue

    if turn == 'white':
        if (chr(ord(file) + 1), rank + 1) in board_matrix:
            if board_matrix[(chr(ord(file) + 1), rank + 1)] == ('black', 'pawn'):
                checking_squares.append((chr(ord(file) + 1), rank + 1))

        if (chr(ord(file) - 1), rank + 1) in board_matrix:
            if board_matrix[(chr(ord(file) - 1), rank + 1)] == ('black', 'pawn'):
                checking_squares.append((chr(ord(file) - 1), rank + 1))

    if turn == 'black':
        if (chr(ord(file) + 1), rank - 1) in board_matrix:
            if board_matrix[(chr(ord(file) + 1), rank - 1)] == ('white', 'pawn'):
                checking_squares.append((chr(ord(file) + 1), rank - 1))

        if (chr(ord(file) - 1), rank - 1) in board_matrix:
            if board_matrix[(chr(ord(file) - 1), rank - 1)] == ('white', 'pawn'):
                checking_squares.append((chr(ord(file) - 1), rank - 1))

    if checking_squares == []:
        return checking_squares, False
    else:
        return checking_squares, True

import cv2

board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]

START_X = 100
START_Y = 100
CELL_SIZE = 100


def draw_board(img):

    # Draw Grid
    for i in range(4):
        cv2.line(
            img,
            (START_X, START_Y + i * CELL_SIZE),
            (START_X + 300, START_Y + i * CELL_SIZE),
            (255, 255, 255),
            3
        )

    for i in range(4):
        cv2.line(
            img,
            (START_X + i * CELL_SIZE, START_Y),
            (START_X + i * CELL_SIZE, START_Y + 300),
            (255, 255, 255),
            3
        )

    # Draw Symbols
    for row in range(3):
        for col in range(3):

            x = START_X + col * CELL_SIZE + 25
            y = START_Y + row * CELL_SIZE + 75

            if board[row][col] == "X":

                cv2.putText(
                    img,
                    "X",
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 255, 0),
                    3
                )

            elif board[row][col] == "O":

                cv2.putText(
                    img,
                    "O",
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0, 0, 255),
                    3
                )


def get_cell(x, y):

    if not (
        START_X <= x <= START_X + 300 and
        START_Y <= y <= START_Y + 300
    ):
        return None

    col = (x - START_X) // CELL_SIZE
    row = (y - START_Y) // CELL_SIZE

    return int(row), int(col)


def check_winner(board_state):

    # Rows
    for row in board_state:
        if row[0] == row[1] == row[2] != "":
            return row[0]

    # Columns
    for col in range(3):
        if (
            board_state[0][col] ==
            board_state[1][col] ==
            board_state[2][col] != ""
        ):
            return board_state[0][col]

    # Main Diagonal
    if (
        board_state[0][0] ==
        board_state[1][1] ==
        board_state[2][2] != ""
    ):
        return board_state[0][0]

    # Anti Diagonal
    if (
        board_state[0][2] ==
        board_state[1][1] ==
        board_state[2][0] != ""
    ):
        return board_state[0][2]

    return None


def is_board_full(board_state):

    for row in board_state:
        for cell in row:

            if cell == "":
                return False

    return True
def get_winning_line(board):

    # Rows
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != "":
            return ("row", r)

    # Columns
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != "":
            return ("col", c)

    # Main diagonal
    if board[0][0] == board[1][1] == board[2][2] != "":
        return ("diag", 0)

    # Anti diagonal
    if board[0][2] == board[1][1] == board[2][0] != "":
        return ("diag", 1)

    return None
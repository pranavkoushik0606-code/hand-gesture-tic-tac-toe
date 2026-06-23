import cv2
import math
import time

from hand_detector import detector
from game import (
    draw_board,
    get_cell,
    board,
    check_winner,
    is_board_full,
    get_winning_line,
)
from ai import ai_move, easy_move, medium_move


cap = cv2.VideoCapture(0)

last_click_time = 0
winner = None
game_over = False
game_started = False

player_score = 0
ai_score = 0
draw_score = 0
score_updated = False

difficulty = "HARD"


def reset_board():
    """Clear the board for a new game."""
    for row in range(3):
        for col in range(3):
            board[row][col] = ""


def draw_start_screen(img):
    """Display the game's start screen."""
    height, width = img.shape[:2]

    # Dark background overlay
    overlay = img.copy()
    cv2.rectangle(
        overlay,
        (0, 0),
        (width, height),
        (15, 15, 25),
        cv2.FILLED,
    )

    cv2.addWeighted(
        overlay,
        0.85,
        img,
        0.15,
        0,
        img,
    )

    title = "HAND GESTURE TIC-TAC-TOE"
    title_size = cv2.getTextSize(
        title,
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        3,
    )[0]

    title_x = max(10, (width - title_size[0]) // 2)

    cv2.putText(
        img,
        title,
        (title_x, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (0, 255, 255),
        3,
    )

    instructions = [
        ("PINCH  = Select Cell", (0, 255, 0)),
        ("1      = Easy", (255, 255, 255)),
        ("2      = Medium", (255, 255, 255)),
        ("3      = Hard", (255, 255, 255)),
    ]

    start_y = 160

    for index, (text, color) in enumerate(instructions):
        text_size = cv2.getTextSize(
            text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            2,
        )[0]

        text_x = max(10, (width - text_size[0]) // 2)
        text_y = start_y + index * 45

        cv2.putText(
            img,
            text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2,
        )

    start_text = "Press SPACE to Start"
    start_size = cv2.getTextSize(
        start_text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        2,
    )[0]

    cv2.putText(
        img,
        start_text,
        (
            max(10, (width - start_size[0]) // 2),
            height - 100,
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2,
    )

    exit_text = "Press ESC to Exit"
    exit_size = cv2.getTextSize(
        exit_text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        2,
    )[0]

    cv2.putText(
        img,
        exit_text,
        (
            max(10, (width - exit_size[0]) // 2),
            height - 55,
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2,
    )


reset_board()


while True:
    success, img = cap.read()

    if not success:
        print("Unable to read from the camera.")
        break

    img = cv2.flip(img, 1)

    # Start screen
    if not game_started:
        draw_start_screen(img)

        cv2.imshow("Hand Gesture Tic-Tac-Toe", img)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # Spacebar
            game_started = True
            reset_board()

            winner = None
            game_over = False
            score_updated = False
            last_click_time = time.time()

        elif key == ord("1"):
            difficulty = "EASY"

        elif key == ord("2"):
            difficulty = "MEDIUM"

        elif key == ord("3"):
            difficulty = "HARD"

        elif key == 27:  # Escape
            break

        continue

    # Main game
    hands, img = detector.findHands(img)

    draw_board(img)

    # Check for winner or draw
    if not game_over:
        winner = check_winner(board)

        if winner:
            game_over = True

        elif is_board_full(board):
            winner = "DRAW"
            game_over = True

    # Update score once
    if game_over and not score_updated:
        if winner == "X":
            player_score += 1

        elif winner == "O":
            ai_score += 1

        elif winner == "DRAW":
            draw_score += 1

        score_updated = True

    # Hand detection
    if hands and not game_over:
        lm_list = hands[0]["lmList"]

        index_x = lm_list[8][0]
        index_y = lm_list[8][1]

        thumb_x = lm_list[4][0]
        thumb_y = lm_list[4][1]

        cv2.circle(
            img,
            (index_x, index_y),
            10,
            (0, 0, 255),
            cv2.FILLED,
        )

        cell = get_cell(index_x, index_y)

        if cell is not None:
            row, col = cell

            cv2.putText(
                img,
                f"Cell: ({row}, {col})",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            distance = math.sqrt(
                (index_x - thumb_x) ** 2
                + (index_y - thumb_y) ** 2
            )

            cv2.putText(
                img,
                f"Distance: {int(distance)}",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2,
            )

            current_time = time.time()

            if (
                distance < 30
                and current_time - last_click_time > 1
            ):
                if board[row][col] == "":
                    # Player move
                    board[row][col] = "X"

                    # AI move
                    if (
                        not check_winner(board)
                        and not is_board_full(board)
                    ):
                        if difficulty == "EASY":
                            easy_move()

                        elif difficulty == "MEDIUM":
                            medium_move()

                        else:
                            ai_move()

                last_click_time = current_time

    # Scoreboard
    cv2.putText(
        img,
        f"Player: {player_score}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        img,
        f"AI: {ai_score}",
        (180, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2,
    )

    cv2.putText(
        img,
        f"Draws: {draw_score}",
        (320, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2,
    )

    cv2.putText(
        img,
        f"Mode: {difficulty}",
        (500, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    # Controls
    cv2.putText(
        img,
        "1-Easy  2-Medium  3-Hard  R-Reset",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
    )

    # Winner message and winning line
    if game_over:
        line = get_winning_line(board)

        if line:
            line_type, index = line

            if line_type == "row":
                line_y = 150 + index * 100

                cv2.line(
                    img,
                    (100, line_y),
                    (400, line_y),
                    (0, 255, 0),
                    6,
                )

            elif line_type == "col":
                line_x = 150 + index * 100

                cv2.line(
                    img,
                    (line_x, 100),
                    (line_x, 400),
                    (0, 255, 0),
                    6,
                )

            elif line_type == "diag":
                if index == 0:
                    cv2.line(
                        img,
                        (100, 100),
                        (400, 400),
                        (0, 255, 0),
                        6,
                    )

                else:
                    cv2.line(
                        img,
                        (400, 100),
                        (100, 400),
                        (0, 255, 0),
                        6,
                    )

        if winner == "X":
            message = "YOU WIN!"
            message_color = (0, 255, 0)

        elif winner == "O":
            message = "AI WINS!"
            message_color = (0, 0, 255)

        else:
            message = "DRAW!"
            message_color = (255, 255, 0)

        cv2.putText(
            img,
            message,
            (250, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            message_color,
            3,
        )

    cv2.imshow("Hand Gesture Tic-Tac-Toe", img)

    key = cv2.waitKey(1) & 0xFF

    # Change difficulty
    if key == ord("1"):
        difficulty = "EASY"

    elif key == ord("2"):
        difficulty = "MEDIUM"

    elif key == ord("3"):
        difficulty = "HARD"

    # Reset game
    elif key in (ord("r"), ord("R")):
        reset_board()

        winner = None
        game_over = False
        score_updated = False
        last_click_time = time.time()

    # Return to start screen
    elif key == 32:
        game_started = False

    # Exit
    elif key == 27:
        break


cap.release()
cv2.destroyAllWindows()
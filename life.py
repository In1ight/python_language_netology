import random
from copy import deepcopy

SIDE = 10
LIVE = "■"
FREE = "·"
NEIGHBORS = [
    lambda board, y, x, dy=dy, dx=dx:
        board[(y + dy) % len(board)][(x + dx) % len(board)] == LIVE
    for dy in (-1, 0, 1)
    for dx in (-1, 0, 1)
    if (dy, dx) != (0, 0)
]
HELP = """Команды:
  c строка столбец — изменить клетку (координаты от 1 до 10)
  r доля           — случайно заполнить поле (доля от 0 до 1)
  n                — сделать один шаг
  8                — показать число соседей
  ?                — показать справку
  q                — выйти
"""


def new_board(side=SIDE):
    return [[FREE for _ in range(side)] for _ in range(side)]


def print_board(board):
    print(*(" ".join(row) for row in board), sep="\n")


def scatter_cells(board, chance):
    for y in range(len(board)):
        for x in range(len(board)):
            board[y][x] = LIVE if random.random() < chance else FREE
    return board


def flip_cell(board, y, x):
    board[y][x] = FREE if board[y][x] == LIVE else LIVE


def live_around(board, y, x):
    return sum(is_busy(board, y, x) for is_busy in NEIGHBORS)


def advance(board):
    result = deepcopy(board)
    for y in range(len(board)):
        for x in range(len(board)):
            amount = live_around(board, y, x)
            if board[y][x] == FREE and amount == 3:
                result[y][x] = LIVE
            elif board[y][x] == LIVE and amount not in (2, 3):
                result[y][x] = FREE
    return result


def print_numbers(board):
    numbers = [
        [str(live_around(board, y, x)) for x in range(len(board))]
        for y in range(len(board))
    ]
    print_board(numbers)


def show(board, numbers):
    if numbers:
        print_numbers(board)
        return
    print_board(board)


def run_game():
    board = new_board()
    turn = 0
    numbers = False

    while True:
        show(board, numbers)
        numbers = False

        if not (command := input(f"\nШаг {turn}. Команда: ").lower().split()):
            continue

        try:
            match command:
                case ["q"]:
                    break
                case ["?"]:
                    print(HELP)
                case ["c" | "с", y_text, x_text]:
                    y, x = int(y_text), int(x_text)
                    if not (1 <= y <= len(board) and 1 <= x <= len(board)):
                        print("Координаты должны быть от 1 до 10")
                        continue
                    flip_cell(board, y - 1, x - 1)
                    turn = 0
                case ["r", chance_text]:
                    chance = float(chance_text)
                    if not 0 <= chance <= 1:
                        print("Доля должна быть от 0 до 1")
                        continue
                    scatter_cells(board, chance)
                    turn = 0
                case ["n"]:
                    next_board = advance(board)
                    turn += 1
                    if next_board == board:
                        print("Игра окончена")
                    board = next_board
                case ["8"]:
                    numbers = True
                case _:
                    print(HELP)
        except Exception:
            print("Некорректные данные")


if __name__ == "__main__":
    run_game()

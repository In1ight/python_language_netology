import random

SIDE = 10
LIVE = "■"
FREE = "·"
SHIFTS = [
    (dy, dx)
    for dy in (-1, 0, 1)
    for dx in (-1, 0, 1)
    if (dy, dx) != (0, 0)
]
HELP = """Команды:
  c строка столбец — изменить клетку
  r доля           — случайно заполнить поле
  n                — сделать один шаг
  8                — показать число соседей
  ?                — показать справку
  q                — выйти
"""


def new_board(side=SIDE):
    return [[False for _ in range(side)] for _ in range(side)]


def print_board(board):
    print("\n".join(
        " ".join(LIVE if cell else FREE for cell in row) for row in board
    ))


def scatter_cells(board, chance):
    for y in range(len(board)):
        for x in range(len(board)):
            board[y][x] = random.random() < chance
    return board


def flip_cell(board, y, x):
    board[y][x] = not board[y][x]


def live_around(board, y, x):
    side = len(board)
    return sum(
        board[(y + dy) % side][(x + dx) % side]
        for dy, dx in SHIFTS
    )


def advance(board):
    result = new_board(len(board))
    for y in range(len(board)):
        for x in range(len(board)):
            amount = live_around(board, y, x)
            if board[y][x]:
                result[y][x] = amount in (2, 3)
            else:
                result[y][x] = amount == 3
    return result


def print_numbers(board):
    print("\n".join(
        " ".join(str(live_around(board, y, x)) for x in range(len(board)))
        for y in range(len(board))
    ))


def run_game():
    board = new_board()
    turn = 0
    numbers = False

    while True:
        if numbers:
            print_numbers(board)
            numbers = False
        else:
            print_board(board)

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
                    if 0 <= y < len(board) and 0 <= x < len(board):
                        flip_cell(board, y, x)
                        turn = 0
                    else:
                        print("Координаты должны быть от 0 до 9")
                case ["r", chance_text]:
                    chance = float(chance_text)
                    if 0 <= chance <= 1:
                        scatter_cells(board, chance)
                        turn = 0
                    else:
                        print("Доля должна быть от 0 до 1")
                case ["n"]:
                    next_board = advance(board)
                    turn += 1
                    if next_board == board:
                        print("Игра окончена")
                    board = next_board
                case ["8"]:
                    numbers = True
                case _:
                    print("Неизвестная команда. Введите ? для справки")
        except ValueError:
            print("Нужно ввести число")


if __name__ == "__main__":
    run_game()

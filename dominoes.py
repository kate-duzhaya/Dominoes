import random
from itertools import cycle


def get_full_domino_set() -> list:
    return [[x, y] for x in range(0, 7) for y in range(x, 7)]


def get_player_dominoes(full_set: list) -> tuple:
    shuffled_set = random.sample(full_set, len(full_set))
    player_set = random.sample(shuffled_set, k=7)
    computer_set = random.sample([x for x in shuffled_set if x not in player_set], k=7)
    stock_set = [x for x in shuffled_set if x not in (player_set + computer_set)]
    return stock_set, computer_set, player_set


def get_starting_piece(player_set: list, computer_set: list) -> tuple:
    dominoes = []
    if max(player_set) > max(computer_set):
        dominoes.append(max(player_set))
        player_set.remove(max(player_set))
        first_move = players[1]
    else:
        dominoes.append(max(computer_set))
        computer_set.remove(max(computer_set))
        first_move = players[0]
    return dominoes, first_move


def show_playing_field():
    print("=" * 70)
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}\n")
    if len(domino_snake) < 6:
        print(*domino_snake)
    else:
        print(*domino_snake[0:3], "...", *domino_snake[-3:])
    print()
    print("Your pieces:")
    for index, pair in enumerate(player_pieces, start=1):
        print(f"{index}: {pair}")


def get_real_index(tile_index: int) -> int:
    real_index = 0
    if tile_index < 0:
        real_index = abs(tile_index + 1)
    elif tile_index > 0:
        real_index = abs(tile_index - 1)
    return real_index


def check_if_move_legal(tile_index: int, tile: list) -> bool:
    if tile_index < 0:
        return domino_snake[0][0] in tile
    elif tile_index > 0:
        return domino_snake[-1][-1] in tile
    elif tile_index == 0:
        return True


def get_computer_move():
    input()
    while True:
        tile_index = random.randrange(-len(computer_pieces), len(computer_pieces))
        real_index = get_real_index(tile_index)
        if check_if_move_legal(tile_index, computer_pieces[real_index]):
            break
    if tile_index == 0:
        skip_a_move(computer_pieces)
    else:
        removed_tile = computer_pieces.pop(real_index)
        add_a_tile_to_domino_snake(tile_index, removed_tile)


def get_player_move():
    input_error_message = "Invalid input. Please try again."
    illegal_move_message = "Illegal move. Please try again."
    while True:
        try:
            tile_index = int(input())
            real_index = get_real_index(tile_index)
            if (-len(player_pieces)) <= tile_index <= len(player_pieces):
                if check_if_move_legal(tile_index, player_pieces[real_index]):
                    break
                else:
                    print(illegal_move_message)
            else:
                raise ValueError
        except ValueError:
            print(input_error_message)
    if tile_index == 0:
        skip_a_move(player_pieces)
    else:
        removed_tile = player_pieces.pop(real_index)
        add_a_tile_to_domino_snake(tile_index, removed_tile)


def add_a_tile_to_domino_snake(tile_index: int, tile: list):
    if tile_index < 0:
        if domino_snake[0][0] != tile[-1]:
            tile.reverse()
        domino_snake.insert(0, tile)
    elif tile_index > 0:
        if domino_snake[-1][-1] != tile[0]:
            tile.reverse()
        domino_snake.append(tile)


def skip_a_move(pieces: list):
    if len(stock_pieces) > 0:
        new_piece = random.choice(stock_pieces)
        stock_pieces.remove(new_piece)
        pieces.append(new_piece)
    else:
        pass


def get_game_status():
    game_over = False
    status = ""
    first_number = domino_snake[0][0]
    count_of_first_number = sum(tile.count(first_number) for tile in domino_snake)
    if len(player_pieces) == 0:
        status = "The game is over. You won!"
        game_over = True
    elif len(computer_pieces) == 0:
        status = "The game is over. The computer won!"
        game_over = True
    elif first_number == domino_snake[-1][-1] and count_of_first_number == 8:
        status = "The game is over. It's a draw!"
        game_over = True
    elif not game_over and current_player == players[0]:
        status = "It's your turn to make a move. Enter your command."
    elif not game_over and current_player == players[1]:
        status = "Computer is about to make a move. Press Enter to continue..."
    return game_over, status


if __name__ == "__main__":
    players = ["player", "computer"]
    stock_pieces, computer_pieces, player_pieces = get_player_dominoes(get_full_domino_set())
    domino_snake, current_player = get_starting_piece(player_pieces, computer_pieces)
    initial_index = players.index(current_player)
    turn_cycle = cycle(players[initial_index:] + players[:initial_index])
    while True:
        current_player = next(turn_cycle)
        show_playing_field()
        is_game_over, game_status = get_game_status()
        print(f"\nStatus: {game_status}")
        if is_game_over:
            exit()
        elif current_player == "computer":
            get_computer_move()
        else:
            get_player_move()

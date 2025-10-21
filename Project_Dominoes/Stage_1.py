import random

def generate_domino_set():
    # Generates a full set of 28 unique dominoes
    dominoes = []
    for i in range(7):
        for j in range(i, 7):
            dominoes.append([i, j])
    return dominoes

def distribute_dominoes(dominoes):
    # Distributes dominoes to stock, computer, and player
    random.shuffle(dominoes)
    stock = dominoes[:14]
    computer_pieces = dominoes[14:21]
    player_pieces = dominoes[21:]
    return stock, computer_pieces, player_pieces

def find_starting_piece_and_player(computer_pieces, player_pieces):
    # Finds the starting piece and determines the first player
    computer_doubles = [d for d in computer_pieces if d[0] == d[1]]
    player_doubles = [d for d in player_pieces if d[0] == d[1]]

    if not computer_doubles and not player_doubles:
        return None, None, None

    if computer_doubles and (not player_doubles or max(computer_doubles) > max(player_doubles)):
        starting_piece = max(computer_doubles)
        computer_pieces.remove(starting_piece)
        status = "player"
    else:
        starting_piece = max(player_doubles)
        player_pieces.remove(starting_piece)
        status = "computer"

    return [starting_piece], computer_pieces, player_pieces, status

# Main game setup loop
while True:
    full_domino_set = generate_domino_set()
    stock_pieces, computer_pieces, player_pieces = distribute_dominoes(full_domino_set)
    domino_snake, computer_pieces, player_pieces, status = find_starting_piece_and_player(computer_pieces, player_pieces)

    if domino_snake is not None:
        break

# Output the results
print("Stock pieces:", stock_pieces)
print("Computer pieces:", computer_pieces)
print("Player pieces:", player_pieces)
print("Domino snake:", domino_snake)
print("Status:", status)

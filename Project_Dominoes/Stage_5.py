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
        return None, None, None, None

    if computer_doubles and (not player_doubles or max(computer_doubles) > max(player_doubles)):
        starting_piece = list(max(computer_doubles))
        computer_pieces.remove(starting_piece)
        status = "player"
    else:
        starting_piece = list(max(player_doubles))
        player_pieces.remove(starting_piece)
        status = "computer"

    return starting_piece, computer_pieces, player_pieces, status

def game_state(stock, computer, player, snake, status):
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}")
    print()
    if len(snake) <= 6:
        print(*snake, sep="")
    else:
        print(*snake[:3], "...", *snake[-3:], sep="")
    print()
    print("Your pieces:")
    for i, piece in enumerate(player):
        print(f"{i+1}:{piece}")
    print()
    if status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status == "player":
        print("Status: It's your turn to make a move. Enter your command.")


def turn(action, stock, pieces, snake):
  if action == 0:
      if stock:
          pieces.append(stock.pop())
  else:
      action_piece = pieces[abs(action) - 1]
      pieces.remove(action_piece)
      if action > 0:
          if snake[-1][1] == action_piece[0]:
              snake.append(action_piece)
          else:
              action_piece.reverse()
              snake.append(action_piece)
      else:
          if snake[0][0] == action_piece[1]:
              snake.insert(0, action_piece)
          else:
              action_piece.reverse()
              snake.insert(0, action_piece)
  return stock, pieces, snake


def snake_count(snake):
  if snake[-1][1] == snake[0][0]:
      piece_values = [0,1,2,3,4,5,6]
      piece_dict = dict.fromkeys(piece_values, 0)
      for piece in snake:
          piece_dict[piece[0]] += 1
          piece_dict[piece[1]] += 1

      for key in piece_dict:
          if piece_dict[key] >= 8 and snake[0][0] == key:
              return True
  return False

def strategic_count(snake, pieces):
    piece_values = [0,1,2,3,4,5,6]
    piece_dict = dict.fromkeys(piece_values, 0)
    for piece in snake:
        piece_dict[piece[0]] += 1
        piece_dict[piece[1]] += 1
    for piece in pieces:
        piece_dict[piece[0]] += 1
        piece_dict[piece[1]] += 1
    
    pieces_values = []
    for piece in pieces:
        pieces_values.append(piece_dict[piece[0]] + piece_dict[piece[1]])
    return pieces_values


def win_check(stock, player, computer, snake):
    if not player:
        print("\nStatus: The game is over. You won!")
        return True
    elif not computer:
        print("\nStatus: The game is over. The computer won!")
        return True
    elif snake_count(snake):
        print("\nStatus: The game is over. It's a draw!")
        return True
    else:
        return False

def rules(action, pieces, snake):
  if action == 0:
    return False
  else:
    action_piece = pieces[abs(action) - 1]
    if action > 0:
      if snake[-1][1] == action_piece[0] or snake[-1][1] == action_piece[1]:
        return False
      else:
        return True
    else:
      if snake[0][0] == action_piece[0] or snake[0][0] == action_piece[1]:
        return False
      else:
        return True

## st - stock pieces list
## cp - computer pieces list
## pp - player pieces list
## ds - domino snake list

# Main game setup loop
while True:
    full_domino_set = generate_domino_set()
    st, cp, pp = distribute_dominoes(full_domino_set)
    starting_piece, cp, pp, status = find_starting_piece_and_player(cp, pp)
    if starting_piece:
        domino_snake = [starting_piece]
    else:
        domino_snake = None
    if domino_snake is not None:
        break

while True:
  game_state(st, cp, pp, domino_snake, status)
  if win_check(st, pp, cp, domino_snake):
    break

  if status == "computer":
    input()
    cp_len = len(cp)
    generator_ok = False
    while not generator_ok:
        piece_values = strategic_count(domino_snake, cp)

        indexed_list = list(enumerate(piece_values))
        sorted_indexed_list = sorted(indexed_list, key=lambda x: x[1])
        sorted_indexed_list.reverse()
        sorted_piece_values_index = [index for index, value in sorted_indexed_list]

        # test each piece in value order
        for i in sorted_piece_values_index:
            if not rules(i + 1, cp, domino_snake):
                computer_action = i + 1
                generator_ok = True
                break
            elif not rules(-i - 1, cp, domino_snake):
                computer_action = -i - 1
                generator_ok = True
                break
        if not generator_ok:
            computer_action = 0
            generator_ok = True

        #computer_action = random.randint(-cp_len, cp_len)
        #if not rules(computer_action, cp, domino_snake):
        #    generator_ok = True

    st, cp, domino_snake = turn(computer_action, st, cp, domino_snake)
    status = "player"

  else:
    input_ok = False
    while not input_ok:
      try:
          player_action = int(input())
          if abs(player_action) > len(pp):
              print("Invalid input. Please try again.")
          elif rules(player_action, pp, domino_snake):
              print("Illegal move. Please try again.")
          else:
              input_ok = True
      except:
          print("Invalid input. Please try again.")


    st, pp, domino_snake = turn(player_action, st, pp, domino_snake)
    status = "computer"

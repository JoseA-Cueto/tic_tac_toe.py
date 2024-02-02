import random

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def print_board(self):
        for row in [self.board[i:i+3] for i in range(0, 9, 3)]:
            print("| " + " | ".join(row) + " |")

    def make_move(self, position):
        if 1 <= position <= 9 and self.board[position - 1] == " ":
            self.board[position - 1] = self.current_player
            self.switch_player()
            return True
        else:
            print("Movimiento inválido. Inténtalo de nuevo.")
            return False

    def make_computer_move(self):
        if self.current_player == "O":
            _, best_move = self.minimax(self.board, "O")
            if best_move is not None:
                self.board[best_move] = self.current_player
                self.switch_player()

    def is_board_full(self):
        return " " not in self.board

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Verificación de líneas horizontales
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return True

        # Verificación de líneas verticales
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return True

        # Verificación de diagonales
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True

        return False
    
    def minimax(self, board, player):
        available_moves = [i for i, mark in enumerate(board) if mark == " "]

        if self.check_winner():
            if player == "O":
                return -1, None
            else:
                return 1, None
        elif not available_moves:
            return 0, None

        best_score = float('-inf') if player == "O" else float('inf')
        best_move = None

        for move in available_moves:
            board[move] = player
            score, _ = self.minimax(board, "X" if player == "O" else "O")
            board[move] = " "  # Deshacer el movimiento

            if player == "O" and score > best_score:
                best_score = score
                best_move = move
            elif player == "X" and score < best_score:
                best_score = score
                best_move = move

        return best_score, best_move


game = TicTacToe()

while not game.check_winner() and not game.is_board_full():
    game.print_board()

    try:
        move = int(input(f"{game.current_player}, elige una posición (1-9): "))
        if game.make_move(move):
            game.make_computer_move()
    except ValueError:
        print("Por favor, ingresa un número válido.")

game.print_board()

if game.check_winner():
    if game.current_player == "X":
        print("¡Felicidades! Ganaste.")
    elif game.current_player == "O":
        print("El ordenador ha vencido.")
else:
    print("¡Empate!")

print("Juego terminado.")

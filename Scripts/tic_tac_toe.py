import random
import tkinter as tk
from tkinter import Button, messagebox

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


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        
        self.game = TicTacToe()
        
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.root, text="", font=('normal', 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Contenedor para los botones
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=3)

        # Botón de reinicio
        restart_button = Button(button_frame, text="Reiniciar", command=self.restart_game)
        restart_button.pack(side=tk.LEFT)

    def on_button_click(self, row, col):
        if self.game.make_move(row * 3 + col + 1):
            self.update_board()
            if not self.game.check_winner() and not self.game.is_board_full():
                self.game.make_computer_move()
                self.update_board()
                if self.game.check_winner():
                    self.show_winner()
            elif self.game.is_board_full():
                messagebox.showinfo("Empate", "¡Empate!")
            else:
                self.show_winner()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.game.board[i * 3 + j]

    def show_winner(self):
        if self.game.check_winner():
            winner_message = "¡Felicidades! Ganaste." if self.game.current_player == "O" else "El ordenador ha vencido."
        else:
            winner_message = "¡Empate!"

        # Mensaje con el botón de reinicio
        result = messagebox.showinfo("¡Juego Terminado!", winner_message)
        if result == "ok":
            self.restart_game()

    def restart_game(self):
        self.game = TicTacToe()
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

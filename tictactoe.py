import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class GameMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe TTT")
        self.window.geometry("500x600")
        self.BG_COLOR = "#2C3E50"
        self.BUTTON_COLOR = "#3498DB"
        self.TEXT_COLOR = "white"

        self.window.configure(bg=self.BG_COLOR)
        self.create_styles()
        self.create_menu()
        self.load_scores()

    def create_styles(self):
        style = ttk.Style()
        style.configure(
            'Custom.TButton',
            font=('Helvetica', 12),
            padding=10,
            width=25
        )
        style.configure(
            'Title.TLabel',
            font=('Helvetica', 24, 'bold'),
            background=self.BG_COLOR,
            foreground=self.TEXT_COLOR
        )

    def create_menu(self):
        title_frame = ttk.Frame(self.window)
        title_frame.pack(pady=30)

        title = ttk.Label(
            title_frame,
            text="Welcome to Tic Tac Toe",
            style='Title.TLabel'
        )
        title.pack()

        modes_frame = ttk.LabelFrame(
            self.window,
            text="Game Modes",
            padding=20
        )
        modes_frame.pack(pady=10, padx=20, fill="x")

        ttk.Button(
            modes_frame,
            text="Player vs Player",
            style='Custom.TButton',
            command=lambda: self.start_game("PVP")
        ).pack(pady=5)

        ttk.Button(
            modes_frame,
            text="Player vs Computer (Easy)",
            style='Custom.TButton',
            command=lambda: self.start_game("PVC_EASY")
        ).pack(pady=5)

        ttk.Button(
            modes_frame,
            text="Player vs Computer (Hard)",
            style='Custom.TButton',
            command=lambda: self.start_game("PVC_HARD")
        ).pack(pady=5)

        options_frame = ttk.LabelFrame(
            self.window,
            text="Options",
            padding=20
        )
        options_frame.pack(pady=10, padx=20, fill="x")

        ttk.Button(
            options_frame,
            text="View Leaderboard",
            style='Custom.TButton',
            command=self.show_leaderboard
        ).pack(pady=5)

        ttk.Button(
            options_frame,
            text="Settings",
            style='Custom.TButton',
            command=self.show_settings
        ).pack(pady=5)

        ttk.Button(
            options_frame,
            text="Exit Game",
            style='Custom.TButton',
            command=self.window.quit
        ).pack(pady=5)

    def load_scores(self):
        self.scores = {
            "Player X": 0,
            "Player O": 0,
            "Player": 0,
            "Computer (Easy)": 0,
            "Computer (Hard)": 0
        }
        try:
            with open("scores.json", "r") as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.save_scores()

    def save_scores(self):
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)

    def show_leaderboard(self):
        leaderboard = tk.Toplevel(self.window)
        leaderboard.title("Leaderboard")
        leaderboard.geometry("400x300")
        leaderboard.configure(bg=self.BG_COLOR)

        tk.Label(
            leaderboard,
            text="Leaderboard",
            font=('Helvetica', 20, 'bold'),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(pady=20)

        scores_frame = tk.Frame(leaderboard, bg=self.BG_COLOR)
        scores_frame.pack(pady=10)

        sorted_scores = dict(sorted(self.scores.items(), key=lambda x: x[1], reverse=True))

        for player, score in sorted_scores.items():
            tk.Label(
                scores_frame,
                text=f"{player}: {score} wins",
                font=('Helvetica', 12),
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR
            ).pack(pady=5)

    def show_settings(self):
        settings = tk.Toplevel(self.window)
        settings.title("Settings")
        settings.geometry("300x200")
        settings.configure(bg=self.BG_COLOR)

        tk.Label(
            settings,
            text="Settings",
            font=('Helvetica', 20, 'bold'),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(pady=20)

        ttk.Button(
            settings,
            text="Reset All Scores",
            command=self.reset_scores
        ).pack(pady=10)

    def reset_scores(self):
        self.scores = {
            "Player X": 0,
            "Player O": 0,
            "Player": 0,
            "Computer (Easy)": 0,
            "Computer (Hard)": 0
        }
        self.save_scores()
        messagebox.showinfo("Success", "All scores have been reset!")

    def start_game(self, mode):
        game_window = tk.Toplevel(self.window)
        TicTacToe(game_window, self, mode)


class TicTacToe:
    def __init__(self, window, menu, mode):
        self.time_left = 15
        self.winning_cells = None 
        
        try:
            import pygame
            pygame.mixer.init()
        except ImportError:
            print("Pygame not installed - sound will be disabled")
        self.window = window
        self.menu = menu
        self.mode = mode
        self.window.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True

        self.GAME_COLOR = "#2C3E50"
        self.BUTTON_COLOR = "#ECF0F1"
        self.BUTTON_HOVER_COLOR = "#BDC3C7"
        self.FONT = ('Helvetica', 24, 'bold')


        self.window.configure(bg=self.GAME_COLOR)
        self.window.resizable(False, False)

        
        info_frame = tk.Frame(self.window, bg=self.GAME_COLOR)
        info_frame.grid(row=0, column=0, columnspan=3, pady=10)

        mode_text = {
            "PVP": "Player vs Player",
            "PVC_EASY": "Player vs Computer (Easy)",
            "PVC_HARD": "Player vs Computer (Hard)"
        }
        tk.Label(
            info_frame,
            text=mode_text[mode],
            font=('Helvetica', 14, 'bold'),
            bg=self.GAME_COLOR,
            fg="white"
        ).pack()

        try:
            self.move_sound = pygame.mixer.Sound("C:\\Users\\suraa\\.vscode\\.vscode\\assets\\move.wav")
            self.win_sound = pygame.mixer.Sound("C:\\Users\\suraa\\.vscode\\.vscode\\assets\\win.wav")
            self.draw_sound = pygame.mixer.Sound("C:\\Users\\suraa\\.vscode\\.vscode\\assets\\draw.wav")
        except:
             print("Sound files not found")
             self.move_sound = None
             self.win_sound = None
             self.draw_sound = None



        self.timer_label = tk.Label(
            info_frame,
            text=f"Time: {self.time_left}s",
            font=('Helvetica', 12),
            bg=self.GAME_COLOR,
            fg="white"
        )
        self.timer_label.pack(pady=5)

        self.status_label = tk.Label(
            info_frame,
            text="Player X's turn",
            font=('Helvetica', 12),
            bg=self.GAME_COLOR,
            fg="white"
        )
        self.status_label.pack(pady=5)

        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.window,
                    text="",
                    font=self.FONT,
                    width=5,
                    height=2,
                    bg=self.BUTTON_COLOR,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5)
                button.bind('<Enter>', lambda e, btn=button: btn.configure(bg=self.BUTTON_HOVER_COLOR))
                button.bind('<Leave>', lambda e, btn=button: btn.configure(bg=self.BUTTON_COLOR))
                self.buttons.append(button)

        control_frame = tk.Frame(self.window, bg=self.GAME_COLOR)
        control_frame.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Button(
            control_frame,
            text="Restart",
            font=('Helvetica', 10),
            command=self.restart_game
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Back to Menu",
            font=('Helvetica', 10),
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)

        self.update_timer()

    def update_timer(self):
        if self.game_active:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=f"Time: {self.time_left}s")
                self.window.after(1000, self.update_timer)
            else:
                self.time_left = 15
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Time's up! Player {self.current_player}'s turn")
                if self.mode != "PVP" and self.current_player == "O":
                    self.make_computer_move()
                self.update_timer()

    def button_click(self, row, col):
        if not self.game_active:
            return

        index = 3 * row + col

        if self.board[index] == "":
            self.make_move(index)
            
            if not self.check_game_end() and self.mode != "PVP" and self.current_player == "O":
                self.window.after(500, self.make_computer_move)
                

    def make_move(self, index):
        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            fg="red" if self.current_player == "X" else "blue"
        )
        try:
            if self.move_sound:
                self.move_sound.play()
        except:
            pass

        if not self.check_game_end():
            self.current_player = "O" if self.current_player == "X" else "X"
            if self.mode == "PVP":
                self.status_label.config(text=f"Player {self.current_player}'s turn")
            else:
                next_player = "Computer's turn" if self.current_player == "O" else "Player's turn"
                self.status_label.config(text=next_player)

    def make_computer_move(self):
        if not self.game_active or self.current_player != "O":
            return

        if self.mode == "PVC_EASY":
            empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
            if empty_cells:
                move = random.choice(empty_cells)
                self.make_move(move)
        else:  # Hard mode
            best_move = self.get_best_move()
            if best_move is not None:
                self.make_move(best_move)

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False, alpha, beta)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner_board(board, "O"):
            return 1
        if self.check_winner_board(board, "X"):
            return -1
        if "" not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score
    def animate_winner(self):
        if self.winning_cells:
            for i in self.winning_cells:
                self.buttons[i].config(bg="#90EE90")  # Light green

    def check_game_end(self):
        if self.check_winner():
            self.game_active = False
            if self.mode == "PVP":
                winner = f"Player {self.current_player}"
                self.menu.scores[f"Player {self.current_player}"] += 1
            else:
                if self.current_player == "X":
                    winner = "Player"
                    self.menu.scores["Player"] += 1
                else:
                    winner = "Computer"
                    difficulty = "Easy" if self.mode == "PVC_EASY" else "Hard"
                    self.menu.scores[f"Computer ({difficulty})"] += 1
            
            self.menu.save_scores()
            self.status_label.config(text=f"{winner} wins!")
            try:
                if self.win_sound:
                    self.win_sound.play()
            except:
                 pass
            self.animate_winner()
            messagebox.showinfo("Game Over", f"{winner} wins!")
            return True

        elif "" not in self.board:
            self.game_active = False
            self.status_label.config(text="It's a tie!")
            try:
                if self.draw_sound:
                   self.draw_sound.play()
            except:
                pass
            messagebox.showinfo("Game Over", "It's a tie!")
            return True

        return False



    def check_winner(self):
        return self.check_winner_board(self.board, self.current_player)

    def check_winner_board(self, board, player):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]              
        ]

        for combo in win_combinations:
            if all(board[i] == player for i in combo):
                self.winning_cells = combo 
                return True
        return False

    def restart_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.status_label.config(text="Player X's turn")
        for button in self.buttons:
            button.config(text="", fg="black")

if __name__ == "__main__":
    menu = GameMenu()
    menu.window.mainloop()

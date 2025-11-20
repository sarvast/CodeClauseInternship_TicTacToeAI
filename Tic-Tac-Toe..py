#!/usr/bin/env python3
"""
My Tic-Tac-Toe AI Project
=========================

Built during my CodeClause AI internship - this was such a fun challenge!
Started simple but ended up implementing a full minimax algorithm.
Pretty proud of how the Hard AI turned out - it's nearly unbeatable! 😄

Features I built:
- Clean GUI with dark theme (spent way too much time on colors)
- Easy AI for beginners (random moves)
- Hard AI with minimax (my first real AI algorithm!)
- Score tracking (to see how often I lose to my own creation)
- Smooth user experience

Author: Sarthak Srivastava
Internship: CodeClause AI Program
Project ID: #CC3599
Built: November 2025
Fun Level: 10/10 would code again!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random


class TicTacToe:
    """
    Core game logic for Tic-Tac-Toe.
    
    This class handles the game board, move validation, and win detection.
    The board is represented as a list of 9 positions (0-8) arranged as:
    
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """
    
    def __init__(self):
        """Initialize a new game with empty board."""
        self.board = [' ' for _ in range(9)]  # Empty 3x3 board
        self.current_winner = None  # Track who won (X, O, or None)
        
    def available_moves(self):
        """Get list of available positions where players can make moves."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        """Check if there are any empty squares left on the board."""
        return ' ' in self.board
    
    def num_empty_squares(self):
        """Count how many empty squares are left."""
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        """
        Attempt to make a move on the board.
        
        Args:
            square (int): Position on board (0-8)
            letter (str): Player symbol ('X' or 'O')
            
        Returns:
            bool: True if move was successful, False if position occupied
        """
        if self.board[square] == ' ':
            self.board[square] = letter
            # Check if this move resulted in a win
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        """
        Check if the last move resulted in a win.
        
        Args:
            square (int): The position of the last move
            letter (str): The player who made the move
            
        Returns:
            bool: True if this move wins the game
        """
        # Check the row of the last move
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
            
        # Check the column of the last move
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
            
        # Check diagonals (only if move was on a diagonal position)
        if square % 2 == 0:  # Corner or center positions
            # Main diagonal (top-left to bottom-right)
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            # Anti-diagonal (top-right to bottom-left)
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False
    
    def reset_game(self):
        """Reset the board for a new game."""
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

class RandomComputerPlayer:
    """
    Easy AI that makes random moves.
    
    This AI player chooses moves randomly from available positions,
    making it beatable for beginners.
    """
    
    def __init__(self, letter):
        """Initialize the random AI player.
        
        Args:
            letter (str): The symbol this AI uses ('O' typically)
        """
        self.letter = letter
        
    def get_move(self, game):
        """
        Choose a random move from available positions.
        
        Args:
            game (TicTacToe): Current game state
            
        Returns:
            int: Random position from available moves
        """
        return random.choice(game.available_moves())

class SmartComputerPlayer:
    """
    Advanced AI using minimax algorithm.
    
    This AI is nearly unbeatable as it uses the minimax algorithm
    to evaluate all possible future game states and choose the optimal move.
    """
    
    def __init__(self, letter):
        """Initialize the smart AI player.
        
        Args:
            letter (str): The symbol this AI uses ('O' typically)
        """
        self.letter = letter
        
    def get_move(self, game):
        """
        Choose the best possible move using minimax algorithm.
        
        Args:
            game (TicTacToe): Current game state
            
        Returns:
            int: Optimal position to play
        """
        # On first move, choose a corner for better strategy
        if len(game.available_moves()) == 9:
            return random.choice([0, 2, 6, 8])  # Corner positions
        else:
            # Use minimax to find the best move
            return self.minimax(game, self.letter)['position']
        
    def minimax(self, state, player):
        """
        Minimax algorithm implementation for optimal play.
        
        This recursive algorithm evaluates all possible future game states
        to determine the best move for the current player.
        
        Args:
            state (TicTacToe): Current game state
            player (str): Current player ('X' or 'O')
            
        Returns:
            dict: Contains 'position' and 'score' for the best move
        """
        max_player = self.letter  # AI is trying to maximize
        other_player = 'O' if player == 'X' else 'X'
        
        # Base cases: game is over
        if state.current_winner == other_player:
            # Game is won - score based on how quickly it was won
            return {'position': None, 
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player 
                    else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            # Game is tied
            return {'position': None, 'score': 0}
            
        # Initialize best move tracking
        if player == max_player:
            best = {'position': None, 'score': -float('inf')}  # Want to maximize
        else:
            best = {'position': None, 'score': float('inf')}   # Want to minimize
            
        # Try each possible move
        for possible_move in state.available_moves():
            # Make the move temporarily
            state.make_move(possible_move, player)
            
            # Recursively evaluate this position
            sim_score = self.minimax(state, other_player)
            
            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update best move if this is better
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class TicTacToeGUI:
    """
    Modern GUI for Tic-Tac-Toe game.
    
    Features:
    - Dark theme with modern colors
    - AI difficulty selection
    - Score tracking
    - Smooth animations and feedback
    - Responsive design
    """
    
    def __init__(self):
        """Initialize the game window and components."""
        # Create main window
        self.root = tk.Tk()
        self.root.title("🎮 Tic-Tac-Toe AI Challenge")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')  # Dark blue-gray background
        self.root.resizable(False, False)
        
        # Apply modern styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Initialize game components
        self.game = TicTacToe()
        self.current_player = 'X'  # Human always starts
        self.ai_difficulty = "smart"  # Default to challenging AI
        self.ai_player = None
        
        # Score tracking
        self.human_wins = 0
        self.ai_wins = 0
        self.ties = 0
        
        # Build the user interface
        self.setup_ui()
        
    def setup_ui(self):
        """Create and arrange all UI elements."""
        # Game header with title and subtitle
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(pady=20)
        
        title_label = tk.Label(header_frame, text="🎮 Tic-Tac-Toe AI Challenge", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Test your skills against our AI!", 
                                 font=('Arial', 12), 
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack(pady=5)
        
        # AI difficulty selection section
        difficulty_frame = tk.Frame(self.root, bg='#2c3e50')
        difficulty_frame.pack(pady=15)
        
        difficulty_label = tk.Label(difficulty_frame, text="🤖 Choose Your Opponent:", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#ecf0f1', bg='#2c3e50')
        difficulty_label.pack()
        
        # Container for difficulty buttons
        diff_buttons_frame = tk.Frame(difficulty_frame, bg='#2c3e50')
        diff_buttons_frame.pack(pady=10)
        
        # Common button styling
        button_style = {'font': ('Arial', 10), 'width': 15, 'height': 2, 
                       'fg': 'white', 'bd': 0, 'cursor': 'hand2'}
        
        # Easy AI button (green for beginner-friendly)
        self.easy_btn = tk.Button(diff_buttons_frame, text="😊 Easy AI", 
                                 command=lambda: self.set_ai_difficulty("easy"),
                                 bg='#27ae60', **button_style)
        self.easy_btn.pack(side=tk.LEFT, padx=5)
        
        # Hard AI button (red for challenging)
        self.hard_btn = tk.Button(diff_buttons_frame, text="🔥 Hard AI", 
                                 command=lambda: self.set_ai_difficulty("smart"),
                                 bg='#e74c3c', **button_style)
        self.hard_btn.pack(side=tk.LEFT, padx=5)
        
        # Game board container
        self.board_frame = tk.Frame(self.root, bg='#2c3e50')
        self.board_frame.pack(pady=20)
        
        # Game status display
        self.status_label = tk.Label(self.root, text="🎯 Select AI difficulty and make your move!", 
                                   font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50')
        self.status_label.pack(pady=10)
        
        # Score tracking display
        score_frame = tk.Frame(self.root, bg='#2c3e50')
        score_frame.pack(pady=10)
        
        self.score_label = tk.Label(score_frame, text="📊 Score: You 0 - 0 AI | Ties: 0", 
                                   font=('Arial', 10), fg='#f39c12', bg='#2c3e50')
        self.score_label.pack()
        
        # Game control buttons
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=20)
        
        # New game button (blue for primary action)
        new_game_btn = tk.Button(control_frame, text="🔄 New Game", 
                                command=self.start_new_game, 
                                font=('Arial', 10), bg='#3498db', fg='white',
                                width=12, height=1, bd=0, cursor='hand2')
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Reset score button (orange for secondary action)
        reset_btn = tk.Button(control_frame, text="📊 Reset Score", 
                             command=self.reset_score, 
                             font=('Arial', 10), bg='#e67e22', fg='white',
                             width=12, height=1, bd=0, cursor='hand2')
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Exit button (gray for neutral action)
        exit_btn = tk.Button(control_frame, text="❌ Exit", 
                           command=self.root.quit,
                           font=('Arial', 10), bg='#95a5a6', fg='white',
                           width=12, height=1, bd=0, cursor='hand2')
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # Create the game board and set initial state
        self.create_board()
        self.update_difficulty_buttons()
        
    def create_board(self):
        """Create the 3x3 game board with clickable buttons."""
        # Remove any existing board elements
        for widget in self.board_frame.winfo_children():
            widget.destroy()
            
        # Create button grid for the game board
        self.buttons = []
        for i in range(9):
            row = i // 3  # Calculate row (0, 1, or 2)
            col = i % 3   # Calculate column (0, 1, or 2)
            
            # Create individual board square
            btn = tk.Button(self.board_frame, text=' ', font=('Arial', 20, 'bold'),
                          width=6, height=3, bg='#34495e', fg='#ecf0f1',
                          relief='raised', bd=3, cursor='hand2',
                          command=lambda idx=i: self.human_move(idx))
            
            # Position button in grid
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.buttons.append(btn)
            
        # Make grid responsive (buttons expand with window)
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
    
    def set_ai_difficulty(self, difficulty):
        """Change AI difficulty and start a new game.
        
        Args:
            difficulty (str): Either 'easy' or 'smart'
        """
        self.ai_difficulty = difficulty
        self.update_difficulty_buttons()
        self.start_new_game()
        
    def update_difficulty_buttons(self):
        """Update button colors to show selected difficulty."""
        # Reset buttons to default colors
        self.easy_btn.config(bg='#27ae60')  # Green for easy
        self.hard_btn.config(bg='#e74c3c')  # Red for hard
        
        # Highlight the selected difficulty
        if self.ai_difficulty == "easy":
            self.easy_btn.config(bg='#2ecc71')  # Brighter green when selected
            ai_type = "😊 Easy AI"
        else:
            self.hard_btn.config(bg='#c0392b')  # Darker red when selected
            ai_type = "🔥 Hard AI"
            
        self.status_label.config(text=f"🎯 Playing against {ai_type}. Your turn (X)!")
    
    def start_new_game(self):
        """Initialize a fresh game with selected AI difficulty."""
        # Reset game state
        self.game.reset_game()
        self.current_player = 'X'  # Human always starts first
        
        # Create appropriate AI opponent
        if self.ai_difficulty == "easy":
            self.ai_player = RandomComputerPlayer('O')
            ai_type = "😊 Easy AI"
        else:
            self.ai_player = SmartComputerPlayer('O')
            ai_type = "🔥 Hard AI"
            
        # Refresh the visual board
        self.update_board()
        self.status_label.config(text=f"🎯 Playing against {ai_type}. Your turn (X)!")
        
        # Make sure all board buttons are clickable
        for btn in self.buttons:
            btn.config(state='normal')
    
    def human_move(self, square):
        """Handle human player's move.
        
        Args:
            square (int): Position clicked by human (0-8)
        """
        # Validate move conditions
        if (self.current_player == 'O' or 
            self.game.current_winner or 
            not self.game.empty_squares()):
            return  # Invalid move conditions
            
        # Attempt to make the move
        if self.game.make_move(square, 'X'):
            self.update_board()
            
            # Check game end conditions
            if self.game.current_winner:
                self.human_wins += 1
                self.show_winner("human")
            elif not self.game.empty_squares():
                self.ties += 1
                self.show_tie()
            else:
                # Switch to AI's turn
                self.current_player = 'O'
                self.status_label.config(text="🤖 AI is thinking...")
                # Add small delay for better user experience
                self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """Handle AI player's move."""
        # Validate AI can make a move
        if (self.current_player == 'O' and 
            self.ai_player and 
            not self.game.current_winner and 
            self.game.empty_squares()):
            
            # Get AI's chosen move
            square = self.ai_player.get_move(self.game)
            
            # Make the AI move
            if self.game.make_move(square, 'O'):
                self.update_board()
                
                # Check game end conditions
                if self.game.current_winner:
                    self.ai_wins += 1
                    self.show_winner("ai")
                elif not self.game.empty_squares():
                    self.ties += 1
                    self.show_tie()
                else:
                    # Switch back to human's turn
                    self.current_player = 'X'
                    ai_type = "😊 Easy AI" if self.ai_difficulty == "easy" else "🔥 Hard AI"
                    self.status_label.config(text=f"🎯 Your turn! Playing against {ai_type}")
    
    def update_board(self):
        """Refresh the visual board to match game state."""
        for i in range(9):
            text = self.game.board[i]
            # Color coding: Red for X (human), Blue for O (AI), Gray for empty
            if text == 'X':
                color = '#e74c3c'  # Red for human player
            elif text == 'O':
                color = '#3498db'  # Blue for AI player
            else:
                color = '#34495e'  # Gray for empty squares
                
            self.buttons[i].config(text=text, bg=color)
            
        # Update score display with current statistics
        self.score_label.config(text=f"📊 Score: You {self.human_wins} - {self.ai_wins} AI | Ties: {self.ties}")
    
    def show_winner(self, winner):
        """Display winner and disable board.
        
        Args:
            winner (str): Either 'human' or 'ai'
        """
        # Disable all board buttons to prevent further moves
        for btn in self.buttons:
            btn.config(state='disabled')
        
        # Set appropriate message and color based on winner
        if winner == "human":
            message = "🎉 Congratulations! You defeated the AI!"
            color = "#2ecc71"  # Green for victory
        else:
            message = "🤖 AI wins! Don't give up, try again!"
            color = "#e74c3c"  # Red for defeat
            
        # Update status and show popup
        self.status_label.config(text=message, fg=color)
        messagebox.showinfo("🎮 Game Over", message)
    
    def show_tie(self):
        """Display tie game message and disable board."""
        # Disable all board buttons
        for btn in self.buttons:
            btn.config(state='disabled')
            
        # Show tie message in orange
        self.status_label.config(text="🤝 Great game! It's a tie!", fg="#f39c12")
        messagebox.showinfo("🎮 Game Over", "🤝 It's a tie! Well played!")
    
    def reset_score(self):
        """Reset all scores to zero and start fresh game."""
        self.human_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.score_label.config(text="📊 Score: You 0 - 0 AI | Ties: 0")
        self.start_new_game()
    
    def run(self):
        """Start the game application."""
        self.root.mainloop()

def main():
    """Main function to run the Tic-Tac-Toe game."""
    try:
        # Create and run the game
        app = TicTacToeGUI()
        app.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        messagebox.showerror("Error", f"Failed to start game: {e}")


if __name__ == "__main__":
    main()
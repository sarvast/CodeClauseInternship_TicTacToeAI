#!/usr/bin/env python3
"""
Unit Tests for Tic-Tac-Toe Game Logic
====================================

Tests for TicTacToe class and AI players to ensure correct functionality.
"""

import unittest
import sys
import os

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import game module from the correctly named file
import importlib.util
game_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Tic-Tac-Toe..py")
spec = importlib.util.spec_from_file_location("game", game_file_path)
game_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_module)
TicTacToe = game_module.TicTacToe
RandomComputerPlayer = game_module.RandomComputerPlayer
SmartComputerPlayer = game_module.SmartComputerPlayer


class TestTicTacToeGame(unittest.TestCase):
    """Test cases for core TicTacToe game logic."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = TicTacToe()
    
    def test_initial_board_state(self):
        """Test that new game has empty board."""
        self.assertEqual(self.game.board, [' '] * 9)
        self.assertIsNone(self.game.current_winner)
        self.assertTrue(self.game.empty_squares())
        self.assertEqual(self.game.num_empty_squares(), 9)
    
    def test_make_valid_move(self):
        """Test making valid moves on empty squares."""
        self.assertTrue(self.game.make_move(0, 'X'))
        self.assertEqual(self.game.board[0], 'X')
        self.assertTrue(self.game.make_move(4, 'O'))
        self.assertEqual(self.game.board[4], 'O')
    
    def test_make_invalid_move(self):
        """Test that occupied squares reject new moves."""
        self.game.make_move(0, 'X')
        self.assertFalse(self.game.make_move(0, 'O'))
        self.assertEqual(self.game.board[0], 'X')
    
    def test_available_moves(self):
        """Test available moves calculation."""
        self.assertEqual(self.game.available_moves(), list(range(9)))
        self.game.make_move(0, 'X')
        self.game.make_move(4, 'O')
        expected = [1, 2, 3, 5, 6, 7, 8]
        self.assertEqual(self.game.available_moves(), expected)
    
    def test_horizontal_win(self):
        """Test horizontal win detection."""
        # Top row win
        self.game.make_move(0, 'X')
        self.game.make_move(1, 'X')
        self.assertTrue(self.game.make_move(2, 'X'))
        self.assertEqual(self.game.current_winner, 'X')
    
    def test_vertical_win(self):
        """Test vertical win detection."""
        # Left column win
        self.game.make_move(0, 'O')
        self.game.make_move(3, 'O')
        self.assertTrue(self.game.make_move(6, 'O'))
        self.assertEqual(self.game.current_winner, 'O')
    
    def test_diagonal_win(self):
        """Test diagonal win detection."""
        # Main diagonal win
        self.game.make_move(0, 'X')
        self.game.make_move(4, 'X')
        self.assertTrue(self.game.make_move(8, 'X'))
        self.assertEqual(self.game.current_winner, 'X')


class TestRandomAI(unittest.TestCase):
    """Test cases for RandomComputerPlayer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe()
        self.ai = RandomComputerPlayer('O')
    
    def test_ai_makes_valid_moves(self):
        """Test that AI only chooses available positions."""
        for _ in range(10):  # Test multiple times due to randomness
            move = self.ai.get_move(self.game)
            self.assertIn(move, self.game.available_moves())
    
    def test_ai_adapts_to_board_state(self):
        """Test AI adapts when board fills up."""
        # Fill most of board
        for i in range(8):
            self.game.make_move(i, 'X')
        
        move = self.ai.get_move(self.game)
        self.assertEqual(move, 8)  # Only position left


class TestSmartAI(unittest.TestCase):
    """Test cases for SmartComputerPlayer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe()
        self.ai = SmartComputerPlayer('O')
    
    def test_ai_blocks_winning_move(self):
        """Test AI blocks opponent's winning move."""
        # Set up: X has two in a row, AI should block
        self.game.make_move(0, 'X')  # X
        self.game.make_move(1, 'X')  # X
        # Position 2 would win for X, AI should block
        
        move = self.ai.get_move(self.game)
        self.assertEqual(move, 2)
    
    def test_ai_takes_winning_move(self):
        """Test AI takes winning move when available."""
        # Set up: AI has two in a row
        self.game.make_move(0, 'O')  # O
        self.game.make_move(1, 'O')  # O
        # Position 2 would win for AI
        
        move = self.ai.get_move(self.game)
        self.assertEqual(move, 2)
    
    def test_first_move_strategy(self):
        """Test AI chooses corner on first move."""
        move = self.ai.get_move(self.game)
        self.assertIn(move, [0, 2, 6, 8])  # Corner positions


if __name__ == '__main__':
    unittest.main()
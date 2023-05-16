
from unittest.mock import Mock
import Piece
from enums import Player
import ai_engine
import chess_engine


# -----------------unit tests-----------------------

def test_all_steps_are_free():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY
    mock_game_state.is_valid_piece = lambda row, col: False
    mock_self_knight = Piece.Knight('n', 6, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0



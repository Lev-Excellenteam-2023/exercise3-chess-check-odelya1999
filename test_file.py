
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
    assert len(valid_moves) == 0  # there is nothing to eat - all relevant slots are empty


def test_can_not_eat_a_player_from_my_team():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)
    mock_self_knight = Piece.Knight('n', 6, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0  # All relevant slots contain players from my team


def test_how_many_options_to_eat_i_have_from_the_other_team():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_piece_takes(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 8  # all the optional slots are relevant

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves


def test_possible_slots_that_the_player_can_change_position_to():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Player.EMPTY
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 8  # there is 8 optional slots are relevant

    expected_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in expected_moves:
        assert move in valid_moves


def test_to_get_empty_slot_If_there_is_no_opposing_player_in_it():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0   # there is an opposing player in all the optional slots that are relevant

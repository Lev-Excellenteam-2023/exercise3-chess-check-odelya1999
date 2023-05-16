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


def test_to_get_empty_slot_if_there_is_no_opposing_player_in_it():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_1)
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0   # there is an opposing player in all the optional slots that are relevant


def test_to_get_empty_slot_if_there_is_no_player_from_the_same_team_in_it():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)
    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)
    valid_moves = Piece.Knight.get_valid_peaceful_moves(mock_self_knight, mock_game_state)
    assert len(valid_moves) == 0


# ------------------integration tests---------------------


def test_to_get_relevant_slots():
    mock_game_state = Mock()
    mock_game_state.get_valid_piece_takes = [(2, 3), (2, 5), (3, 2), (3, 6)]
    mock_game_state.get_valid_peaceful_moves = [(5, 2), (5, 6), (6, 3), (6, 5)]

    mock_self_knight = Piece.Knight('n', 4, 4, Player.PLAYER_2)

    total_moves = Piece.Knight.get_valid_piece_moves(mock_self_knight, mock_game_state)

    assert len(total_moves) == 8  # maximum 8 slots that are empty \ full

    appeasement_moves = [(2, 3), (2, 5), (3, 2), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)]
    for move in appeasement_moves:
        assert move in total_moves


def test_ai_options_in_board():
    mock_game_state = Mock()
    mock_game_state.get_piece = lambda row, col: Piece.Rook('r', row, col, Player.PLAYER_2)

    mock_self_ai = Mock()
    mock_self_ai.get_piece_value = lambda evaluated_piece, player: 50

    total_score = ai_engine.chess_ai.evaluate_board(mock_self_ai, mock_game_state, Player.PLAYER_1)
    expected_evaluation_score = 50 * 8 * 8
    assert expected_evaluation_score == total_score


# -----------------------system test-------------------

def test_moving_a_player_on_the_board():
    game_state = chess_engine.game_state()
    game_state.move_piece((1, 2), (2, 2), False)
    game_state.move_piece((6, 3), (4, 3), False)
    game_state.move_piece((1, 1), (3, 1), False)
    game_state.move_piece((7, 4), (3, 0), False)

    assert game_state.checkmate_stalemate_checker() == 0

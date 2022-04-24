from collections import namedtuple

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


class Game:
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    # self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class GameOfNim(Game):
    def __init__(self, board):
        possible_moves = [(r, n) for r in range(0, len(board)) for n in range(1, board[r] + 1)]

        # to_move: C = comp, P = player
        self.initial = GameState(to_move='C', utility=0, board=board, moves=possible_moves)

    # returns new state reached from given state and given move
    def result(self, state, move):
        if move not in state.moves:
            return state

        newBoard = state.board.copy()

        newBoard[move[0]] = newBoard[move[0]] - move[1]

        newMoves = [(r, n) for r in range(0, len(newBoard)) for n in range(1, newBoard[r] + 1)]

        newPlyr = 'P' if state.to_move == 'C' else 'C'

        return GameState(to_move=newPlyr,
                         utility=self.compute_utility(newBoard, newPlyr),
                         board=newBoard, moves=newMoves)

    # returns a list of valid actions in the given state
    def actions(self, state):
        return state.moves

    # returns True if given state represents end of game
    def terminal_test(self, state):
        for idx in state.board:
            if idx != 0:
                return False
        return True

    # returns +1 if the Player wins or -1 if Computer wins
    def utility(self, state, player):
        if player == 'C':
            return state.utility
        else:
            return -state.utility

    def compute_utility(self, board, player):
        if sum(board) == 0:
            if player == 'C':
                return 1
            else:
                return -1
        return 0

    '''
    # added under player_query
    def display_board(self, rockList, randPile):
        # display board
        print("-" * 25)
        for i in range(0, randPile):
            print('Pile {}: {}'.format(i + 1, 'O' * rockList[i]))
        print("-" * 25)
    '''

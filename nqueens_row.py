''' 
    nqueens_row.py - The N Queens problem

    Board represented with placed queens a tuple of 
    tuples (i,j) represented queen present at (i,j).

    Action: append a row containing a queen to a
    non fully placed board (length less than N)
    
    Problem solved using A* search

    6/10/2015 - Olafur Bogason
    MIT Licenced
'''

from simpleai.search import SearchProblem, astar
from random import shuffle

class NQueensRow(SearchProblem):
    def __init__(self, N):
        super(NQueensRow, self).__init__()
        self.N             = N
        self.initial_state = ()
        self._actions      = range(N)
        shuffle(self._actions) # randomize actions

    def actions(self, s):
        '''Possible actions from a state.'''
        # generate every possible state then filter out invalid
        tmp = [a for a in self._actions if self._is_valid(self.result(s, a))]
        shuffle(tmp) # randomize actions at each step
        return tmp

    def result(self, s, a):
        '''Result of applying an action to a state.'''
        b = list(s)     # make mutable to add
        b.append(a)
        return tuple(b) # needs to be immutable again to search

    def is_goal(self, state):
        '''Goal: N queens on board and no queen under attack.'''
        return self.N == len(state)

    def heuristic(self, state):
        return self.N - len(state)

    def _is_valid(self, s):
        '''Check if a state is valid.'''
        # valid states: any arrangement of N queens with none attacking each other
        # check horizontal, vertical, right/left diagonals
        attacked = self._attacked
        return attacked(s, (1, 1)) and attacked(s, (1,-1)) and \
               attacked(s, (0, 1)) and attacked(s, (1, 0))
              

    def _attacked(self, s, (delta_x, delta_y)):
        '''Check if adjacent queens exist on board already.'''
        N = self.N
        pairs = zip(s, range(len(s)))   # zip together rows and columns with queen

        for p in pairs:
            original = p

            x, y = p
            while (0 <= x < N) and (0 <= y < N):
                if (x,y) in pairs and (x,y) != original:
                    return False
                x, y = x + delta_x, y + delta_y

            x, y = p
            while (0 <= x < N) and (0 <= y < N):
                if (x,y) in pairs and (x,y) != original:
                    return False
                x, y = x - delta_x, y - delta_y

        return True

    def print_board(self, s):
        board = zip(range(len(s)), s)
        N = len(board)
        for i in range(N):
            for j in range(N):
                if (i,j) in board:
                    print 'Q',
                else:
                    print '.',
            print ''

# Run for the 8x8 case
problem = NQueensRow(N=8)
result = astar(problem, graph_search=False)
problem.print_board(result.state)
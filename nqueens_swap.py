''' 
    nqueens_swao.py - The N Queens problem

    Board represented only with placed queens a tuple of 
    tuples (i,j) represented queen present at (i,j).

    Action: swap queens that are under attack.
    
    Problem solved using A* search

    6/10/2015 - Olafur Bogason
    MIT Licenced
'''

from simpleai.search import SearchProblem, astar
from random import shuffle

class NQueensSwap(SearchProblem):
    def __init__(self, N):
        self.N = N
        init               = [i for i in range(N)]
        shuffle(init)   # randomize the initial array
        self.initial_state = tuple(init)    # states must me immutable
        self._actions      = [ (i, j) for i in range(N) 
                                      for j in range(i,N) 
                                          if i != j ]

    def actions(self, s):
        '''Possible actions from a state.'''
        # generate every possible state then filter out invalid
        tmp = [a for a in self._actions if self._is_valid(self.result(s, a))]
        shuffle(tmp) # randomize actions at each step
        return tmp

    def result(self, s, a):
        '''Result of applying an action to a state.'''
        b          = list(s)     # make board mutable to swap queens
        (i, j)     = a
        b[i], b[j] = b[j], b[i] # swap queens
        return tuple(b)         # make immutable again to search

    def is_goal(self, state):
        '''Goal: N queens on board and no queen under attack.'''
        return self.heuristic(state) == 0

    def heuristic(self, state):
        # scan the state horizontally, vertically and diagonally (left & right)
        # return the number of attacks summed for all queens
        nattacks = self._num_attacks
        return nattacks(state, (0, 1)) + nattacks(state, (1, 0)) + \
               nattacks(state, (1,-1)) + nattacks(state, (1, 1))

    def _is_valid(self, s):
        '''Check if a state is valid.'''
        # all states are valid by default
        return True

    def _num_attacks(self, s, (delta_x, delta_y)):
        '''Check if adjacent queens exist on board already.'''
        N     = self.N
        pairs = zip(range(N), s)    # zip together rows and columns cont. queens
        tot   = 0                   # count attacks

        for p in pairs:
            original = p

            x, y = p
            while (0 <= x < N) and (0 <= y < N):
                if (x, y) in pairs and (x, y) != original:
                    tot += 1
                x, y = x + delta_x, y + delta_y

            x, y = p
            while (0 <= x < N) and (0 <= y < N):
                if (x, y) in pairs and (x, y) != original:
                    tot += 1
                x, y = x - delta_x, y - delta_y

        return tot

    def print_board(self, s):
        N     = self.N
        board = zip(range(N), s)
        for i in range(N):
            for j in range(N):
                if (i,j) in board:
                    print 'Q',
                else:
                    print '.',
            print ''

# Run for the 8x8 case
problem = NQueensSwap(N=8)
result = astar(problem, graph_search=False)
problem.print_board(result.state)
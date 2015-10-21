''' 
    N-Queens problem

    Naive approach, board stored as double N arrays with
    the presence of a queen represented with a 1.

    Raw action: place a queen at one of each of the squares
    on the board (total of N*N at each state).
    
    Problem olved using A* search

    5/10/2015 - Olafur Bogason
    MIT Licenced
'''

from simpleai.search import SearchProblem, astar
from random import shuffle

class NQueensSquare(SearchProblem):
    def __init__(self, N):
        super(NQueensSquare, self).__init__()
        self.N = N
        self.initial_state = tuple([tuple([0 for i in range(N)]) for j in range(N)])
        self._actions      = [(i, j) for i in range(N) for j in range(N)]

    def actions(self, s):
        '''Possible actions from a state.'''
        # generate every possible state then filter out invalid
        tmp = [a for a in self._actions if self._is_valid(self.result(s, a))] 
        shuffle(tmp)
        return tmp

    def result(self, s, a):
        '''Result of applying an action to a state.'''
        (i, j) = a
        b      = list(s)    # make immutable object to place queen
        tmp    = list(b[i])    
        tmp[j] = 1          # place queen to square (i,j) in board

        s    = list(s)      # extra steps for immutability
        s[i] = tuple(tmp)   # required by A* search in simpleai
        return tuple(s)

    def is_goal(self, state):
        '''Goal: N queens on board and no queen under attack.'''
        return self._num_queens_on_board(state) == self.N

    def heuristic(self, state):
        return self.N - self._num_queens_on_board(state)

    def _is_valid(self, s):
        '''Check if a state is valid.'''
        # valid states: any arrangement of <= N queens on board
        # with no queen under attack
        uattack = self._under_attack
        return uattack(s, (0, 1)) and uattack(s, (1, 0)) and \
               uattack(s, (1,-1)) and uattack(s, (1, 1))

    def _num_queens_on_board(self, s):
        '''Returns how many queens are on board s'''
        return sum([sum(i) for i in s])

    def _under_attack(self, s, (delta_x, delta_y)):
        '''Check if any queen is under attack'''
        N = self.N

        # step to easier compute adjacent queens
        pairs = []
        for i, row in enumerate(s):
            for j, cell in enumerate(row):
                if cell == 1:
                    pairs.append((i, j))

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
        for row in s:
            for cell in row:
                if cell == 1:
                    print 'Q',
                else:
                    print '.',
            print ''


# Run for the 8x8 case
problem = NQueensSquare(N=8)
result = astar(problem, graph_search=False)
problem.print_board(result.state)
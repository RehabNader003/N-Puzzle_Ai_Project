from queue import PriorityQueue
import time
import matplotlib.pyplot as plt # type: ignore

class BFS:
    def __init__(self, initial):
        if BFS.isValid(initial):
            self.__size = len(initial)
            self.__initial = initial
            self.__goal = self.__set_goal()
            self.__visited = set()
            self.__pq = PriorityQueue()
            self.__valid = True
            self.__moves=0
            self.__startT = None
            self.__endT = None
            self.__path = []
            self.__isDone = False
        else:
            self.__valid = False
            print('Error : Invalid Board Size or Values')
            #print('Board size :)


    @staticmethod
    def isValid(board):
        n = len(board)

        # Check if the board is squared
        if n != len(board[0]):
            return False
        
        # Check if the board is 8 or 15 or 24 puzzle
        if (n != 3) and (n != 4) and (n != 5):
            return False
        
        #Convert to 1d
        flattened = [val for row in board for val in row]
        # Check if the values are distinct and in the range from 0 to n^2 - 1
        if sorted(flattened) != list(range(n**2)):
            return False
        
        return True

    def __set_goal(self):
        n = self.__size
        board = [[i + j * n + 1 for i in range(n)] for j in range(n)]
        board[-1][-1] = 0
        return board

    def get_initial(self):
        return self.__initial
    
    # Get Node's Children
    def __expand(self, state):
        children = []

        # Get 0 position row,col
        blank = self.__getBlankPos(state)

        # right down left up
        for m in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = [blank[0] + m[0], blank[1] + m[1]]

            # if new position inside board range make a new state of Movement
            if self.__isLegal(new_pos[0], new_pos[1]):
                new_state = [row[:] for row in state]
                new_state[blank[0]][blank[1]] = state[new_pos[0]][new_pos[1]]
                new_state[new_pos[0]][new_pos[1]] = 0
                children.append(new_state)
        return children

    def solve(self, funNum):
        self.__path = []
        levelinc=1
        if not self.__valid:
            return

        if (funNum > 3) or (funNum < 0):
            print('Wrong Function Input')
            return

        self.__startTime()
        value = self.__calcFn(self.__initial, funNum)
        self.__pq.put((value, 0, [self.__initial, 0, []]))  # Include an empty list for the path
        while not self.__pq.empty():
            _, _, Node = self.__pq.get()
            current_state, level, path = Node

            self.__path.append((current_state, level, path))  # Save the path to the current state
            if len(self.__path)>80000:
                return -1
            if self.__isSolved(current_state):
                self.__endTime()
                self.__isDone = True
                self.__moves=len(path + [current_state])
                return path + [current_state]

            if tuple(map(tuple, current_state)) not in self.__visited:
                self.__visited.add(tuple(map(tuple, current_state)))

                level += levelinc
                for child in self.__expand(current_state):
                    value = self.__calcFn(child, funNum)
                    
                    self.__pq.put((value + level, 0, [child, level, path + [current_state]]))
        return -1

    def __isSolved(self, current_state):
        return current_state == self.__goal

    def __calcFn(self, state, funNum):
        if funNum == 0:
            return manhattan_distance(state, self.__goal)
        elif funNum == 1:
            return hamming_distance(state, self.__goal)
        elif funNum == 2:
            return euclidean_distance(state, self.__goal)
        elif funNum == 3:
            return linear_conflict(state, self.__goal)
        # Add the Fourth Heuristic Here and Change if range in solve()

    def __getBlankPos(self, state):
        for i in range(self.__size):
            for j in range(self.__size):
                if state[i][j] == 0:
                    return [i, j]

    def __isLegal(self, row, col):
        rowlen = len(self.__goal)
        return 0 <= row < rowlen and 0 <= col < rowlen

    def __startTime(self):
        self.__startT = time.time()

    def __endTime(self):
        self.__endT = time.time()

    def getTime(self):
        if self.__isDone:
            return self.__endT - self.__startT
        else:
            return 0

    def getNumOfSteps(self):
        if self.__isDone:
            return len(self.__path)-1
        else:
            return 0
    def getMoves(self):
        if self.__isDone:
            return self.__moves-1
        else:
            return 0
    @staticmethod
    def getGraph(x,y,times):
        x_values = x
        y_values = y
        plt.bar(x_values, y_values)
        plt.title('Stats')
        plt.xlabel('Times')
        plt.ylabel('Nodes')
        for i, time in enumerate(times):
            plt.text(i, time + 0.5, str(time), ha='center', va='bottom')
        plt.show()

##############################
# #  Heuristic Functions   # #
##############################

# O(n^2)
def manhattan_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                x2, y2 = element_position(state[x][y], goal)
                cost += abs(x2 - x) + abs(y2 - y)
    return cost

# O(n^2)
def hamming_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                if state[x][y] != goal[x][y]:
                    cost += 1
    return cost

# O(n^2)
def euclidean_distance(state, goal):
    cost = 0
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] != 0:
                x2, y2 = element_position(state[x][y], goal)
                cost += ((x2 - x) ** 2 + (y2 - y) ** 2) ** 0.5
    return cost


def element_position(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return i, j


# O(n^2)
def linear_conflict(state, goal):
    size = len(state)
    conflict_count = 0

    # Helper function to count linear conflicts in a single row or column
    def count_linear_conflicts(line):
        conflicts = 0
        max_val = -1

        for i in range(len(line)):
            if line[i] == 0:
                continue

            if line[i] > max_val:
                max_val = line[i]
            else:
                # Current tile is in conflict with a previous tile
                conflicts += 1

        return conflicts

    # Check rows for conflicts
    for i in range(size):
        conflict_count += count_linear_conflicts(state[i])
        conflict_count += count_linear_conflicts([state[j][i] for j in range(size)])

    return 2 * conflict_count + manhattan_distance(state, goal)




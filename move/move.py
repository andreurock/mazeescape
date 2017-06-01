from move.astar import AStar

class CalculateMove(object):
    def __init__(self, width, height, walls, start, end):
        self.width = width
        self.height = height
        self.walls = walls
        self.start = start
        self.end = end

    def nextMove(self):
        aStar = AStar()
        aStar.init_grid(self.width, self.height, self.walls, self.start, self.end)
        path = aStar.solve()
        nextPosition = path[1]
        nextMove = 'up'

        if nextPosition[0] > self.start[0]:
            nextMove = 'right'
        elif nextPosition[0] < self.start[0]:
            nextMove = 'left'
        elif nextPosition[1] > self.start[1]:
            nextMove = 'down'
        elif nextPosition[1] < self.start[1]:
            nextMove = 'up'

        return nextMove
from random import randint

import pygame
from pygame.locals import QUIT


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self):
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))

    def create_grid(self, randomize=False):
        n = self.cell_height
        m = self.cell_width

        if randomize:
            return [[randint(0,1) for i in range(n)] for j in range(m)]
        else:
            return [[0 for i in range(n)] for j in range(m)]

    def draw_grid(self):
        # grid = self.create_grid(True)

        grid = [[1, 1, 0, 0, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [1, 0, 1, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 0, 1, 1, 1]]
        
        size = self.cell_size
        for j in range (0, self.cell_width):
            for i in range(0, self.cell_height):
                x = j * size + 1
                y = i * size + 1

                self.get_neighbours((x, y))

                if grid[i][j] == 1:
                    color = 'green'
                else:
                    color = 'white'
                pygame.draw.rect(surface=self.screen, color=pygame.Color(color), rect=(x, y, size-1, size-1))

    def new_grid(self):
        size = self.cell_size
        for j in range (0, self.cell_width):
            for i in range(0, self.cell_height):
                x = j * size + 1
                y = i * size + 1
                self.get_neighbours((x, y))

    def get_neighbours(self, cell):
        x, y = cell
        size = self.cell_size
        h = self.height
        w = self.width
        neighbour = 0

        start_x = x - size
        start_y = y - size
        end_x = x + size
        end_y = y + size

        for i in range(start_x, end_x, size):
            if (i > 0) and (i < h):
                for j in range(start_y, end_y, size):
                    if (j > 0) and (j < w):
                        if pygame.Surface.get_at(self.screen, (i, j)) == (0, 255, 0 , 255):
                            neighbour += 1

        if (neighbour < 2) or (neighbour > 3):
            color = 'white'
        else:
            color = 'green'
        pygame.draw.rect(surface=self.screen, color=pygame.Color(color), rect=(x, y, size-1, size-1))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.new_grid()
            pygame.display.flip()
            clock.tick(self.speed)


        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(320, 240, 40)
    game.run()

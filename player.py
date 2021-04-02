import pygame

class Player:
    def __init__(self, cs, x, y, color):
        self.cell_size = cs  # individual segment 10 px
        self.direction = 1  # 1- up, 2 - right, 3 - down, 4 - left
        self.snake_pos = [[x, y],
                          [x, y + self.cell_size],
                          [x, y + self.cell_size * 2],
                          [x, y + self.cell_size * 3]]
        self.color = color
        self.body_inner = (92, 92, 92)
        self.body_outer = (59, 59, 59)

    def is_out(self):
        return self.snake_pos[0][0] < 0 or self.snake_pos[0][0] >= 600 or self.snake_pos[0][1] < 0 or self.snake_pos[0][1] >= 600

    def turn(self, event):
        if event.key == pygame.K_UP and self.direction != 3:
            self.direction = 1
        elif event.key == pygame.K_RIGHT and self.direction != 4:
            self.direction = 2
        elif event.key == pygame.K_DOWN and self.direction != 1:
            self.direction = 3
        elif event.key == pygame.K_LEFT and self.direction != 2:
            self.direction = 4

    def step(self):
        self.snake_pos = self.snake_pos[-1:] + self.snake_pos[:-1]
        if self.direction == 1:
            self.snake_pos[0][0] = self.snake_pos[1][0]
            self.snake_pos[0][1] = self.snake_pos[1][1] - self.cell_size
        if self.direction == 3:
            self.snake_pos[0][0] = self.snake_pos[1][0]
            self.snake_pos[0][1] = self.snake_pos[1][1] + self.cell_size
        if self.direction == 2:
            self.snake_pos[0][1] = self.snake_pos[1][1]
            self.snake_pos[0][0] = self.snake_pos[1][0] + self.cell_size
        if self.direction == 4:
            self.snake_pos[0][1] = self.snake_pos[1][1]
            self.snake_pos[0][0] = self.snake_pos[1][0] - self.cell_size

    def reset(self, x, y):
        self.direction = 1  # 1- up, 2 - right, 3 - down, 4 - left
        self.snake_pos = [[x, y],
                          [x, y + self.cell_size],
                          [x, y + self.cell_size * 2],
                          [x, y + self.cell_size * 3]]

    def new_piece(self, inc):
        for i in range(inc):
            # new segment of snake
            new_piece = list(self.snake_pos[-1])
            if self.direction == 1:
                new_piece[1] += self.cell_size
            if self.direction == 3:
                new_piece[1] -= self.cell_size
            if self.direction == 2:
                new_piece[0] -= self.cell_size
            if self.direction == 4:
                new_piece[0] += self.cell_size
            self.snake_pos.append(new_piece)

    def draw(self, screen):
        head = 1
        for x in self.snake_pos:
            if head == 0:
                pygame.draw.rect(screen, self.body_outer, (x[0], x[1], self.cell_size, self.cell_size))
                pygame.draw.rect(screen, self.body_inner, (x[0] + 1, x[1] + 1, self.cell_size - 2, self.cell_size - 2))
            if head == 1:
                pygame.draw.rect(screen, self.color, (x[0], x[1], self.cell_size, self.cell_size))
                head = 0


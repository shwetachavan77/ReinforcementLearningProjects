import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 10

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TEAL = (0, 100, 255)
BLACK = (0, 0, 0)

class snakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Shweta's Snake Game")
        self.clock = pygame.time.Clock()

        # initializing game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.placeFood()

    def placeFood(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.placeFood()

    def playStep(self):
        
        # 1. User i/p
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. Move
        self.move(self.direction)
        self.snake.insert(0, self.head)

        # 3. Check if Game Over
        gameOver = False
        if self.isCollision():
            gameOver = True
            return gameOver, self.score

        # 4. New Food/ Just Move
        if self.head == self.food:
            self.score += 1
            self.placeFood()
        else:
            self.snake.pop()


        # 5. Update UI and Clock
        self.updateUI()
        self.clock.tick(SPEED)

        #6. Return G.O and Score
        return gameOver, self.score
    
    def isCollision(self):
        # hit boundary?
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # hit itself?
        if self.head in self.snake[1:]:
            return True
        
        return False

    def updateUI(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, TEAL, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))

        pygame.draw.circle(self.display, RED, (self.food.x + BLOCK_SIZE/2, self.food.y + BLOCK_SIZE/2), BLOCK_SIZE/2)

        text = font.render("Score: "+ str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)



if __name__ == '__main__':
    game = snakeGame()

    # game loop
    while True:
        gameOver, score = game.playStep()

        if gameOver:
            break

    print("Final Score")

        
    pygame.quit()

import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 80

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TEAL = (0, 100, 255)
BLACK = (0, 0, 0)

class snakeGameAI:

    def __init__(self, w=640, h=480, render = True):
        self.w = w
        self.h = h
        self.render = render
        
        if self.render:                                                 #Jupyter
            self.display = pygame.display.set_mode((w, h))              
            pygame.display.set_caption("Shweta's Snake Game")           #Jupyter
        else: 
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption("Shweta's Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()                                                    

    
    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.placeFood()
        self.frameIt = 0 
        

    def placeFood(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.placeFood()

    def playStep(self, action):
        
        self.frameIt += 1

        # 1. User i/p
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move
        self.move(action)
        self.snake.insert(0, self.head)

        # 3. Check if Game Over
        reward = 0
        gameOver = False
        if self.isCollision() or self.frameIt > 100*len(self.snake):
            gameOver = True
            reward = -10
            return reward, gameOver, self.score

        # 4. New Food/ Just Move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.placeFood()
        else:
            self.snake.pop()

        # 5. Update UI and Clock
        self.updateUI()
        self.clock.tick(SPEED)

        #6. Return G.O and Score
        return reward, gameOver, self.score
    
    def isCollision(self, point = None):
        if point is None:
            point = self.head

        # hit boundary?
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        
        # hit itself?
        if point in self.snake[1:]:
            return True
        
        return False

    def updateUI(self):
        if not self.render:             #render in Jupyter
            return
        
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, TEAL, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))

        pygame.draw.circle(self.display, RED, (self.food.x + BLOCK_SIZE/2, self.food.y + BLOCK_SIZE/2), BLOCK_SIZE/2)

        text = font.render("Score: "+ str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move(self, action):
        # str, right, left

        clk = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clk.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]):
            newDir = clk[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            newDir = clk[(idx + 1) % 4] # right turn
        elif np.array_equal(action, [0, 0, 1]):
            newDir = clk[(idx - 1) % 4] # left turn

        self.direction = newDir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if self.direction == Direction.UP:
            y -= BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)




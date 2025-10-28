import torch
import numpy as np
import random
from collections import deque
from snake_pygame_ai import snakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot, plot_png

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n = 0
        self.ep = 0 # controls randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEM)
        
        hiddenSize = 256
        self.model = Linear_QNet(11, hiddenSize, 3) 
        self.trainer = QTrainer(self.model, lr = LR, gamma = self.gamma)

    def getState(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = (game.direction == Direction.LEFT)
        dir_r = (game.direction == Direction.RIGHT)
        dir_u = (game.direction == Direction.UP)
        dir_d = (game.direction == Direction.DOWN)

        state = [    # Danger straight
                    (dir_r and game.isCollision(point_r)) or 
                    (dir_l and game.isCollision(point_l)) or 
                    (dir_u and game.isCollision(point_u)) or 
                    (dir_d and game.isCollision(point_d)),

                    # Danger right
                    (dir_u and game.isCollision(point_r)) or 
                    (dir_d and game.isCollision(point_l)) or 
                    (dir_l and game.isCollision(point_u)) or 
                    (dir_r and game.isCollision(point_d)),

                    # Danger left
                    (dir_d and game.isCollision(point_r)) or 
                    (dir_u and game.isCollision(point_l)) or 
                    (dir_r and game.isCollision(point_u)) or 
                    (dir_l and game.isCollision(point_d)),

                    # Move direction
                    dir_l,
                    dir_r, 
                    dir_u, 
                    dir_d,

                    # Food location
                    game.food.x < game.head.x, # food left
                    game.food.x > game.head.x, # food right
                    game.food.y < game.head.y, # food up
                    game.food.y > game.head.y  # food down
            ]
    
        return np.array(state, dtype=int)


    def remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done))

    def trainLMem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_samples = random.sample(self.memory, BATCH_SIZE) #random list of tuples between 0-batch size
        else:
            mini_samples = self.memory

        states, actions, rewards, nextStates, dones = zip(*mini_samples)
        self.trainer.trainStep(states, actions, rewards, nextStates, dones)

    def trainSMem(self, state, action, reward, nextState, done):
        self.trainer.trainStep(state, action, reward, nextState, done)

    def getAction(self, state):
        # random moves tradeoff b/w [exploration, exploitation]

        self.ep = 80 - self.n
        finalMove = [0, 0, 0]
        if random.randint(0, 200) < self.ep:
            move = random.randint(0, 2)
            finalMove[move] = 1 
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            finalMove[move] = 1

        return finalMove

def train():
    plotScores = []
    plotAvgScores = []
    avgScore = 0
    totalScore = 0
    record = 0
    agent = Agent()
    game = snakeGameAI(render = True)
    MAX_GAMES = 500
    
    while agent.n < MAX_GAMES:
        stateOld = agent.getState(game)

        finalMove = agent.getAction(stateOld)

        reward, done, score = game.playStep(finalMove)

        stateNew = agent.getState(game)

        agent.trainSMem(stateOld, finalMove, reward, stateNew, done)

        agent.remember(stateOld, finalMove, reward, stateNew, done)

        if done:
            # train long mem, experience replay
            game.reset()

            agent.n += 1
            agent.trainLMem()

            if score > record:
                record = score

                agent.model.save()

            print(f'Game: {agent.n}, Score: {score}, Record: {record}')

            #plots
            plotScores.append(score)
            totalScore += score
            avgScore = totalScore / agent.n
            plotAvgScores.append(avgScore)

            if (agent.n % 10) == 0:
                # plot(plotScores, plotAvgScores)
                plot_png(plotScores, plotAvgScores, save=True, filename=f"plot_{agent.n}.png")

if __name__ == '__main__':
    train()

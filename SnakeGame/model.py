import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os


class Linear_QNet(nn.Module):

    def __init__(self, inputSize, hiddenSize, outputSize):
        super().__init__()

        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)

        return x
    
    def save(self, fileName='model.pth'):
        modelFolderPath = './model'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        fileName = os.path.join(modelFolderPath, fileName)
        torch.save(self.state_dict(), fileName)

class QTrainer:

    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.model = model
        self.gamma = gamma
        self.optim = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def trainStep(self, state, action, reward, nextState, done):
        state_np = np.array(state)   
        action_np = np.array(action)   
        reward_np = np.array(reward)   
        nextState_np = np.array(nextState)   

        state = torch.tensor(state_np, dtype = torch.float)
        nextState = torch.tensor(nextState_np, dtype = torch.float)
        action = torch.tensor(action_np, dtype = torch.long)
        reward = torch.tensor(reward_np, dtype = torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        #else: the format is (n, x) where n is batch 
        

        #LOGIC:
        # Q = model.predict(state0)
        # nQ = reward + gamma * max(Q(state1)) 

        # predicted Q value with state0
        pred = self.model(state)

        # r + gamma * max(next predicted Q value at state1)
        target = pred.clone()

        for idx in range(len(done)):
            pred_new = reward[idx]
            if not done[idx]:
                pred_new = reward[idx] + self.gamma * torch.max(self.model(nextState[idx]))

            target[idx][torch.argmax(action).item()] =  pred_new

        self.optim.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optim.step()




        
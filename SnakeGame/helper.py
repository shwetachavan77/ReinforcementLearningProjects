import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from IPython import display
import os


plt.ion()

def plot(scores, meanScores):
    display.clear_output(wait=True)
    # display.display(plt.gcf())
    plt.clf()
    plt.title('Training Stats')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(meanScores)
    plt.ylim(ymin=0)
    if scores:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if meanScores: 
        plt.text(len(meanScores)-1, meanScores[-1], str(meanScores[-1]))

    # display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.pause(0.001)

def plot_png(scores, meanScores, save=False, filename="plot.png"):
    plt.clf()
    plt.title('Training Stats')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(meanScores, label='Mean Score')
    plt.ylim(ymin=0)
    if scores:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if meanScores: 
        plt.text(len(meanScores)-1, meanScores[-1], str(meanScores[-1]))
    if save:
        save_png(filename)

        

def save_png(fileName):
        modelFolderPath = './plot'
        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        fileName = os.path.join(modelFolderPath, fileName)
        plt.savefig(fileName)
        plt.close()


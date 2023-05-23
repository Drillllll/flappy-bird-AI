import random
import numpy as np
import random
import matplotlib.pyplot as plt


class QLearningAgent:
    def __init__(self):
        #3D numpy array representing states and rewards.
        # first two dimentions - x and y - (discrete) - horizontal position of next pipe and vertical distance between player and next pipe
        # 3rd dimention - two actions that can be taken in each state - jump or not jump
        # reward for jump action is located in index 1 in 3rd dimention [a][b][1]
        # reward for not jumping action is located in index 0 in 3rd dimention [a][b][0]
        self.q_table = np.zeros((7, 21, 2), dtype=float)
        self.scores = []

        # saving and loading q_table from file
        self.save = False
        self.load = True

        # q_table update parameters
        self.learning_rate = 0.6
        self.discount_rate = 1

    def choose_action(self, x, y):
        jump = 0
        if (self.q_table[x][y][1] > self.q_table[x][y][0]):
            jump = 1
        return jump

    def update_q_table(self, x_prev,y_prev, action ,reward,x_new,y_new):

        # previous formulas that were less optimal
        #self.q_table[x_prev][y_prev][action] = 0.4 * self.q_table[x_prev][y_prev][action] + (0.6) * (
                    #reward + max(self.q_table[x_new][y_new][0], self.q_table[x_new][y_new][1]))
        # self.q_table[x_prev][y_prev][action] = state[action] + A*(reward + G*(max(new_state[0], new_state[1])) - state[action])

        state = self.q_table[x_prev][y_prev]
        new_state = self.q_table[x_new][y_new]
        A = self.learning_rate
        G = self.discount_rate

        self.q_table[x_prev][y_prev][action] = (1-A)*state[action] + A*(reward + G*(max(new_state[0], new_state[1])))

    def convert(self, playery, pipex, pipey):
        """
            converts the player and next pipe position to the state indexes
        """
        x = min(280, pipex)
        y = pipey - playery
        if (y < 0):
            y = abs(y) + 408  # indexes from 0-10 - player is above the pipe, indexes greater than 10 - player is below the pipe
        return int(x/40 - 1), int(y/40)

    def save_q_table(self):
        np.save('q_table.npy', self.q_table)

    def load_q_table(self):
        self.q_table = np.load('q_table.npy')

    def print_state(self, x, y):
        print (self.q_table[x][y][1], self.q_table[x][y][0])

    def display_scores(self):
        plt.semilogy(range(len(self.scores)), self.scores, 'o')
        #plt.scatter(range(len(self.scores)), self.scores)
        plt.xlabel('generacje')
        plt.ylabel('wynik')
        plt.title('wyniki w kolejnych generacjach')
        plt.show()



import random
import numpy as np
import random

class Q:
    def __init__(self):
        # Initialize the Q-table to zeros
        self.q_table = np.zeros((7,21,2),dtype = float)


        # Set hyperparameters
        self.alpha = 0.7
        self.gamma = 0.9
        self.epsilon = 0.1

    def convert(self, playery, pipex, pipey):
        x = min(280, pipex)
        y = pipey - playery
        if (y < 0):
            y = abs(y) + 408
        return int(x / 40 - 1), int(y / 40)


    def print_state(self, x, y):
        print (self.q_table[x][y][1], self.q_table[x][y][0])

    def choose_action(self, x, y):
        max = 0
        jump = 0

        if (self.q_table[x][y][1] > self.q_table[x][y][0]):
            max = self.q_table[x][y][1]
            jump = 1

        return jump

    #scale the x and y distance to get the index of state in q table
    #returns scaled_x and scaled_y distances
    def scale_distances(self, x, y):
        # minx, miny, maxx, maxy
        # 0 -100 250 267
        #x += 120  #0 - 240 + 120 (0-360) /25  q table xsize -  11
        y += 120 #0 - 280 + 120 (0-400) /25  q table ysize - 17
        x = int(x//25)
        y = int(y//25)
        if x > 10:
            x = 15
        if x < 0:
            x = 0
        if y > 16:
            y = 16
        if y < 0:
            y = 0
        return x, y

    # jump - action == 1
    def update_q_table(self, x_prev,y_prev, action ,reward,x_new,y_new):
       # learning_rate = 0.2
       # discount_factor = 0.9

       # old_q_value = self.q_table[x_prev][y_prev][action]
       # max_future_q_value = max(self.q_table[x_new][y_new])

      #  new_q_value = (1 - learning_rate) * old_q_value + learning_rate * (
                    #reward + discount_factor * max_future_q_value)
       # self.q_table[x_prev][y_prev][action] = new_q_value

        self.q_table[x_prev][y_prev][action] = 0.4 * self.q_table[x_prev][y_prev][action] + (0.6) * (
                    reward + max(self.q_table[x_new][y_new][0], self.q_table[x_new][y_new][1]))
        #self.q_table[x_prev][y_prev][action] =\
            #self.q_table[x_prev][y_prev][action] + self.alpha * (reward + self.gamma * max(self.q_table[x_new][y_new][0], self.q_table[x_new][y_new][1]) - self.q_table[x_prev][y_prev][action])



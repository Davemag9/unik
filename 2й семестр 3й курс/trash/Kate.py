
import gymnasium as gym
import numpy as np
import random
import math
import matplotlib.pyplot as plt

buckets = (5, 5, 5, 5, 5, 5, 2, 2)

average_window = 500
average_rewards_list = []

env = gym.make("LunarLander-v2")
observation = env.observation_space
n = env.action_space.n

q_table = np.load('/Users/davemag9/VSCode/sosuHui100ktimes.npy')

ranges = list(zip(env.observation_space.low, env.observation_space.high))
print(ranges)
ranges[0] = [-1, 1]
ranges[1] = [-1, 1]
ranges[2] = [-1, 1]
ranges[3] = [-1, 1]
ranges[4] = [-1, 1]
ranges[5] = [-1, 1]
ranges[6] = [0, 1]
ranges[7] = [0, 1]

def discretize_state(state):
    bucket_indexes = []
    for i in range(len(state)):
        if state[i] <= ranges[i][0]:
            bucket_index = 0
        elif state[i] >= ranges[i][1]:
            bucket_index = buckets[i] - 1
        else:
            bound_width = ranges[i][1] - ranges[i][0]
            offset = (buckets[i] - 1) * ranges[i][0] / bound_width
            scaling = (buckets[i] - 1) / bound_width
            bucket_index = int(round(scaling * state[i] - offset))
        bucket_indexes.append(bucket_index)
    return tuple(bucket_indexes)

def evaluation(n, Q_table):
    res = 0
    for i in range(n):
        print(str(i/n * 100) + '%')
        env_test = gym.make('LunarLander-v2', render_mode="rgb_array")
        state = env_test.reset()[0]
        discrete_state_test = discretize_state(state)
        done = False
        total_reward = 0
        for j in range(1000):
            action = np.argmax(Q_table[discrete_state_test])  
            next_state, reward, done, info, _ = env_test.step(action)
            discrete_state_test = discretize_state(next_state)
            total_reward +=  reward
            env_test.render()
            if done:
                break
        env_test.close()
        if total_reward >= 200:
            res += 1
    print(res/n * 100)

evaluation(100, q_table)
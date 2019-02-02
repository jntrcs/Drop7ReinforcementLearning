# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:06:15 2019

@author: jntrcs
"""

import Drop7Gym as gym
import random

env = gym.Drop7Env()

data=env.reset()


env.render()
#This is the human readable version of the board.
#For a better idea of what you're looking at check out https://www.youtube.com/watch?v=L_RLjEruSx8
#Note, the game imitates "hardcore"/"blitz" mode and contrary to what you see in the video, you'll
#never be given a gray ball to drop.

print("Action Space", env.actionSpace)
data, reward, gameOver, messages= env.step(1) #This is how your agent will indicate what column to drop the next ball into

env.render()




###Here's a demo simulation of 1000 games, where each choice is made randomly
scores=[]
gameLength=[]
for i in range(1000):
    env.reset()
    gameOver=False
    totalReward=0
    steps=0
    while not gameOver:
        data, reward, gameOver, messages= env.step(random.randint(0,6))
        if reward<0: #In this case we want the true score, not the penalty for choosing an invalid column
            reward=0
        totalReward+=reward
        steps+=1
    scores.append(totalReward)
    gameLength.append(steps)
    

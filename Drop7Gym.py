# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 11:05:39 2019

@author: jntrcs
"""

from drop7 import *


class Drop7Env:
    
    def __init__(self):
        #print("Init Gym")
        self.game = None
        self.actionSpace = range(7)
        
        

    def reset(self):
        self.game=MachineGame()
        #Call something to start the game
        return self.game.getGameData()
    
    def step(self, choice):
        oldScore=self.game.score
        
        if self.game.takeTurn(choice):
            #print("succeeded")
            #your reward is however much your score increased that round
            return self.game.getGameData(), self.game.score-oldScore, self.game.gameOver, {}
            
        else:
            #Handle the case where you attempted to place a ball in a full column
            #Currently allow it to happen, ignore it, and return -20000 reward to encourage agents away from it.
            return self.game.getGameData(), -20000, self.game.gameOver, {}
        
    def render(self):
        self.game.visualizeGame()
        
   # def gameToTensor(self, gameData):
        #This function just provides one way to transform the data in the game to a tensor format,
        #different ways of representing the data may yield better results for different agents
        
        
        

#env = Drop7Env() #This is like gym.make('Drop7')

#env.reset()
#env.render()
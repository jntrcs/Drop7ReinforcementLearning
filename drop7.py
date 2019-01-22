# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 18:57:27 2019

@author: jntrcs
"""

import random

class Board:
    def __init__(self):
        #print("Hi")
        self.board = [[Space() for i in range(7)] for j in range(8)]
        #self.board[0][0].set(3)
        self.randomStart()

        #print(self.board)
        
    def isOver(self): #Game is over if anything is above row 7 or if all of row 7 is full
        for i in range(7):
            if self.board[7][i].isNotEmpty():
                return True
        for i in range(7): 
            if self.board[6][i].isEmpty():
                return False
        return True
    
    def randomStart(self):
        numBalls = random.randint(6,12)
        for i in range(numBalls):
            legalCol=False
            while not legalCol:
                col= random.randint(1,7)
                legalCol=self.canDrop(col)
            num = random.randint(1,7)
            self.drop(col, num)
        self.resolve(0)
        
    def canDrop(self, col):
        return self.board[6][col-1].isEmpty()
        
    def drop(self, col, num):
        done = False
        spot=0
        while not done:
            if self.board[spot][col-1].isEmpty():
                self.board[spot][col-1].set(num)
                done=True
            else:
                spot+=1
                
    def addRow(self):
        for row in range(6, -1,-1):
            for col in range(7):
                if self.board[row][col].isNotEmpty():
                    self.board[row+1][col] = self.board[row][col].copy()
                    #self.board[row][col].emptyMe()
        for col in range(7):
            self.board[0][col]=Space(empty=False, gray=True)
            
    
    def resolve(self, multiplier):
        #self.printBoard()
        #These are the point totals you get for chaining
        if multiplier>17:
            pointsPerBall=20000
        else:
            pointsPerBall = [7,39, 109, 224, 391,617, 907, 1267, 1701, 2213, 2809, 3491, 4265, 5133, 6099,
                             7168, 8347, 9622][multiplier]
        roundScore=0
        needsPopped = set()
        for row in range(7):
            for col in range(7):
                if self.shouldPop(row, col):
                    needsPopped.add((row, col))
        #print(needsPopped)       
        if len(needsPopped)>0:
            for row, col in needsPopped:
                self.board[row][col].pop()
                self.crackNeighbors(row, col) #if a ball pops, it changes the gray ones
            roundScore+=len(needsPopped)*pointsPerBall    
            self.gravity(needsPopped) #if some were popped, let gravity do its thing
            endScore, endMultiplier = self.resolve(multiplier+1)
            return roundScore+endScore, endMultiplier #If some were deleted recursively call the resolve function to start over
        return roundScore, multiplier
    
    
    def gravity(self, poppedList):
        wherePopsOccurred= [set() for i in range(7)]
        for row, col in poppedList:
            wherePopsOccurred[col].add(row)
        #print(wherePopsOccurred)
        for col in range(7):
            if len(wherePopsOccurred[col])>0:
                for row in range(1,7):
                  if  self.board[row][col].isNotEmpty():
                      needsToDrop =0
                      for x in wherePopsOccurred[col]:
                          if x<row:
                              needsToDrop+=1
                      if needsToDrop>0:
                          self.board[row-needsToDrop][col]=self.board[row][col].copy()
                          self.board[row][col].emptyMe()
                          
    def cleared(self):
        for i in range(7):
            if self.board[0][i].isNotEmpty():
                return False
        return True
    
    def printBoard(self):
        printout='_____________\n'
        for row in range(6, -1,-1):
            for col in range(7):
                printout+=self.board[row][col].printString()
            printout+='\n'
        printout+='_____________'
        print(printout)
            
                    

    def crackNeighbors(self, row, col):
        if row>0:
            self.board[row-1][col].crack()
        if row<6:
            self.board[row+1][col].crack()
        if col>0:
            self.board[row][col-1].crack()
        if col<6:
            self.board[row][col+1].crack()
        
    def shouldPop(self, row, col):
        num = self.board[row][col].getNum()
        if num is not None:
            horizontal=1
            index= col
            toRightDone=False
            while (not toRightDone) and (horizontal <= num) :
                index+=1
                if index >6:
                    toRightDone=True
                else:
                    if self.board[row][index].isNotEmpty():
                        horizontal+=1
                    else:
                        toRightDone=True
            toLeftDone=False
            index=col
            while (not toLeftDone) and (horizontal <= num) :
                index-=1
                if index <0:
                    toLeftDone=True
                else:
                    if self.board[row][index].isNotEmpty():
                        horizontal+=1
                    else:
                        toLeftDone=True
            shouldPop  = horizontal==num
            if not shouldPop:
                vertical=1
                index= row
                upDone=False
                while (not upDone) and (vertical <= num) :
                    index+=1
                    if index >6:
                        upDone=True
                    else:
                        if self.board[index][col].isNotEmpty():
                            vertical+=1
                        else:
                            upDone=True
                downDone=False
                index=row
                while (not downDone) and (vertical <= num) :
                    index-=1
                    if index <0:
                        downDone=True
                    else:
                        if self.board[index][col].isNotEmpty():
                            vertical+=1
                        else:
                            downDone=True
                shouldPop= vertical==num
            return shouldPop
                    
                

            
        
        

class Space:
    
    def __init__(self, empty=True, num=None, gray=False, cracked=False):
        self.empty=empty
        self.num=num
        self.gray=gray
        self.cracked=cracked
        
    def isNotEmpty(self):
        return not self.empty
    
    def isEmpty(self):
        return self.empty
    
    def set(self, num):
        if self.isNotEmpty():
            raise ValueError('The space was not empty but you tried to fill it anyway')
        self.num=num
        self.empty=False
        
    def getNum(self):
        return self.num
    
    def pop(self):
        self.empty=True
        self.num=None
        self.gray=False
        self.cracked=False
    
    def crack(self):
        if self.num is not None or self.empty:
            return True
        if self.gray:
            self.gray=False
            self.cracked=True
            return True
        if self.cracked:
            self.cracked=False
            self.num = random.randint(1,7)
            return True
        
    def emptyMe(self):
        self.__init__()
        
    def copy(self):
        return Space(self.empty, self.num, self.gray, self.cracked)
    
    def printString(self):
        if self.empty:
            return('- ')
        if self.gray:
            return('O ')
        if self.cracked:
            return('0 ')
        return(str(self.num)+' ')

    
class Game:
    def __init__(self):
        self.score = 0
        self.board=Board()
        #self.board.printBoard()
        self.nextBall=random.randint(1, 7)
        self.ballsTillNext=5
        self.gameOver=False
        
    def startGame(self):
        while not self.gameOver:
            print "Current Score:", self.score
            print "# of balls till new row:", self.ballsTillNext
            self.board.printBoard()
            print "Current ball:", self.nextBall
            col = input("What column would you like to place the ball in (1-7)? ")
            while not self.board.canDrop(col):
                col = input("What column would you like to place the ball in (1-7)? ")
            self.handleDrop(col)
            
            print(col)
            
            
    def handleDrop(self, col): #Note column here is [1, 7] not [0,6]
        self.board.drop(col, self.nextBall)
        score, mult = self.board.resolve(0)
        self.score+=score
        if self.board.cleared():
            self.score+=90000
        self.gameOver=self.board.isOver()
        self.nextBall=random.randint(1,7)
        self.ballsTillNext-=1
        if self.ballsTillNext==0:
            self.ballsTillNext=5
            self.score += 17000
            self.board.addRow()
            if self.board.isOver():
                self.gameOver=True
                return
            score, _=self.board.resolve(mult)
            if self.board.cleared():
                self.score+=90000
            self.score+=score
            
    def finalScore(self):
        return self.score
            
            
        
a = Game()
a.startGame()
print "Game over! Final Score:", a.finalScore()

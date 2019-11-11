
import sys

class Sudoku:
	def __init__(self):

		self.problemSolution = [
			[5,3,4,6,7,8,9,1,2],
			[6,7,2,1,9,5,3,4,8],
			[1,9,8,3,4,2,5,6,7],
			[8,5,9,7,6,1,4,2,3],
			[4,2,6,8,5,3,7,9,1],
			[7,1,3,9,2,4,8,5,6],
			[9,6,1,5,3,7,2,8,4],
			[2,8,7,4,1,9,6,3,5],
			[3,4,5,2,8,6,1,7,9]
		]

		self.problem = [
			[5,3,0,0,7,0,0,0,0],
			[6,0,0,1,9,5,0,0,0],
			[0,9,8,0,0,0,0,6,0],
			[8,0,0,0,6,0,0,0,3],
			[4,0,0,8,0,3,0,0,1],
			[7,0,0,0,2,0,0,0,6],
			[0,6,0,0,0,0,2,8,0],
			[0,0,0,4,1,9,0,0,5],
			[0,0,0,0,8,0,0,7,9]
		]

		self.boardMap = self.mapFixedNumbers()

	def mapFixedNumbers(self):
		temp = []
		for row in self.problem:
			tempRow=[]
			for i in row:
				if i == 0:
					tempRow.append(i)
				else:
					tempRow.append(1)
			temp.append(tempRow)
		return temp

	def solve(self):
		self.recursion(0,0,1)
		if self.problem == self.problemSolution:
			print( "solved" )
		for i in self.problem:
			print(i)

	def recursion(self,c,r,v):
		if r == 9: return
		if self.isFixed(c, r):
			c,r = self.moveToNext(c, r)
		while self.breaksRules(c, r, v) and v in range(10):
			v += 1
		if v == 10:
			self.problem[r][c] = 0
			c,r = self.moveBack(c, r)
			v = self.problem[r][c]	
			self.recursion(c, r, v+1)
		else:
			self.problem[r][c] = v
			c,r = self.moveToNext(c, r)			
			v = 1
			self.recursion(c, r, v) 

	# takes in current position
	# skips fixed ones
	def moveToNext(self, c, r):	
		if c == 8: c = 0; r += 1
		else: c += 1
		while self.isFixed(c, r):
			if c == 8: 
				c = 0
				r += 1
				if r == 9: break
			else: c += 1
		return [c,r]

	def moveBack(self, c, r):
		if c == 0: c = 8; r -= 1
		else: c -= 1
		while self.isFixed(c, r):
			if c == 0: 
				c = 8
				r -= 1
			else: c -= 1
		return [c,r]

	def breaksRules(self, c, r, v):	
		breaksC = self.breaksColumnRule(c, v)
		breaksR = self.breaksRowRule(r, v)
		breaksB = self.breaksBoxRule(c, r, v)
		if breaksC or breaksR or breaksB:
			return True
		return False

	# determines whether the number in the box is 
	# a part of the original given numbers or not
	# (and thus is fixed, cannot be changed)
	def isFixed(self, colIdx, rowIdx):
		if self.boardMap[rowIdx][colIdx] == 0:
			return False
		return True

	def breaksColumnRule(self, colIdx, value):
		for row in self.problem:
			if value == row[colIdx]:
				return True
		return False

	def breaksRowRule(self, rowIdx, value):
		if value in self.problem[rowIdx]:
			return True
		return False

	def breaksBoxRule(self, colIdx, rowIdx, value):
		xLo, yLo = self.currentBoxOrigin(rowIdx, colIdx)
		xHi, yHi = xLo + 3, yLo + 3 
		for row in self.problem[yLo:yHi]:
			if value in row[xLo:xHi]:
				return True
		return False

	def currentBoxOrigin(self, rowIdx, colIdx ):
		xBox = self.checkWhichThird(colIdx)
		yBox = self.checkWhichThird(rowIdx)
		return [3 * i for i in [xBox, yBox]]

	def checkWhichThird(self,idx):
		j = 0
		for i in range(9):
			if i % 3 == 0: j += 1
			if idx == i: return(j-1)


	# ****************************
	# *        *        *        *
	# *  1,1   *   2,1  *   3,1  *
	# *        *        *        *
	# ****************************
	# *        *        *        *
	# *  1,2   *   2,2  *   3,2  *
	# *        *        *        *
	# ****************************
	# *        *        *        *
	# *  1,3   *   2,3  *   3,3  *
	# *        *        *        *
	# ****************************

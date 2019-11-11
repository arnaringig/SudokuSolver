
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
				if i == 0: tempRow.append(i)
				else: tempRow.append(1)
			temp.append(tempRow)
		return temp

	def solve(self):
		self.recursion(0,0,1)               # We start the recursion at the top right corner of the sudoku problem and try the inital value as 1
		if self.problem == self.problemSolution:
			print( "solved" )
		for i in self.problem:
			print(i)

	def recursion(self,c,r,v):
		if r == 9: return                   # If we have reached a place where the row is number 9, we have found all the values and solved the problem, so we return.
		if self.isFixed(c, r):              # check if the first square is a fixed number or empty.
			c,r = self.moveToNext(c, r) # If fixed we move one right (or until there´s an empty square)
		while self.breaksRules(c, r, v) and v in range(10):  
			v += 1                      # Then we try numbers from 1 to 9 and see if there´s a number that doesn´t break the rules.
		if v == 10:                         # If v gets to 10 it means no number didn´t break the rules so we have to backtrack.
			self.problem[r][c] = 0.     # When backtracking we must "empty" the current square so we can check if it´s empty when moving forward again.
			c,r = self.moveBack(c, r)   # Moves us to the next point that isn´t fixed.
			v = self.problem[r][c]      # Let´s get the value from the square we´re backtracking to so we can increase it by 1
			self.recursion(c, r, v+1)   # We backtracked to this point and now we go forward again by increasing this square´s value by 1
		else:
			self.problem[r][c] = v      # So we found a value between 1 and 9 and it doesn´t break the rules. We put that value in the square
			c,r = self.moveToNext(c, r) # Then we find the next "legal" square, one that isn´t fixed	
			v = 1                       # and we set v to 1 so 1 will be the first value we try in the next iteration
			self.recursion(c, r, v)     # So we have set c, r and v to the appropriate values and perform a recursive call to the method.

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

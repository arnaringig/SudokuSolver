import sys
from Sudoku import Sudoku

def main():
	sudoku = Sudoku()
	sys.setrecursionlimit(10000)

	sudoku.solve()

if __name__ == "__main__":
	main()

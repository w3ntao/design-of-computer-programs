# -----------------
# User Instructions
#
# Write the function show that takes a board
# as input and outputs a pretty-printed
# version of it as shown below.


## Handle complete boards

def a_board():
	return map(list, ['|||||||||||||||||',
					  '|J............I.|',
					  '|A.....BE.C...D.|',
					  '|GUY....F.H...L.|',
					  '|||||||||||||||||'])

def show(board):
	"Print the board."
	for row in board:
		for item in row:
			print item,
		print

# >>> a_board()
# [['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|'],
#  ['|', 'J', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'I', '.', '|'],
#  ['|', 'A', '.', '.', '.', '.', '.', 'B', 'E', '.', 'C', '.', '.', '.', 'D', '.', '|'],
#  ['|', 'G', 'U', 'Y', '.', '.', '.', '.', 'F', '.', 'H', '.', '.', '.', 'L', '.', '|'],
#  ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|']]

# >>> show(a_board())
# | | | | | | | | | | | | | | | | |
# | J . . . . . . . . . . . . I . |
# | A . . . . . B E . C . . . D . |
# | G U Y . . . . F . H . . . L . |
# | | | | | | | | | | | | | | | | |

if __name__ == '__main__':
	show(a_board())
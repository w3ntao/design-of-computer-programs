# -----------------
# User Instructions
#
# Write a function, word_score, that takes as input a word, and
# returns the sum of the individual letter scores of that word.
# For testing, you can assume that you have access to a file called
# 'words4k.txt'


POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
	"The sum of the individual letter point scores for this word."
	return sum([POINTS[L] for L in word])

if __name__ == '__main__':
	print word_score("RAHN")
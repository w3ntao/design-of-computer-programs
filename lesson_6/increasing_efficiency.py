# -----------------
# User Instructions
#
# The find_prefixes function takes a hand, a prefix, and a
# results list as input.
# Modify the find_prefixes function to cache previous results
# in order to improve performance.

def prefixes(word):
	"A list of the initial sequences of a word, not including the complete word."
	return [word[:i] for i in range(len(word))]

def readwordlist(filename):
	"Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
	wordset = set(file(filename).read().upper().split())
	prefixset = set(p for word in wordset for p in prefixes(word))
	return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

class anchor(set):
	"An anchor is where a new word can be placed; has a set of allowable letters."

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ANY = anchor(LETTERS) # The anchor that can be any letter

def is_letter(sq):
	return isinstance(sq, str) and sq in LETTERS

def is_empty(sq):
	"Is this an empty square (no letters, but a valid position on board)."
	return sq  == '.' or sq == '*' or isinstance(sq, set)

def add_suffixes(hand, pre, start, row, results, anchored=True):
	"Add all possible suffixes, and accumulate (start, word) pairs in results."
	i = start + len(pre)
	if pre in WORDS and anchored and not is_letter(row[i]):
		results.add((start, pre))
	if pre in PREFIXES:
		sq = row[i]
		if is_letter(sq):
			add_suffixes(hand, pre+sq, start, row, results)
		elif is_empty(sq):
			possibilities = sq if isinstance(sq, set) else ANY
			for L in hand:
				if L in possibilities:
					add_suffixes(hand.replace(L, '', 1), pre+L, start, row, results)
	return results

def legal_prefix(i, row):
	"""A legal prefix of an anchor at row[i] is either a string of letters
	already on the board, or new letters that fit into an empty space.
	Return the tuple (prefix_on_board, maxsize) to indicate this.
	E.g. legal_prefix(a_row, 9) == ('BE', 2) and for 6, ('', 2)."""
	s = i
	while is_letter(row[s-1]): s -= 1
	if s < i: ## There is a prefix
		return ''.join(row[s:i]), i-s
	while is_empty(row[s-1]) and not isinstance(row[s-1], set): s -= 1
	return ('', i-s)

###Modify this function. You may need to modify
# variables outside this function as well.

#global prev_hand, prev_results
prev_hand, prev_results = '', set() # cache for find_prefixes

def find_prefixes(hand, pre='', results=None):
	"""Find all prefixes (of words) that can be made from letters in hand."""
	global prev_hand, prev_results
	if prev_hand == hand:
		return prev_results
	if results is None:
		results = set()
	if pre == '':
		prev_hand, prev_results = hand, results

	if pre in PREFIXES:
		results.add(pre)
		for L in hand:
			find_prefixes(hand.replace(L, '', 1), pre+L, results)

	return results

if __name__ == '__main__':
	print find_prefixes("ABCEHKN")
	print ""
	print prev_results
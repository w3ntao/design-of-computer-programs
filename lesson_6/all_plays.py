# -----------------
# User Instructions
#
# The all_plays function takes a hand and a current board as input.
# Modify the all_plays function to return the resulting set of
# all plays.

def removed(letters, remove):
	"Return a str of letters, but with each letter in remove removed once."
	for L in remove:
		letters = letters.replace(L, '', 1)
	return letters

def prefixes(word):
	"A list of the initial sequences of a word, not including the complete word."
	return [word[:i] for i in range(len(word))]

def transpose(matrix):
	"Transpose e.g. [[1,2,3], [4,5,6]] to [[1, 4], [2, 5], [3, 6]]"
	# or [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
	return map(list, zip(*matrix))

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

prev_hand, prev_results = '', set() # cache for find_prefixes

def find_prefixes(hand, pre='', results=None):
	## Cache the most recent full hand (don't cache intermediate results)
	global prev_hand, prev_results
	if hand == prev_hand: return prev_results
	if results is None: results = set()
	if pre == '': prev_hand, prev_results = hand, results
	# Now do the computation
	if pre in WORDS or pre in PREFIXES: results.add(pre)
	if pre in PREFIXES:
		for L in hand:
			find_prefixes(hand.replace(L, '', 1), pre+L, results)
	return results

def row_plays(hand, row):
	"Return a set of legal plays in row.  A row play is an (start, 'WORD') pair."
	results = set()
	## To each allowable prefix, add all suffixes, keeping words
	for (i, sq) in enumerate(row[1:-1], 1):
		if isinstance(sq, set):
			pre, maxsize = legal_prefix(i, row)
			if pre: ## Add to the letters already on the board
				start = i - len(pre)
				add_suffixes(hand, pre, start, row, results, anchored=False)
			else: ## Empty to left: go through the set of all possible prefixes
				for pre in find_prefixes(hand):
					if len(pre) <= maxsize:
						start = i - len(pre)
						add_suffixes(removed(hand, pre), pre, start, row, results,
									 anchored=False)
	return results

def find_cross_word(board, i, j):
	"""Find the vertical word that crosses board[j][i]. Return (j2, w),
	where j2 is the starting row, and w is the word"""
	sq = board[j][i]
	w = sq if is_letter(sq) else '.'
	for j2 in range(j, 0, -1):
		sq2 = board[j2-1][i]
		if is_letter(sq2): w = sq2 + w
		else: break
	for j3 in range(j+1, len(board)):
		sq3 = board[j3][i]
		if is_letter(sq3): w = w + sq3
		else: break
	return (j2, w)

def neighbors(board, i, j):
	"""Return a list of the contents of the four neighboring squares,
	in the order N,S,E,W."""
	return [board[j-1][i], board[j+1][i],
			board[j][i+1], board[j][i-1]]

def set_anchors(row, j, board):
	"""Anchors are empty squares with a neighboring letter. Some are resticted
	by cross-words to be only a subset of letters."""
	for (i, sq) in enumerate(row[1:-1], 1):
		neighborlist = (N,S,E,W) = neighbors(board, i, j)
		# Anchors are squares adjacent to a letter.  Plus the '*' square.
		if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
			if is_letter(N) or is_letter(S):
				# Find letters that fit with the cross (vertical) word
				(j2, w) = find_cross_word(board, i, j)
				row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
			else: # Unrestricted empty square -- any letter will fit.
				row[i] = ANY

def horizontal_plays(hand, board):
	"Find all horizontal plays -- ((i, j), word) pairs -- across all rows."
	results = set()
	for (j, row) in enumerate(board[1:-1], 1):
		set_anchors(row, j, board)
		for (i, word) in row_plays(hand, row):
			results.add(((i, j), word))
	return results

ACROSS, DOWN = (1, 0), (0, 1) # Directions that words can go

def all_plays(hand, board):
	"""All plays in both directions. A play is a (pos, dir, word) tuple,
	where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
	hplays = horizontal_plays(hand, board)            # set of ((i, j), word)
	vplays = horizontal_plays(hand, transpose(board)) # set of ((j, i), word)
	return (set(((i, j), ACROSS, word) for ((i, j), word) in hplays) |
			set(((i, j), DOWN, word)   for ((j, i), word) in vplays))
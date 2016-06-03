# -----------------
# User Instructions
#
# Write a function, readwordlist, that takes a filename as input and returns
# a set of all the words and a set of all the prefixes in that file, in
# uppercase. For testing, you can assume that you have access to a file
# called 'words4k.txt'

def prefixes(word):
	"A list of the initial sequences of a word, not including the complete word."
	return [word[:i] for i in range(len(word))]

def readwordlist(filename):
	"""Read the words from a file and return a set of the words
	and a set of the prefixes."""
	wordset   = set(file(filename).read().upper().split())
	prefixset = set(p for word in wordset for p in prefixes(word))
	return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

def test():
	assert len(WORDS)    == 3892
	assert len(PREFIXES) == 6475
	assert 'UMIAQS' in WORDS
	assert 'MOVING' in WORDS
	assert 'UNDERSTANDIN' in PREFIXES
	assert 'ZOMB' in PREFIXES
	return 'tests pass'

if __name__ == '__main__':
	print test()
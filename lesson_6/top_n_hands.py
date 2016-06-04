# -----------------
# User Instructions
#
# Write a function, topn, that takes as input a hand, the set of
# current letters on the board, and a number n, and returns the
# n best words we can play, sorted by word score.
# For testing, you can assume that you have access to a file called
# 'words4k.txt'
#
# Enter your code at line 83.

import time

def prefixes(word):
	"A list of the initial sequences of a word, not including the complete word."
	return [word[:i] for i in range(len(word))]

def readwordlist(filename):
	file = open(filename)
	text = file.read().upper()
	wordset = set(word for word in text.splitlines())
	prefixset = set(p for word in wordset for p in prefixes(word))
	return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

def removed(letters, remove):
	"Return a str of letters, but with each letter in remove removed once."
	for L in remove:
		letters = letters.replace(L, '', 1)
	return letters

def find_words(letters, pre='', results=None):
	if results is None: results = set()
	if pre in WORDS: results.add(pre)
	if pre in PREFIXES:
		for L in letters:
			find_words(letters.replace(L, '', 1), pre+L, results)
	return results

def word_plays(hand, board_letters):
	"Find all word plays from hand that can be made to abut with a letter on board."
	# Find prefix + L + suffix; L from board_letters, rest from hand
	results = set()
	for pre in find_prefixes(hand, '', set()):
		for L in board_letters:
			add_suffixes(removed(hand, pre), pre+L, results)
	return results

def find_prefixes(hand, pre='', results=None):
	"Find all prefixes (of words) that can be made from letters in hand."
	if results is None: results = set()
	if pre in PREFIXES:
		results.add(pre)
		for L in hand:
			find_prefixes(hand.replace(L, '', 1), pre+L, results)
	return results

def add_suffixes(hand, pre, results):
	"""Return the set of words that can be formed by extending pre with letters in hand."""
	if pre in WORDS: results.add(pre)
	if pre in PREFIXES:
		for L in hand:
			add_suffixes(hand.replace(L, '', 1), pre+L, results)
	return results

assert (word_plays('ADEQUAT', set('IRE')) ==
		set(['DIE', 'ATE', 'READ', 'AIT', 'DE', 'IDEA', 'RET', 'QUID', 'DATE', 'RATE',
			 'ETA', 'QUIET', 'ERA', 'TIE', 'DEAR', 'AID', 'TRADE', 'TRUE', 'DEE',
			 'RED', 'RAD', 'TAR', 'TAE', 'TEAR', 'TEA', 'TED', 'TEE', 'QUITE', 'RE',
			 'RAT', 'QUADRATE', 'EAR', 'EAU', 'EAT', 'QAID', 'URD', 'DUI', 'DIT', 'AE',
			 'AI', 'ED', 'TI', 'IT', 'DUE', 'AQUAE', 'AR', 'ET', 'ID', 'ER', 'QUIT',
			 'ART', 'AREA', 'EQUID', 'RUE', 'TUI', 'ARE', 'QI', 'ADEQUATE', 'RUT']))

def longest_words(hand, board_letters):
	"Return all word plays, longest first."
	words = word_plays(hand, board_letters)
	return sorted(words, reverse=True, key=len)

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
	"The sum of the individual letter point scores for this word."
	return sum(POINTS[L] for L in word)

def topn(hand, board_letters, n=10):
	"Return a list of the top n words that hand can play, sorted by word score."
	words = word_plays(hand, board_letters)
	return sorted(words, reverse=True, key=word_score)[:n]

def timedcall(fn, *args):
	"Call function with args; return the time in seconds and result."
	t0 = time.clock()
	result = fn(*args)
	t1 = time.clock()
	return t1-t0, result

hands = {  ## Regression test
	'ABECEDR': set(['BE', 'CARE', 'BAR', 'BA', 'ACE', 'READ', 'CAR', 'DE', 'BED', 'BEE',
		 'ERE', 'BAD', 'ERA', 'REC', 'DEAR', 'CAB', 'DEB', 'DEE', 'RED', 'CAD',
		 'CEE', 'DAB', 'REE', 'RE', 'RACE', 'EAR', 'AB', 'AE', 'AD', 'ED', 'RAD',
		 'BEAR', 'AR', 'REB', 'ER', 'ARB', 'ARC', 'ARE', 'BRA']),
	'AEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'TIE', 'SIN', 'TAR', 'TAS',
		 'RAN', 'SIT', 'SAE', 'RIN', 'TAE', 'RAT', 'RAS', 'TAN', 'RIA', 'RISE',
		 'ANESTRI', 'RATINES', 'NEAR', 'REI', 'NIT', 'NASTIER', 'SEAT', 'RATE',
		 'RETAINS', 'STAINER', 'TRAIN', 'STIR', 'EN', 'STAIR', 'ENS', 'RAIN', 'ET',
		 'STAIN', 'ES', 'ER', 'ANE', 'ANI', 'INS', 'ANT', 'SENT', 'TEA', 'ATE',
		 'RAISE', 'RES', 'RET', 'ETA', 'NET', 'ARTS', 'SET', 'SER', 'TEN', 'RE',
		 'NA', 'NE', 'SEA', 'SEN', 'EAST', 'SEI', 'SRI', 'RETSINA', 'EARN', 'SI',
		 'SAT', 'ITS', 'ERS', 'AIT', 'AIS', 'AIR', 'AIN', 'ERA', 'ERN', 'STEARIN',
		 'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE', 'AI', 'IS', 'IT',
		 'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'IRE', 'ARS', 'ART', 'ARE']),
	'DRAMITC': set(['DIM', 'AIT', 'MID', 'AIR', 'AIM', 'CAM', 'ACT', 'DIT', 'AID', 'MIR',
		 'TIC', 'AMI', 'RAD', 'TAR', 'DAM', 'RAM', 'TAD', 'RAT', 'RIM', 'TI',
		 'TAM', 'RID', 'CAD', 'RIA', 'AD', 'AI', 'AM', 'IT', 'AR', 'AT', 'ART',
		 'CAT', 'ID', 'MAR', 'MA', 'MAT', 'MI', 'CAR', 'MAC', 'ARC', 'MAD', 'TA',
		 'ARM']),
	'ADEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'DEAR', 'TIE', 'SIN', 'RAD',
		 'TAR', 'TAS', 'RAN', 'SIT', 'SAE', 'SAD', 'TAD', 'RE', 'RAT', 'RAS', 'RID',
		 'RIA', 'ENDS', 'RISE', 'IDEA', 'ANESTRI', 'IRE', 'RATINES', 'SEND',
		 'NEAR', 'REI', 'DETRAIN', 'DINE', 'ASIDE', 'SEAT', 'RATE', 'STAND',
		 'DEN', 'TRIED', 'RETAINS', 'RIDE', 'STAINER', 'TRAIN', 'STIR', 'EN',
		 'END', 'STAIR', 'ED', 'ENS', 'RAIN', 'ET', 'STAIN', 'ES', 'ER', 'AND',
		 'ANE', 'SAID', 'ANI', 'INS', 'ANT', 'IDEAS', 'NIT', 'TEA', 'ATE', 'RAISE',
		 'READ', 'RES', 'IDS', 'RET', 'ETA', 'INSTEAD', 'NET', 'RED', 'RIN',
		 'ARTS', 'SET', 'SER', 'TEN', 'TAE', 'NA', 'TED', 'NE', 'TRADE', 'SEA',
		 'AIT', 'SEN', 'EAST', 'SEI', 'RAISED', 'SENT', 'ADS', 'SRI', 'NASTIER',
		 'RETSINA', 'TAN', 'EARN', 'SI', 'SAT', 'ITS', 'DIN', 'ERS', 'DIE', 'DE',
		 'AIS', 'AIR', 'DATE', 'AIN', 'ERA', 'SIDE', 'DIT', 'AID', 'ERN',
		 'STEARIN', 'DIS', 'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE',
		 'AD', 'AI', 'IS', 'IT', 'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'ID', 'ARS',
		 'ART', 'ANTIRED', 'ARE', 'TRAINED', 'RANDIEST', 'STRAINED', 'DETRAINS']),
	'ETAOIN': set(['ATE', 'NAE', 'AIT', 'EON', 'TIN', 'OAT', 'TON', 'TIE', 'NET', 'TOE',
		 'ANT', 'TEN', 'TAE', 'TEA', 'AIN', 'NE', 'ONE', 'TO', 'TI', 'TAN',
		 'TAO', 'EAT', 'TA', 'EN', 'AE', 'ANE', 'AI', 'INTO', 'IT', 'AN', 'AT',
		 'IN', 'ET', 'ON', 'OE', 'NO', 'ANI', 'NOTE', 'ETA', 'ION', 'NA', 'NOT',
		 'NIT']),
	'SHRDLU': set(['URD', 'SH', 'UH', 'US']),
	'SHROUDT': set(['DO', 'SHORT', 'TOR', 'HO', 'DOR', 'DOS', 'SOUTH', 'HOURS', 'SOD',
		 'HOUR', 'SORT', 'ODS', 'ROD', 'OUD', 'HUT', 'TO', 'SOU', 'SOT', 'OUR',
		 'ROT', 'OHS', 'URD', 'HOD', 'SHOT', 'DUO', 'THUS', 'THO', 'UTS', 'HOT',
		 'TOD', 'DUST', 'DOT', 'OH', 'UT', 'ORT', 'OD', 'ORS', 'US', 'OR',
		 'SHOUT', 'SH', 'SO', 'UH', 'RHO', 'OUT', 'OS', 'UDO', 'RUT']),
	'TOXENSI': set(['TO', 'STONE', 'ONES', 'SIT', 'SIX', 'EON', 'TIS', 'TIN', 'XI', 'TON',
		 'ONE', 'TIE', 'NET', 'NEXT', 'SIN', 'TOE', 'SOX', 'SET', 'TEN', 'NO',
		 'NE', 'SEX', 'ION', 'NOSE', 'TI', 'ONS', 'OSE', 'INTO', 'SEI', 'SOT',
		 'EN', 'NIT', 'NIX', 'IS', 'IT', 'ENS', 'EX', 'IN', 'ET', 'ES', 'ON',
		 'OES', 'OS', 'OE', 'INS', 'NOTE', 'EXIST', 'SI', 'XIS', 'SO', 'SON',
		 'OX', 'NOT', 'SEN', 'ITS', 'SENT', 'NOS'])}

def test_words():
	assert removed('LETTERS', 'L') == 'ETTERS'
	assert removed('LETTERS', 'T') == 'LETERS'
	assert removed('LETTERS', 'SET') == 'LTER'
	assert removed('LETTERS', 'SETTER') == 'L'
	t, results = timedcall(map, find_words, hands)
	for ((hand, expected), got) in zip(hands.items(), results):
		assert got == expected, "For %r: got %s, expected %s (diff %s)" % (
			hand, got, expected, expected ^ got)
	return t

if __name__ == '__main__':
	print test_words()
	print topn("RAHN", "RAHN")
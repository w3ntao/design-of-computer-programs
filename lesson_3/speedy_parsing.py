# ---------------
# User Instructions
#
# Modify the parse function so that it doesn't repeat computations.
# You have learned about a tool in this unit that prevents
# repetitive computations. Try using that!
#
# For this question, the grader will be looking for a specific
# solution. Hint: it should only involve adding one line of code
# (and that line should only contain 5 characters).

from functools import update_wrapper
import re

def parse(start_symbol, text, grammar):
	"""Example call: parse('Exp', '3*x + b', G).
	Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
	string. Failure iff remainder is None. This is a deterministic PEG parser,
	so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
	longest parse first; don't do 'E => T | T op E'
	Also, no left recursion allowed: don't do 'E => E op T'"""

	tokenizer = grammar[' '] + '(%s)'

	def parse_sequence(sequence, text):
		result = []
		for atom in sequence:
			tree, text = parse_atom(atom, text)
			if text is None: return Fail
			result.append(tree)
		return result, text

	@memo
	def parse_atom(atom, text):
		if atom in grammar:  # Non-Terminal: tuple of alternatives
			for alternative in grammar[atom]:
				tree, rem = parse_sequence(alternative, text)
				if rem is not None: return [atom]+tree, rem
			return Fail
		else:  # Terminal: match characters against start of text
			m = re.match(tokenizer % atom, text)
			return Fail if (not m) else (m.group(1), text[m.end():])

	# Body of parse:
	return parse_atom(start_symbol, text)

Fail = (None, None)

# The following decorators may help you solve this question. HINT HINT!

def decorator(d):
	"Make function d a decorator: d wraps a function fn."
	def _d(fn):
		return update_wrapper(d(fn), fn)
	update_wrapper(_d, d)
	return _d

@decorator
def memo(f):
	"""Decorator that caches the return value for each call to f(args).
	Then when called again with same args, we can just look it up."""
	cache = {}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			cache[args] = result = f(*args)
			return result
		except TypeError:
			# some element of args can't be a dict key
			return f(args)
	return _f

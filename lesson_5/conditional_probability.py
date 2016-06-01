import itertools
from fractions import Fraction

sex = "BG"

def product(*variables):
	"""The cartesian product (as a str) of the possibilities for each variable."""
	return map("".join, itertools.product(*variables))

two_kids = product(sex, sex)

one_boy = [s for s in two_kids if "B" in s]

def two_boys(s): return s.count("B") is 2

def condP(predicate, event):
	"""Conditional probability: P(predicate(s) | s in event).
	The proportion of states in event for which predicate is true."""
	pred = [s for s in event if predicate(s)]
	return Fraction(len(pred), len(event))

print condP(two_boys, one_boy)
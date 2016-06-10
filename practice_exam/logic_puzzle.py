"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
	one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
	arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools

def logic_puzzle():
	"Return a list of the names of the people, in the order they arrive."
	## your code here; you are free to define additional functions if needed
	days = Monday, Tuesday, Wednesday, Thursday, Friday = [0,1,2,3,4]
	possible_days = list(itertools.permutations(days))

	name  = ["Hamming", "Knuth", "Minsky", "Simon", "Wilkes"]

	order = next((Hamming, Knuth, Minsky, Simon, Wilkes)
			for (Hamming, Knuth, Minsky, Simon, Wilkes) in possible_days
			if Knuth - Simon is 1

			for (programmer, writer, manager, designer, _) in possible_days
			if not Wilkes is programmer
			if not Minsky is writer
			if not designer is Thursday
			if Knuth - manager is 1

			for (laptop, droid, tablet, iphone, _) in possible_days
			if Wednesday is laptop
			if set([programmer, droid]) == set([Wilkes, Hamming])
			if manager not in [tablet, Knuth]
			if not tablet is Friday
			if not designer is droid
			if not laptop is Wilkes and set([laptop, Wilkes]) == set([Monday, writer])
			if Tuesday in [iphone, tablet]
	)

	name_order = [(name[i], order[i]) for i in range(len(name))]
	return map(lambda x: x[0], sorted(name_order, key=lambda x: x[1]))

if __name__ == '__main__':
	print logic_puzzle()
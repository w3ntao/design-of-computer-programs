from maximizing_differential import max_wins, max_diffs

goal = 40

states = [(0, me, you, pending)
			for me in range(goal+1)
			for you in range(goal+1)
			for pending in range(goal+1)
			if me + pending <= goal]

total_action = len(states)

from collections import defaultdict

record = defaultdict(int)
for s in states: record[max_wins(s), max_diffs(s)] += 1


def print_action(action):
	print action,
	print "{:>6}".format(record[action]),
	print "{:5.2f}%".format(float(record[action])/total_action*100.0)

if __name__ == '__main__':
	print "max_win  max_diff"
	print ""

	print "same:"
	for action in record:
		if action[0] == action[1]:
			print_action(action)

	print "different:"
	for action in record:
		if action[0] != action[1]:
			print_action(action)
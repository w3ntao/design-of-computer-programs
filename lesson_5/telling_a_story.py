from collections import defaultdict
from maximizing_differential import max_wins, max_diffs

goal = 40

states = [(0, me, you, pending)
			for me in range(goal+1)
			for you in range(goal+1)
			for pending in range(goal+1)
			if me + pending <= goal]

def story():
	record = defaultdict(lambda: [0, 0])
	for s in states:
		w, d = max_wins(s), max_diffs(s)
		if w != d:
			_, _, _, pending = s
			i = 0 if (w == "roll") else 1
			record[pending][i] += 1

	print "pending   win_roll   diff_roll"
	for (delta, (wrolls, drolls)) in sorted(record.items()):
		print "{:>4}:        {:>3}       {:>3}".format(delta, wrolls, drolls)

if __name__ == '__main__':
	story()
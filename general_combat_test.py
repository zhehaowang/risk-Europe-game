import random

def toss():
	atk_dices = 3
	def_dices = 2

	tosses_atk = []
	for i in xrange(0, atk_dices):
		tosses_atk.append(random.randint(1, 6))
	tosses_atk.sort(reverse = True)

	tosses_def = []
	for i in xrange(0, def_dices):
		tosses_def.append(random.randint(1, 6))
	tosses_def.sort(reverse = True)
	
	scores_atk = 0
	scores_def = 0
	
	for i in xrange(0, 2):
		if tosses_atk[i] > tosses_def[i]:
			scores_atk += 1
		else:
			scores_def += 1

	return scores_atk, scores_def

if __name__ == "__main__":
	random.seed()
	total_cnt = 100000
	atk_favored = 0
	def_favored = 0
	draw = 0
	for i in range(0, total_cnt):
		scores_atk, scores_def = toss()
		if scores_def == scores_atk:
			draw += 1
		elif scores_atk > scores_def:
			atk_favored += 1
		else:
			def_favored += 1

	print "Chances of Attacker-favored result: " + str(float(atk_favored) / total_cnt)
	print "Chances of Defender-favored result: " + str(float(def_favored) / total_cnt)
	print "Chances of Draw: " + str(float(draw) / total_cnt)
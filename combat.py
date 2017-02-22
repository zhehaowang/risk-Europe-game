import os
import math
import random

# Number of total tosses for Monte Carlo to estimate the probability
NUM_TOSSES = 10000

class CombatStats(object):
    def __init__(self, footmen, archer, knight, siege, is_atk, has_castle = False):
        self.footmen = footmen
        self.archer = archer
        self.knight = knight
        self.siege = siege

        self.is_atk = is_atk
        self.has_castle = (not is_atk) and has_castle

class Combat(object):

    # always kill the least valuable stuff since you get to pick!
    # returns True if this action is successful
    @staticmethod
    def reduce_amount(stats):
        if stats.footmen > 0:
            stats.footmen -= 1
            return True
        if stats.archer > 0:
            stats.archer -= 1
            return True
        if stats.knight > 0:
            stats.knight -= 1
            return True
        if stats.siege > 0:
            stats.siege -= 1
            return True
        return False

    # returns True if this action is successful
    @staticmethod
    def reduce_amount_n(stats, n):
        for i in xrange(n):
            if not Combat.reduce_amount(stats):
                return False
        return True

    @staticmethod
    def total_remaining(stats):
        return stats.footmen + stats.archer + stats.knight + stats.siege

    # One pass in one Monte-Carlo toss
    @staticmethod
    def combat(atk_stats, def_stats):
        # round 1: siege: 2 dices, 3+ wins
        scores_atk = 0
        for i in xrange(atk_stats.siege):
            toss_1 = random.randint(1, 6)
            toss_2 = random.randint(1, 6)
            if toss_1 > 2:
                scores_atk += 1
            if toss_2 > 2:
                scores_atk += 1

        scores_def = 0
        for i in xrange(def_stats.siege):
            toss_1 = random.randint(1, 6)
            toss_2 = random.randint(1, 6)
            if toss_1 > 2:
                scores_def += 1
            if toss_2 > 2:
                scores_def += 1

        Combat.reduce_amount_n(atk_stats, scores_def)
        Combat.reduce_amount_n(def_stats, scores_atk)
        
        # round 2: ranged: 1 dice, 5+ wins
        scores_atk = 0
        for i in xrange(atk_stats.archer):
            toss_1 = random.randint(1, 6)
            if toss_1 > 4:
                scores_atk += 1

        scores_def = 0
        for i in xrange(def_stats.archer):
            toss_1 = random.randint(1, 6)
            if toss_1 > 4:
                scores_def += 1

        Combat.reduce_amount_n(atk_stats, scores_def)
        Combat.reduce_amount_n(def_stats, scores_atk)

        # round 3: cav: 1 dice, 3+ wins
        scores_atk = 0
        for i in xrange(atk_stats.knight):
            toss_1 = random.randint(1, 6)
            if toss_1 > 2:
                scores_atk += 1

        scores_def = 0
        for i in xrange(def_stats.knight):
            toss_1 = random.randint(1, 6)
            if toss_1 > 2:
                scores_def += 1

        Combat.reduce_amount_n(atk_stats, scores_def)
        Combat.reduce_amount_n(def_stats, scores_atk)

        # round 4: general
        atk_dices = min(3, Combat.total_remaining(atk_stats))
        def_dices = min(2, Combat.total_remaining(def_stats))

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
        # What happens if (atk, def) has (3, 1), (2, 1) or (1, 2) units? Does the 2nd dice count? 
        # (Rule doens't say explicitly, currently handled as doesn't count)
        comparisons = min(len(tosses_def), len(tosses_atk))
        for i in xrange(0, comparisons):
            if tosses_atk[i] > tosses_def[i]:
                scores_atk += 1
            else:
                scores_def += 1

        Combat.reduce_amount_n(atk_stats, scores_def)
        Combat.reduce_amount_n(def_stats, scores_atk)

        # return 0 for draw
        if Combat.total_remaining(atk_stats) == 0 and Combat.total_remaining(def_stats) == 0:
            return 0
        elif Combat.total_remaining(def_stats) == 0:
            # return 1 for atk_win
            return 1
        elif Combat.total_remaining(atk_stats) == 0:
            # return -1 for def_win
            return -1
        else:
            # unable to finish combat in this round, do another round and return its result
            return Combat.combat(atk_stats, def_stats)

def test_combat():
    draw_cnt = 0
    atk_win_cnt = 0
    def_win_cnt = 0
    random.seed()

    for i in xrange(0, NUM_TOSSES):
        atk_stats = CombatStats(9, 0, 0, 0, True, False)
        def_stats = CombatStats(10, 0, 0, 0, False, False)
        result = Combat.combat(atk_stats, def_stats)
        
        if result == 0:
            draw_cnt += 1
        elif result > 0:
            atk_win_cnt += 1
        else:
            def_win_cnt += 1

    print "Chances of Attacker winning: " + str(float(atk_win_cnt) / NUM_TOSSES)
    print "Chances of Defender winning: " + str(float(def_win_cnt) / NUM_TOSSES)
    print "Chances of Draw: " + str(float(draw_cnt) / NUM_TOSSES)

if __name__ == "__main__":
    test_combat()
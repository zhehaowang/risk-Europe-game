from flask import Flask, request
from combat import Combat, CombatStats
import random

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

NUM_TOSSES = 10000

def test_combat(atk_d, atk_a, atk_c, atk_s, def_d, def_a, def_c, def_s):
    if sum([atk_d, atk_a, atk_c, atk_s]) == 0 and sum([def_d, def_a, def_c, def_s]) == 0:
        return "0 inputs!"
    elif sum([atk_d, atk_a, atk_c, atk_s]) == 0:
        return "Defender wins!"
    elif sum([def_d, def_a, def_c, def_s]) == 0:
        return "Attacker wins!"

    draw_cnt = 0
    atk_win_cnt = 0
    def_win_cnt = 0
    random.seed()

    for i in xrange(0, NUM_TOSSES):
        atk_stats = CombatStats(atk_d, atk_a, atk_c, atk_s, True, False)
        def_stats = CombatStats(def_d, def_a, def_c, def_s, False, False)
        result = Combat.combat(atk_stats, def_stats)
        
        if result == 0:
            draw_cnt += 1
        elif result > 0:
            atk_win_cnt += 1
        else:
            def_win_cnt += 1

    result_string = ""
    result_string += "<p>Chances of Attacker winning: " + str(float(atk_win_cnt) / NUM_TOSSES) + "</p>"
    result_string += "<p>Chances of Defender winning: " + str(float(def_win_cnt) / NUM_TOSSES) + "</p>"
    result_string += "<p>Chances of Draw: " + str(float(draw_cnt) / NUM_TOSSES) + "</p>"
    return result_string

@app.route('/combat', methods=['GET', 'POST'])
def combat():
    if request.method == 'GET':
        try:
            atk_d = request.args.get('atk_d', '0')
        except KeyError as e:
            atk_d = 0
        try:
            atk_a = request.args.get('atk_a', '0')
        except KeyError as e:
            atk_a = 0        
        try:
            atk_c = request.args.get('atk_c', '0')
        except KeyError as e:
            atk_c = 0
        try:
            atk_s = request.args.get('atk_s', '0')
        except KeyError as e:
            atk_s = 0

        try:
            def_d = request.args.get('def_d', '0')
        except KeyError as e:
            def_d = 0
        try:
            def_a = request.args.get('def_a', '0')
        except KeyError as e:
            def_a = 0
        try:
            def_c = request.args.get('def_c', '0')
        except KeyError as e:
            def_c = 0
        try:
            def_s = request.args.get('def_s', '0')
        except KeyError as e:
            def_s = 0

        result = test_combat(int(atk_d), int(atk_a), int(atk_c), int(atk_s), int(def_d), int(def_a), int(def_c), int(def_s))
        return result
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
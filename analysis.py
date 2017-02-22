import Gnuplot, Gnuplot.funcutils
import random 

from combat import Combat, CombatStats

NUM_TOSSES = 10000

def run_test(atk, dfd):
    draw_cnt = 0
    atk_win_cnt = 0
    def_win_cnt = 0

    for i in xrange(0, NUM_TOSSES):
        atk_stats = CombatStats(atk["footmen"], atk["archer"], atk["knight"], atk["siege"], True, False)
        def_stats = CombatStats(dfd["footmen"], dfd["archer"], dfd["knight"], dfd["siege"], False, False)
        result = Combat.combat(atk_stats, def_stats)
        
        if result == 0:
            draw_cnt += 1
        elif result > 0:
            atk_win_cnt += 1
        else:
            def_win_cnt += 1

    return float(atk_win_cnt) / NUM_TOSSES, float(def_win_cnt) / NUM_TOSSES, float(draw_cnt) / NUM_TOSSES

def init_g(g, title, xlabel, outfile):
    g('set key right bottom')
    g('set style data linespoints')
    g('set term pdf')

    g.xlabel(xlabel) # 'Number of dudes'
    g.ylabel('Chance of success')
    g.title(title) # 'Dude spam vs dude spam'
    g("set output \"" + outfile + "\"") # figures/dude-spam.pdf

def plot():
    random.seed()

    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []

    # footmen vs footmen, equal number
    print "calculating footmen fight..."
    for i in range(1, 26):
        atk = {"footmen": i, "archer": 0, "knight": 0, "siege": 0}
        dfd = {"footmen": i, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)

    g = Gnuplot.Gnuplot(debug = 1)
    init_g(g, 'Dude spam vs dude spam', 'Number of dudes', 'figures/dude-spam.pdf')
    
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "footmen analysis finished"
    g.reset()

    # archer vs archer, equal number
    print "calculating archer fight..."
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    for i in range(1, 13):
        atk = {"footmen": 0, "archer": i, "knight": 0, "siege": 0}
        dfd = {"footmen": 0, "archer": i, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)

    init_g(g, 'Archer spam vs archer spam', 'Number of archers', 'figures/archer-spam.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "archer analysis finished"
    g.reset()

    # when should you get an archer? (attacking)
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []

    print "calculating archer (attack)"
    for i in range(0, 11):
        atk = {"footmen": 20 - 2 * i, "archer": i, "knight": 0, "siege": 0}
        dfd = {"footmen": 20, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '20 dudes and archers (atk) vs 20 dudes (def)', 'Number of archers on attacking side (x), (20 - 2x) is the number of dudes', 'figures/archer-dude-atk.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "archers (attack) analysis finished"
    g.reset()

    # when should you get an archer? (defending)
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating archer (defend)"
    for i in range(0, 11):
        dfd = {"footmen": 20 - 2 * i, "archer": i, "knight": 0, "siege": 0}
        atk = {"footmen": 20, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '20 dudes and archers (def) vs 20 dudes (atk)', 'Number of archers on defending side (x), (20 - 2x) is the number of dudes', 'figures/archer-dude-def.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "archers (defend) analysis finished"
    g.reset()

    # when should you get a knight (attack)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating knight (attack)"
    for i in range(0, 7):
        atk = {"footmen": 18 - 3 * i, "archer": 0, "knight": i, "siege": 0}
        dfd = {"footmen": 18, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)

    init_g(g, '18 dudes and knights (atk) vs 18 dudes (def)', 'Number of knights on attacking side (x), (18 - 3x) is the number of dudes', 'figures/knight-dude-atk.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "knight (attack) analysis finished"
    g.reset()

    # when should you get a knight (attack)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating knight (defend)"
    for i in range(0, 7):
        dfd = {"footmen": 18 - 3 * i, "archer": 0, "knight": i, "siege": 0}
        atk = {"footmen": 18, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '18 dudes and knights (def) vs 18 dudes (atk)', 'Number of knights on defending side (x), (18 - 3x) is the number of dudes', 'figures/knight-dude-def.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "knight (defend) analysis finished"
    g.reset()

    # when should you get a siege (attack)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating siege (attack)"
    for i in range(0, 3):
        atk = {"footmen": 20 - 10 * i, "archer": 0, "knight": 0, "siege": i}
        dfd = {"footmen": 20, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '20 dudes and catapults (atk) vs 20 dudes (def)', 'Number of catapults on attacking side (x), (20 - 10x) is the number of dudes', 'figures/siege-dude-atk.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "siege (attack) analysis finished"
    g.reset()

    # when should you get a siege (defend)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating siege (defend)"
    for i in range(0, 3):
        dfd = {"footmen": 20 - 10 * i, "archer": 0, "knight": 0, "siege": i}
        atk = {"footmen": 20, "archer": 0, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '20 dudes and catapults (def) vs 20 dudes (atk)', 'Number of catapults on defending side (x), (20 - 10x) is the number of dudes', 'figures/siege-dude-def.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "siege (defend) analysis finished"
    g.reset()

    # archers or knights (attack)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating archers / knights (attack)"
    for i in range(0, 5):
        atk = {"footmen": 0, "archer": 12 - 3 * i, "knight": 2 * i, "siege": i}
        dfd = {"footmen": 0, "archer": 12, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(2 * i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)

    init_g(g, '12 archers and knights (atk) vs 12 archers (def)', 'Number of knights on attacking side (2x), (12 - 3x) is the number of archers', 'figures/knight-archer-atk.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "archers / knights (attack) analysis finished"
    g.reset()

    # archers or knights (defend)?
    points = []
    atk_values = []
    def_values = []
    draw_values = []
    reference_line = []
    
    print "calculating archers / knights (defend)"
    for i in range(0, 5):
        dfd = {"footmen": 0, "archer": 12 - 3 * i, "knight": 2 * i, "siege": i}
        atk = {"footmen": 0, "archer": 12, "knight": 0, "siege": 0}
        atk_win, def_win, draw = run_test(atk, dfd)
        
        points.append(2 * i)
        atk_values.append(atk_win)
        def_values.append(def_win)
        draw_values.append(draw)
        reference_line.append(0.5)
    
    init_g(g, '12 archers and knights (def) vs 12 archers (atk)', 'Number of knights on defending side (2x), (12 - 3x) is the number of archers', 'figures/knight-archer-def.pdf')
    g.plot(Gnuplot.Data(points, atk_values, title="Attacker wins"), 
        Gnuplot.Data(points, def_values, title="Defender wins"), 
        Gnuplot.Data(points, draw_values, title="Draws"), 
        Gnuplot.Data(points, reference_line, title="Reference", with_="lines lt 3 linecolor rgb 'grey'"))
    print "archers / knights (defend) analysis finished"
    g.reset()

    
if __name__ == "__main__":
    plot()
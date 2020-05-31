# https://old.reddit.com/r/GlobalOffensive/comments/8mjqgc/i_made_a_python_script_that_generates_stats_using/
# https://pastebin.com/LLpym05c

import datetime

import matplotlib.pyplot as plt


def min_to_sec(line):  # converts minutes in string format 'XXX:XX' to seconds
    seconds = 0
    seconds += (int(line[-1]))
    seconds += (int(line[-2])) * 10
    seconds += (int(line[-4])) * 60
    if line[-5].isdigit():
        seconds += (int(line[-5])) * 600
    if line[-6].isdigit():
        seconds += (int(line[-6])) * 6000

    return seconds


def create_plot(entries, plottitle, xaxlabel, filelabel, res, kdinput):  # dont feel like commenting this tbh
    if kdinput:
        plt.hist(entries, bins=(int(max(entries) * res)))
    else:
        plt.hist(entries, bins=range(min(entries), max(entries) + 1, 1))

    plt.title(plottitle)
    if kdinput:
        plt.xticks(range(0, int(max(entries))))
    plt.xlabel(xaxlabel)
    plt.ylabel('Occurrences')
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.grid(color='b', linestyle=':', alpha=0.3, linewidth=1)
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * 0.4)

    plt.savefig(filelabel, dpi=300)
    plt.clf()


filename = input("Input File Name (e.g. stats.txt or stats.htm): ")
steamid = input("Your Steam ID: ")

# splits file into list of individual HTML element strings
file = open(filename, encoding="utf8").read().split('<')

stats = []  # contains lists of individual games
# Format: ['MAP', [D, M, Y], Q LENGTH, GAME LENGTH, GAME SCORE,[PING, K, A, D, MVP, HSP, Score]]

current_game = [0] * 6  # temporarily holds current game data
begin = False  # for parsing through beginning of document

for i, line in enumerate(file):
    line = line.strip()

    if 'td>\n' in line:  # game info lines begin with <td>\n for some reason
        if 'Competitive' in line[10:]:
            begin = True  # begin storing document data here
            current_game[0] = line[22:]

        if line[10:12] == '20':
            year = line[10:14]
            month = line[15:17]
            day = line[18:20]
            current_game[1] = list(map(int, [day, month, year]))

        if 'Wait Time:' in line[10:]:
            current_game[2] = min_to_sec(line)

        if 'Match Duration:' in line[10:]:
            current_game[3] = min_to_sec(line)

    # stores personal game data as list
    if begin and line[0:7] == 'a class' and steamid in line:
        ping = file[i + 4][3:]
        k = file[i + 6][3:]
        a = file[i + 8][3:]
        d = file[i + 10][3:]

        # had to do this because single MVPs don't contain the number '1' by the star
        mvp = -1  # if MVP entry is empty
        if file[i + 12][-2] == '>':
            mvp = 1
        else:
            for j, char in enumerate(file[i + 12]):
                if char.isdigit():
                    mvp = file[i + 12][j:]
                    break

        # had to do this because some HSP entries are empty
        hsp = -1  # if HSP entry is empty
        if file[i + 14][-2].isdigit():
            hsp = file[i + 14][3:len(file[i + 14]) - 1]

        score = file[i + 16][3:]

        # appends performance data (list of ints) to stats list as fifth 6th element
        current_game[5] = list(map(int, [ping, k, a, d, mvp, hsp, score]))

    # gets the match score and sorts it in a list of 2 ints (your score first)
    if 'csgo_scoreboard_score' in line:
        match_score = line[45:].split(' : ')
        if not isinstance(current_game[5], list):
            match_score.reverse()

        current_game[4] = list(map(int, match_score))

    if isinstance(current_game[4], list) and isinstance(current_game[5],
                                                        list):  # individual game lists contain 6 entries
        stats.append(current_game)
        current_game = [0] * 6  # clears list before recording next game's info
        current_game[3] = 1800  # 30 minute placeholder

# declaration of stat variables
total_kills = 0
total_deaths = 0
total_assists = 0
total_MVPs = 0
total_rounds_w = 0
total_rounds_l = 0
max_match_length = 0
min_match_length = 5400
win_streak = 0
loss_streak = 0
tie_streak = 0
max_win_streak = 0
max_loss_streak = 0
max_tie_streak = 0
total_score = 0

hsp = []  # list containing all hsps
mvp = []  # list containing all mvps
map_plays = {}  # dict containing maps (keys) and plays (vals)

# initializing output file
output = open('output.txt', 'w')

stats.reverse()
# looping through every 'stats' entry (game lists)
for i, stat in enumerate(stats):
    # writing a list of every match to the output file
    output.write('\n' + str(i) + ': ' + repr(stat))

    # summing K, D, A, MVP
    total_kills += stat[5][1]
    total_deaths += stat[5][3]
    total_assists += stat[5][2]
    total_MVPs += stat[5][4]
    total_rounds_w += stat[4][0]
    total_rounds_l += stat[4][1]
    total_score += stat[5][6]

    # creating list of Headshot Percentages (-1 excluded because -1 means no entry was listed)
    if stat[5][5] >= 0:
        hsp.append(stat[5][5])

    # creating list of MVPs (-1 excluded because -1 means no entry was listed)
    if stat[5][4] >= 0:
        mvp.append(stat[5][4])

    # finding the longest match
    if stat[3] > max_match_length:
        max_match_length = stat[3]
        max_match_index = i

    if stat[3] < min_match_length:
        min_match_length = stat[3]
        min_match_index = i

    # builds dictionary containing maps and number of times map has been played
    if stat[0] not in map_plays:
        map_plays[stat[0]] = 1
    else:
        map_plays[stat[0]] += 1

    ###########################################################################
    # convoluted way of calculating win/tie/loss streaks:
    if stat[4][0] > stat[4][1]:
        win_streak += 1
        loss_streak, tie_streak = 0, 0
    elif stat[4][0] == stat[4][1]:
        tie_streak += 1
        win_streak, loss_streak = 0, 0
    else:
        loss_streak += 1
        win_streak, tie_streak = 0, 0

    if win_streak > max_win_streak:
        max_win_streak = win_streak
        max_win_index = i
    if tie_streak > max_tie_streak:
        max_tie_streak = tie_streak
        max_tie_index = i
    if loss_streak > max_loss_streak:
        max_loss_streak = loss_streak
        max_loss_index = i
################################################################################

# writing output to output.txt file
output.write('\nFormat: [\'MAP\', [D, M, Y], QUEUE LENGTH, GAME LENGTH, GAME SCORE, [PING, K, A, D, MVP, HSP, Score]]')
output.write('\n\nSTATS----------------------------------------------------------------\n')

output.write('{:<20} {:>7}'.format('\nTotal Kills:', total_kills))
output.write('{:<20} {:>7}'.format('\nTotal Deaths:', total_deaths))
output.write('{:<20} {:>7}'.format('\nTotal Assists:', total_assists))
output.write('{:<20} {:>7}'.format('\nTotal MVPs:', total_MVPs))
kdr = round(total_kills / total_deaths, 3)
output.write('{:<20} {:>7}'.format('\nK/D:', kdr))

output.write('\n')
output.write('{:<20} {:>7}'.format('\nTotal Rounds Won:', total_rounds_w))
output.write('{:<20} {:>7}'.format('\nTotal Rounds Lost:', total_rounds_l))

output.write('\n\nAverages (per game):')
output.write('\n\t{:<15} {:>8}'.format('K:', round(total_kills / len(stats), 2)))
output.write('\n\t{:<15} {:>8}'.format('D:', round(total_deaths / len(stats), 2)))
output.write('\n\t{:<15} {:>8}'.format('A:', round(total_assists / len(stats), 2)))
output.write('\n\t{:<15} {:>8}'.format('MVP:', round(total_MVPs / len(stats), 2)))
output.write('\n\t{:<15} {:>8}'.format('Score:', round(total_score / len(stats), 2)))

avg_rounds_won = round(total_rounds_w / len(stats), 1)
avg_rounds_lost = round(total_rounds_l / len(stats), 1)

output.write('\n\t{:<10} {} : {}'.format('Match (W:L):', avg_rounds_won, avg_rounds_lost))

total_rounds = total_rounds_l + total_rounds_w
output.write('\n\nAverages (per round):')
output.write('\n\t{:<15} {:>8}'.format('K:', round(total_kills / total_rounds, 2)))
output.write('\n\t{:<15} {:>8}'.format('D:', round(total_deaths / total_rounds, 2)))
output.write('\n\t{:<15} {:>8}'.format('A:', round(total_assists / total_rounds, 2)))
output.write('\n\t{:<15} {:>8}'.format('MVP:', round(total_MVPs / total_rounds, 2)))

output.write('\n\nHSP:')
output.write('\n\t{:<10} {:>8}%'.format('Max:', round(max(hsp), 2)))
output.write('\n\t{:<10} {:>8}%'.format('Min:', round(min(hsp), 2)))
output.write('\n\t{:<10} {:>8}%'.format('Avg:', round(sum(hsp) / len(hsp), 1)))

output.write(
    '\n\nLongest Match:\t\t{}\t\t(game #{})'.format(datetime.timedelta(seconds=max_match_length), max_match_index))
output.write(
    '\nShortest Match:\t\t{}\t\t(game #{})'.format(datetime.timedelta(seconds=min_match_length), min_match_index))

output.write(
    '\nMax Win Streak: \t{}\t\t(from game #{} to #{})'.format(max_win_streak, max_win_index - max_win_streak + 1,
                                                              max_win_index))
output.write(
    '\nMax Tie Streak: \t{}\t\t(from game #{} to #{})'.format(max_tie_streak, max_tie_index - max_tie_streak + 1,
                                                              max_tie_index))
output.write(
    '\nMax Loss Streak: \t{}\t\t(from game #{} to #{})'.format(max_loss_streak, max_loss_index - max_loss_streak + 1,
                                                               max_loss_index))

output.write('\n\nMap Plays:')
for entry in sorted(map_plays, key=map_plays.get, reverse=True):
    output.write('\n\t{:<12} {:>12}'.format(entry, map_plays[entry]))

print('\'output.txt\' can be found in the same directory as this script')
output.close()

#####################################################################
# graphing and graphing calculations done below

# lists containing raw vals for each stat
kd = []
kills = []
deaths = []
assists = []
mvps = []
hsps = []
rw = []  # rounds won
rl = []
games_played = {}

for stat in stats:
    # collects vals from each game
    kills.append(stat[5][1])
    deaths.append(stat[5][3])
    assists.append(stat[5][2])
    if stat[5][4] == -1:
        mvps.append(0)
    else:
        mvps.append(stat[5][4])
    if stat[5][5] == -1:
        hsps.append(0)
    else:
        hsps.append(stat[5][5])

    if stat[5][3] > 0:
        kd.append(stat[5][1] / stat[5][3])
    else:
        kd.append(1)

    if stat[4][0] < 15:
        rw.append(stat[4][0])
    if stat[4][1] < 15:
        rl.append(stat[4][1])

    if stat[1][2] * 12 + stat[1][1] not in games_played:
        games_played[stat[1][2] * 12 + stat[1][1]] = 1
    else:
        games_played[stat[1][2] * 12 + stat[1][1]] += 1

plt.rc('font', size=8)
create_plot(kd, 'K/D Distribution', 'K/D (resolution: 0.05)', 'KD_Distribution.png', 20, True)
kd_trimmed = [x for x in kd if x <= 3]
create_plot(kd_trimmed, 'K/D Distribution (truncated at x = 3)', 'K/D (resolution: 0.01)',
            'KD_Distribution (TRIMMED).png', 100, True)
create_plot(kills, 'Kill Distribution', 'Kills', 'Kill_Distribution.png', 0, False)
create_plot(deaths, 'Death Distribution', 'Deaths', 'Death_Distribution.png', 0, False)
create_plot(assists, 'Assist Distribution', 'Assists', 'Assist_Distribution.png', 0, False)
create_plot(mvps, 'MVP Distribution', 'MVPs', 'MVP_Distribution.png', 0, False)
create_plot(hsps, 'HSP Distribution', 'HSP', 'HSP_Distribution.png', 0, False)
create_plot(rw, 'Rounds Won Distribution (exc. 15, 16)', 'Rounds', 'RW_Distribution.png', 0, False)
create_plot(rl, 'Rounds Lost Distribution (exc. 15, 16)', 'Rounds', 'RL_Distribution.png', 0, False)

# graphing games played
games_played_x = []
games_played_y = []
for entry in sorted(games_played):
    games_played_x.append(entry - 1)
    games_played_y.append(games_played[entry])

games_played_x_string = []
for entry in games_played_x:
    year = int(entry / 12)
    month = (entry % 12) + 1
    monthyear = str(month) + '-' + str(year)
    games_played_x_string.append(monthyear)

plt.bar(games_played_x, games_played_y)
plt.title('Games Played Per Month')
plt.xlabel('Month')
plt.ylabel('Occurrences')
plt.xticks(games_played_x[::4], games_played_x_string[::4], rotation='45')
plt.savefig('Games_Played.png', dpi=300)
plt.clf()

print('output images can be found in the same directory as this script')

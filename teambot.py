from operator import truediv
from os import dup
import random
import keyboard

scoresraw = open("C:/Users/s2000925/Documents/Championship/teamgenerator/scores.txt", "r")

def print_team(team):
    teamtotalscore = get_team_score(team)

    return f'{team[0][0]}, {team[1][0]}, {team[2][0]}, {teamtotalscore}'

def get_team_score(team):
    return team[0][1] + team[1][1] + team[2][1]

def swap(parts, p1, p2):
    parts[p1], parts[p2] = parts[p2], parts[p1]

def generate_teams(parts):
    team1 = [parts[0], parts[1], parts[2]]
    team2 = [parts[3], parts[4], parts[5]]
    team3 = [parts[6], parts[7], parts[8]]
    team4 = [parts[9], parts[10], parts[11]]

    return [team1,team2,team3,team4]

def get_score_diff(teams):
    scores = [get_team_score(teams[0]),get_team_score(teams[1]),get_team_score(teams[2]),get_team_score(teams[3])]
    return max(scores) - min(scores)

def check_for_duplicates(allparts, bestparts):
    allparts.append(bestparts)

    for aps in allparts:
        sorted_aps = sorted(aps)
        for y in allparts:
            print(aps[y])

    return True

    




s = scoresraw.readlines()

participants = []

for x in s:
    x = x.replace('\n','')
    x = x.split(',')
    name = x[0]
    season1score = int(x[1])
    season2score = int(x[2])

    averagescore = (season1score + season2score) / 2
    
    if (season1score == 0 or season2score == 0):
        averagescore = max(season1score, season2score)
    
    participants.append([name,averagescore])

teams = generate_teams(participants)
scorediff = get_score_diff(teams)

alternatives = 0
alternativeparts = []

while True:

    tempparts = participants.copy()

    thisbestscore = scorediff
    thisbestparts = tempparts

    for p in range(len(tempparts)):
        for s in range(len(tempparts)):
            swap(tempparts,p,s)

            tempteams = generate_teams(tempparts)
            thisscorediff = get_score_diff(tempteams)

            if (thisscorediff < thisbestscore):
                thisbestscore = thisscorediff
                thisbestparts = tempparts
                alternatives = 0
                alternativeparts.clear()
            elif (thisscorediff == thisbestscore and check_for_duplicates(alternativeparts, thisbestparts)):

                alternatives += 1
                alternativeparts.append(tempparts)

            tempparts = participants.copy()

    sd = get_score_diff(generate_teams(thisbestparts))

    if (sd < scorediff):
        scorediff = sd
        participants = thisbestparts.copy()
    else:
        break


    print(f'Generating team... Diff: ({scorediff})')

bestteams = generate_teams(participants)

for f in bestteams:
    f.sort()


print(f'\n{print_team(bestteams[0])}, \n{print_team(bestteams[1])}, \n{print_team(bestteams[2])}, \n{print_team(bestteams[3])}\nScore diff ({scorediff})')
print(f'')

al = 0
if (alternatives > 0):
    for a in alternativeparts:
        altbestteams = generate_teams(a)
        altscorediff = get_score_diff(altbestteams)
        
        for t in altbestteams:
            t.sort()

        duplicates = 0
        for t2 in range(len(altbestteams)):
            for p in range(len(altbestteams[t2])):
                if (altbestteams[t2][p] == bestteams[t2][p]):
                    duplicates += 1

        if (duplicates == 12):
            continue
        
        al += 1

        print(f'ALTERNATIVE {al}')
        print(f'{print_team(altbestteams[0])}, \n{print_team(altbestteams[1])}, \n{print_team(altbestteams[2])}, \n{print_team(altbestteams[3])}\n')

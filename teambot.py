from operator import truediv
from os import dup
import random
import keyboard
import os

scoresraw = open(f"{os.getcwd()}/scores.txt", "r")

alternativeteam_scoretreshhold = 15

def print_team(team):
    teamtotalscore = get_team_score(team)

    return f'{team[0][0]}, {team[1][0]}, {team[2][0]}, (Score: {teamtotalscore})'

def print_not_participating(parts):
    np = f''

    for p in range(len(parts)):
        if p > 11:
            np += f'{parts[p][0]}, '
    
    return np

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

def check_for_duplicates(team, allparts, bestparts):
    allparts.append(bestparts)

    for a in allparts:
        diffinpart = 0
        for p in range(len(a)):
            if a[p][0] != team[p][0]:
                diffinpart += 1
        if diffinpart == 0:
            return True


    return False

    




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

participants_sorted = sorted(participants, key=lambda p : p[1],reverse=True)
participants = participants_sorted

teams = generate_teams(participants)
scorediff = get_score_diff(teams)

alternatives = 0
alternativeparts = []

while True:

    tempparts = participants.copy()

    thisbestscore = scorediff
    thisbestparts = tempparts

    improvements = 0

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
                improvements += 1
            elif (thisscorediff <= thisbestscore + alternativeteam_scoretreshhold and not check_for_duplicates(tempparts, alternativeparts, thisbestparts)):
                alternatives += 1
                alternativeparts.append(tempparts)

            tempparts = participants.copy()

    sd = get_score_diff(generate_teams(thisbestparts))

    if (sd < scorediff):
        scorediff = sd
        participants = thisbestparts.copy()
    else:
        break


    print(f'Teams generated. {improvements} optimization(s) found. Diff: ({scorediff})')

bestteams = generate_teams(participants)

for f in bestteams:
    f.sort()


print(f'\nBEST TEAMS:\nTeam 1: {print_team(bestteams[0])} \nTeam 2: {print_team(bestteams[1])} \nTeam 3: {print_team(bestteams[2])} \nTeam 4: {print_team(bestteams[3])}\nScore diff ({scorediff})')
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
        print(f'Team 1: {print_team(altbestteams[0])} \nTeam 2: {print_team(altbestteams[1])} \nTeam 3: {print_team(altbestteams[2])} \nTeam 4: {print_team(altbestteams[3])}\nScore diff ({altscorediff})\n')

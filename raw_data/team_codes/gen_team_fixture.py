import json

def gen_team_fix(team_list):   
    """ Function to build fixture for team info.

    This function was desiged to work on the file found at 
    http://www.retrosheet.org/team_codes.html.

    Ideally I would like to use the file from 
    http://www.retrosheet.org/TeamIds.htm however, it is unavailable.
    
    That file is set up with 1 team per line.  
    Columns are TEAMID,LEAGUE,START,END,CITY,NICKNAME,FRANCHID,SEQ

    """ 
    output = []

    # slice is to remove the first line which contains column info 
    for line in team_list[1:]:
        line = line.split(',')
        team = {}
        team['pk'] = line[0]
        team['model'] = 'atbatvis.Team'
        team['fields'] = {}
        team['fields']['name'] = line[5]
        team['fields']['city'] = line[4]
        team['fields']['start'] = line[2]
        team['fields']['end'] = check_year(line[3])

        output.append(team)

    with open('team_fix/teams.json', 'w') as f:
        json.dump(output, f, indent=2)

def check_year(year):
    if year == "0":
        return "Current"
    else:
        return year
  

def main():
    with open('team_raw/team_codes.txt', 'r') as f:
        lines = [line.strip() for line in f]

    gen_team_fix(lines)

main()

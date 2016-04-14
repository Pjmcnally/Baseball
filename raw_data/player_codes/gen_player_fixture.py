import json

def gen_player_fix(player_list):   
    """ Function to build fixture for player info.

    This function was desiged to work on http://www.retrosheet.org/retroID.htm.
    
    That file is set up with 1 player per line.  
    Columns are LAST,FIRST,ID,DEBUT

    """ 
    output = []

    # slice is to remove the first line which contains column info 
    for line in player_list[1:]:
        line = line.split(',')
        player = {}
        player['pk'] = line[2]
        player['model'] = 'atbatvis.Player'
        player['fields'] = {}
        player['fields']['f_name'] = line[1]
        player['fields']['l_name'] = line[0]
        player['fields']['debut'] = build_date(line[3])

        output.append(player)

    with open('players.json', 'w') as f:
        json.dump(output, f, indent=2)


def build_date(date):
    if date:
        return "{y}-{m}-{d}".format(y=date[6:], m=date[0:2], d=date[3:5])
    else:
        return None
  

def main():
    with open('playercodes.txt', 'r') as f:
        lines = [line.strip() for line in f]

    gen_player_fix(lines)

main()
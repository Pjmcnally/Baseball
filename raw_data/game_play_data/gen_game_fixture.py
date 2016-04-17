import json
import re
import os

def get_files(path):
    files = {}

    for folder in os.walk(path):
        for file in folder[2]:
            if ".EVN" in file or ".EVA" in file:
                files[file] = "{}/{}".format(folder[0], file)

    return files


def gen_fixtures(game_list):   
    """ Function to build fixture for game info.

    This function was desiged to work on game data file from Retrosheets.
    
    """ 
    game_output = []
    play_output = []
    game = {}
    play = {}
    old_player = ""

    # slice is to remove the first line which contains column info 
    for i, line in enumerate(game_list):

        if line[0] == "id":
            if game:
                game['fields']['players'] = list(players)
                game_output.append(game)
            game = {}
            players = set()
            game_id = line[1]
            game['pk'] = game_id
            game['model'] = 'atbatvis.Game'
            game['fields'] = {}
        elif line[0] == "info":
            if line[1] == "hometeam":
                game['fields']['home_team'] = line[2]
            elif line[1] == "visteam":
                game['fields']['away_team'] = line[2]
            elif line[1] == "site":
                game['fields']['location'] = line[2]
            elif line[1] == "date":
                game['fields']['date'] = build_date(line[2])
            elif line[1] == "starttime":
                game['fields']['start_time'] = build_time(line[2])

        # This section creates and saves play objects.
        elif line[0] == "play":
            player = line[3]
            players.add(player)
            pitches = line[5]
            play_full = line[6]
            count = line[4].replace("??", "")

            
            # These are all plays that do not end a plate apperance
            if (
                "WP" in play_full or
                "NP" in play_full or
                "OA" in play_full or
                "SB" in play_full or
                "CS" in play_full or 
                "PO" in play_full or 
                "PB" in play_full
            ):
                continue
            else:
                play = {}
                play['model'] = 'atbatvis.Play'
                play['fields'] = {}
                play['fields']['inning'] = line[1]
                play['fields']['bottom'] = bool(int(line[2]))
                play['fields']['player'] = player
                play['fields']['game'] = game_id
                play['fields']['count'] = count
                play['fields']['pitches'] = pitches
                play['fields']['play_full'] = play_full
                play['fields']['play_short'] = interp(
                    pitches, 
                    play_full
                )

                play_output.append(play)  
            

    game['fields']['players'] = list(players)
    game_output.append(game)
    return game_output, play_output

def interp(pitches, play):
    pitches, play = pitches.upper(), play.upper()

    if play[0].isdigit():
        special = ["GDP", "GTP", "LDP", "LTP"]
        for item in special:
            if item in play:
                return item
        else:
            try:
                return re.findall(r'\/([A-Z]+)[\.\-0-9A-Z;\(\)\+#]*$', play)[0]
            except:
                return "OUT"

    else:
        play_short = re.findall(r'^([A-Z]+)', play)[0]
        
        if play_short == "S":
            return "1B"
        elif play_short == "D":
            return "2B"
        elif play_short == "T":
            return "3B"
        elif "HP" in play:
            return "HBP"
        elif "H" in play_short:
            return "HR"
        elif "E" in play_short:
            return "E"
        elif play_short == "FC":
            return "FC"
        elif play_short == "DGR":
            return "GRD"
        elif play_short == "C":
            return "E"
        elif "FLE" in play:
            return "E"
        elif "K" in play:
            return "K"
        elif "I" in play:
            return "IW"
        elif "W" in play:
            return "W"
        
        else:
            print(play_short, play)
            return "THIS SHOULD NEVER BE SEEN (not out)"



def build_date(date):
    if date:
        date = date.replace("/", "-")
        return date
    else:
        return None

def build_time(time):
    h_reg = r'^([\d]+):'
    m_reg = r':([\d]+)'
    
    if time:
        hour = int(re.findall(h_reg, time)[0])
        if "pm" in time.lower():
            hour += 12
            if hour == 24:
                hour = 0
        minute = re.findall(m_reg, time)[0]

        return "{h}:{m}:{s}".format(h=hour, m=minute, s="00")
    else:
        return ''
  

def main():
    in_path = "./game_raw"
    g_out_path = "./game_fix"
    p_out_path = "./play_fix"
    
    # For testing
    # in_path = "./test"
    # g_out_path = "./test"
    # p_out_path = "./test"

    files = get_files(in_path)

    for name, path in sorted(files.items()):
        file_name = name[:-4]
        print(file_name)
        with open(path, 'r') as f:
            lines = [line.strip().split(",") for line in f]

        games, plays = gen_fixtures(lines)

        g_name = "{}/{}_games.json".format(g_out_path, file_name)
        with open(g_name, 'w') as f:
            json.dump(games, f, indent=2)

        p_name = "{}/{}_plays.json".format(p_out_path, file_name)
        with open(p_name, 'w') as f:
            json.dump(plays, f, indent=2)

main()
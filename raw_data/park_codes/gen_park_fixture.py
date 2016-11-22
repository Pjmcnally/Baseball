import json


def gen_park_fix(park_list):
    """ Function to build fixture for park info.

    This function was desiged to work on parkcode.txt file from Retrosheets.

    That file is set up with 1 park per line.
    Columns are PARKID,NAME,AKA,CITY,STATE,START,END,LEAGUE,NOTES

    """
    output = []

    # slice is to remove the first line which contains column info
    for line in park_list[1:]:
        line = line.split(',')
        park = {}
        park['pk'] = line[0]
        park['model'] = 'atbatvis.Location'
        park['fields'] = {}
        park['fields']['name'] = line[1]
        park['fields']['aka'] = line[2]
        park['fields']['city'] = line[3]
        park['fields']['state'] = line[4]
        park['fields']['start'] = build_date(line[5])
        park['fields']['end'] = build_date(line[6])

        output.append(park)

    with open('park_fix/parks.json', 'w') as f:
        json.dump(output, f, indent=2)


def build_date(date):
    if date:
        return "{y}-{m}-{d}".format(y=date[6:], m=date[0:2], d=date[3:5])
    else:
        return None


def main():
    with open('park_raw/parkcode.txt', 'r') as f:
        lines = [line.strip() for line in f]

    gen_park_fix(lines)

main()

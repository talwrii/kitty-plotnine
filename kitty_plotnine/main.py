import argparse
import csv
import datetime
import json
import os
import re
import sys
import webbrowser


import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotnine

os.environ["MPLBACKEND_KITTY_SIZING"] = "manual"
matplotlib.use('module://matplotlib-backend-kitty')


NUMBERS = """\
one
two
three
four
five
six
seven
eight
nine
ten
eleven
twelve
thirteen
fourteen
fifteen
sixteen
seventeen
eighteen
nineteen
twenty
twenty_one
twenty_two
twenty_three
twenty_four
twenty_five
twenty_six
twenty_seven
twenty_eight
twenty_nine
thirty
thirty_one
thirty_two
thirty_three
thirty_four
thirty_five
thirty_six
thirty_seven
thirty_eight
thirty_nine
forty
forty_one
forty_two
forty_three
forty_four
forty_five
forty_six
forty_seven
forty_eight
forty_nine
fifty
fifty_one
fifty_two
fifty_three
fifty_four
fifty_five
fifty_six
fifty_seven
fifty_eight
fifty_nine
sixty
sixty_one
sixty_two
sixty_three
sixty_four
sixty_five
sixty_six
sixty_seven
sixty_eight
sixty_nine
seventy
seventy_one
seventy_two
seventy_three
seventy_four
seventy_five
seventy_six
seventy_seven
seventy_eight
seventy_nine
eighty
eighty_one
eighty_two
eighty_three
eighty_four
eighty_five
eighty_six
eighty_seven
eighty_eight
eighty_nine
ninety
ninety_one
ninety_two
ninety_three
ninety_four
ninety_five
ninety_six
ninety_seven
ninety_eight
ninety_nine
""".splitlines()


PARSER = argparse.ArgumentParser(description='Plot data directly in the shell')
PARSER.add_argument("--doc", action='store_true', help="Show the document for this graphical element")
PARSER.add_argument("--list", action='store_true', help="List all graphical elements")
PARSER.add_argument("--web", action='store_true', help="List all graphical elements")
PARSER.add_argument("expression", help="plotnine graphics of grammar expression", nargs="*")



INTRO = """\
k9 reads data in CSV or JSON and plots a graph using plotnine in kitty.

Example expression:

aes(x="one", y="two") + geom_point()

Use `k9 --list` to see all graphical elements.
Use `k9 --doc` to show the documentation for elements.

"""

def main():

    args = PARSER.parse_args()

    if args.list:
        elements = dir(plotnine)

        for search in sys.argv[1:]:
            if search in ["-l", "--list"]:
                continue
            print(search)
            elements = [x for x in elements if re.search(search, x)]

        print('\n'.join(elements))
        return

    if args.doc:
        if args.web:
            if not args.expression:
                webbrowser.open('https://plotnine.org/reference/')
                return
            else:
                element, = args.expression
                if element not in vars(plotnine):
                    raise Exception(f'{element} is not a graphical element')

                url = f'https://plotnine.org/reference/{element}.html'
                webbrowser.open(url)
                return

        print(eval(element, vars(plotnine)).__doc__)
        return

    lines = sys.stdin.read().splitlines()
    if lines[0].startswith("{"):
        data = [json.loads(l) for l in lines]
        data = pd.DataFrame(data)
    elif "," in lines[0]:
        data = list(csv.reader(lines))
        data = [[maybe_number(c) for c in r] for r in data]
        ncol = len(data[0])
        data = pd.DataFrame(data, columns=NUMBERS[:ncol])
    else:
        data = [line.split() for line in lines]
        data = [[maybe_number(c) for c in r] for r in data]
        ncol = len(data[0])
        data = pd.DataFrame(data, columns=NUMBERS[:ncol])


    def is_datetime(x):
        try:
            return datetime.datetime.fromisoformat(x)
        except (ValueError, TypeError):
            return False

    def is_date(x):
        try:
            return datetime.date.fromisoformat(x)
        except (ValueError, TypeError):
            return False

    for c in data.columns:
        if data[c].map(is_date).all() or data[c].map(is_datetime).all():
            data[c] = pd.to_datetime(data[c])

    plot = eval("ggplot(data) + " + " ".join(args.expression), dict(data=data, **vars(plotnine)))
    plot.show()


def maybe_number(x):
    try:
        return float(x)
    except ValueError:
        return x

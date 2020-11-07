import requests
import sys
import time
import winsound
from bs4 import BeautifulSoup as bs

url = "https://www.foxnews.com/elections/2020/general-results"

def connect ():
    try:
        r = requests.get(url)
        soup = bs(r.text, features="lxml")
        return soup
    except:
        print(f"Failed to get {state_abbr}")
        return None

def get_states (state_abbr):
    soup = connect()
    all_state_polls = soup.findAll("div", class_=["content", "race-table"])[4]
    polls = all_state_polls.find("table", {"data-state": state_abbr})
    return polls.text.replace("\n", " ")

def get_totals ():
    soup = connect()
    upper_page = soup.findAll("div", class_=["content", "race-table"])[0]
    counts = upper_page.text.replace("\n", " ").split()
    return (counts[0], counts[5])

start = round(time.time())
repeat = 60
current_status = {
    "GA": get_states("GA"),
    "PA": get_states("PA"),
    "NC": get_states("NC"),
    "NV": get_states("NV"),
}
states = ["GA", "PA", "NV", "NC"]

biden_total, trump_total = get_totals()
# print(f"Start, GA: {current_status.get('GA')}")


while True:

    if round(time.time()) == start + repeat:
        sys.stdout.write(str(round(time.time())) + "\n")
        sys.stdout.flush()
        start = round(time.time())

        for state in states :
            new_site = get_states(state)
            if current_status[state] == new_site :

                pass
            else:
                sys.stdout.write(f"{state} has changed!\n")
                pre_change = list(filter(None, current_status[state].split(" ")))
                sys.stdout.write("from: {}\n".format(" ".join(pre_change[13:25])))
                post_change = list(filter(None, new_site.split(" ")))
                sys.stdout.write("to: {}\n".format(" ".join(post_change[13:25])))
                sys.stdout.flush()
                winsound.PlaySound("Alert_sounds/sound1.wav", winsound.SND_ASYNC)
                current_status[state] = new_site

        biden_fin, trump_fin = get_totals()

        if biden_fin != biden_total:
            print(f"Biden state secured, new total: {biden_fin}")
            biden_total = biden_fin
            winsound.PlaySound("Alert_sounds/sound2.wav", winsound.SND_ASYNC)
        elif trump_fin != trump_total:
            print(f"Trump state secured, new total: {trump_fin}")
            trump_total = trump_fin
            winsound.PlaySound("Alert_sounds/sound3.wav", winsound.SND_ASYNC)

    else:
        time.sleep(1)
        pass

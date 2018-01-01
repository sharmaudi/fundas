import json
import os

def get_config_for(key):
    r = os.path.dirname(os.path.abspath(__file__))
    print(f'{r}')
    print('Getting config for {}'.format(key))
    config = []
    with open(f"{r}/../appconfig/{key}.config.json", "r") as infile:
        config = json.load(infile)
    return config


def get_watchlist():
    with open("appconfig/watchlist.json", "r") as infile:
        return_set = json.load(infile)
    return return_set


def set_watchlist(watchlist):
    with open("appconfig/watchlist.json", "w") as infile:
        json.dump(watchlist, infile)


def add_to_watchlist(company):
    orig_list = get_watchlist()
    orig_list.append(company)
    set_watchlist(orig_list)


def remove_from_watchlist(company):
    orig_list = get_watchlist()
    if company in orig_list:
        orig_list.remove(company)
    if orig_list:
        set_watchlist(orig_list)
    else:
        set_watchlist([])

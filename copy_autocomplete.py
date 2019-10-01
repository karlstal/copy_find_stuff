#!/usr/bin/python

import requests
import sys
import time


def get_autocomplete(client_url):
    req_url = '/'.join([
        client_url.strip('/'),
        '_autocomplete/list?&size=999'
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when fetching autocomplete. Aborting.")
    return result.json()['hits']


def add_autocomplete(autocompletes, client_url):
    if autocompletes is None or len(autocompletes) == 0:
        return
    req_url = '/'.join([
        client_url.strip('/'),
        '_autocomplete/'
    ])
    for autocomplete in autocompletes:
        time.sleep(0.025)
        aut = {
            'priority': autocomplete['priority'],
            'query': autocomplete['query'],
            'tags': autocomplete['tags']
        }
        response = requests.post(req_url, json=aut)
        if response.status_code not in [200, 201]:
            sys.exit("Something went wrong when adding autocompletes. Aborting.")

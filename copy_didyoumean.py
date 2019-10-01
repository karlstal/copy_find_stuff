#!/usr/bin/python

import requests
import sys
import time


def get_didyoumean(client_url):
    result = make_didyoumean_req(client_url, 0)
    hits = result['hits']
    from_ = 100
    while from_ < result['total']:
        time.sleep(0.2)
        hits += make_didyoumean_req(client_url, from_)['hits']
        from_ += 100
    return hits


def make_didyoumean_req(client_url, from_=0):
    req_url = '/'.join([
        client_url.strip('/'),
        '_didyoumean/list?size=100&from=' + str(from_)
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when fetching didyoumean. Aborting.")
    return result.json()


def add_didyoumean(didyoumeans, client_url):
    if didyoumeans is None or len(didyoumeans) == 0:
        return
    req_url = '/'.join([
        client_url.strip('/'),
        '_didyoumean/'
    ])
    for didyoumean in didyoumeans:
        time.sleep(0.025)
        didy = {
            'priority': didyoumean['priority'],
            'query': didyoumean['query'],
            'suggestion': didyoumean['suggestion'],
            'tags': didyoumean['tags']
        }
        response = requests.post(req_url, json=didy)
        if response.status_code not in [200, 201]:
            sys.exit("Something went wrong when adding didyoumean. Aborting.")

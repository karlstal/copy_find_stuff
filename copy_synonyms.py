#!/usr/bin/python

import requests
import sys
import time


def get_synonyms(client_url):
    result = make_synonym_req(client_url, 0)
    hits = result['hits']
    from_ = 100
    while from_ < result['total']:
        time.sleep(0.2)
        hits += make_synonym_req(client_url, from_)['hits']
        from_ += 100
    return hits


def make_synonym_req(client_url, from_=0):
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/synonym/?size=100&from=' + str(from_)
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when fetching synonyms. Aborting.")
    return result.json()


def add_synoyms(synonyms, client_url):
    if synonyms is None or len(synonyms) == 0:
        return
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/synonym/'
    ])
    for synonym in synonyms:
        time.sleep(0.025)
        del synonym['id']
        response = requests.post(req_url, json=synonym)
        if response.status_code not in [200, 201]:
            sys.exit("Something went wrong when adding synonyms. Aborting.")

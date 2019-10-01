#!/usr/bin/python

import requests
import sys


def get_unifiedweights(client_url):
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/unifiedweights/'
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when fetching unifiedweights. Aborting.")
    if result.json()['total'] == 0:
        return {}
    return result.json()['hits'][0]


def add_unifiedweights(unifiedweights, client_url):
    if unifiedweights is None or len(unifiedweights) == 0:
        return
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/unifiedweights/'
    ])

    # don't know why there is a list in the list in the 'tags' property..
    uw = {
        'name': unifiedweights['name'],
        'weights': unifiedweights['weights'],
        'tags': unifiedweights['tags'][0]
    }
    response = requests.post(req_url, json=uw)
    if response.status_code not in [200, 201]:
        sys.exit("Something went wrong when adding unifiedweights. Aborting.")

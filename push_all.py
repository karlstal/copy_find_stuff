#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import json
import requests

CONFIGURATION_FILE = 'config.json'


def main():
    print("\nStarting uploads.\n")
    config = read_config()
    client_url = config['client_url']

    with open("downloaded_{0}.json".format(config['time'])) as f:
        settings = json.load(f)

    actions = {
        'autocomplete': add_autocomplete, 'connectors': add_connectors,
        'didyoumean': add_didyoumean, 'synonyms': add_synonyms,
        'unifiedweights': add_unifiedweights
    }
    settings = {k: v for k, v in settings.items() if v is not None and len(v) != 0 and k in actions}
    for k, v in settings.items():
        print("Counting {0} entries for {1}. Uploading..".format(str(len(v)), k))
        actions[k](v, client_url)
    print("\nAll uploads finished!\n")


def read_config():
    with open(CONFIGURATION_FILE) as f:
        config = json.load(f)
    return config


def make_req(client_url, path, payload):
    req_url = client_url.strip('/') + '/' + path
    response = requests.post(req_url, json=payload)
    if response.status_code not in [200, 201]:
        sys.exit("Error: GET to {0} returned status code {1}.".format(
            path,
            str(response.status_code)
        ))


def add_autocomplete(autocompletes, client_url):
    for autocomplete in autocompletes:
        time.sleep(0.025)
        aut = {
            'priority': autocomplete['priority'],
            'query': autocomplete['query'],
            'tags': autocomplete['tags']
        }
        make_req(client_url, '_autocomplete/', aut)


def add_connectors(connectors, client_url):
    for connector in connectors:
        n_connectors = _n_connectors(client_url)
        make_req(client_url, '_admin/connector/', connector)
        while n_connectors == _n_connectors(client_url):
            print("Waiting for connector to be added..")
            time.sleep(3)
        print("Connector was added!")


def _n_connectors(client_url):
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/connector/'
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when counting connectors. Aborting.")
    return result.json()['total']


def add_didyoumean(didyoumeans, client_url):
    for didyoumean in didyoumeans:
        time.sleep(0.025)
        didy = {
            'priority': didyoumean['priority'],
            'query': didyoumean['query'],
            'suggestion': didyoumean['suggestion'],
            'tags': didyoumean['tags']
        }
        make_req(client_url, '_didyoumean/', didy)


def add_synonyms(synonyms, client_url):
    for synonym in synonyms:
        time.sleep(0.025)
        del synonym['id']
        make_req(client_url, '_admin/synonym/', synonym)


def add_unifiedweights(unifiedweights, client_url):
    # don't know why there is a list in the list in the 'tags' property..
    uw = {
        'name': unifiedweights['name'],
        'weights': unifiedweights['weights'],
        'tags': unifiedweights['tags'][0]
    }
    make_req(client_url, '_admin/unifiedweights/', uw)

if __name__ == '__main__':
    main()

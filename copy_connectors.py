#!/usr/bin/python

import requests
import sys
import time


def get_connectors(client_url):
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/connector/'
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when fetching connectors. Aborting.")
    connectors = []
    for hit in result.json()['hits']:
        configuration = hit['configuration']
        del configuration['version']
        connectors.append({
            'type': 'crawler',
            'configuration': configuration,
            'name': hit['name'],
            'channel': 'system!web'
        })
    return connectors


def add_connectors(connectors, client_url):
    if connectors is None or len(connectors) == 0:
        return
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/connector/'
    ])
    n_connectors = _n_connectors(client_url)
    for connector in connectors:
        response = requests.post(req_url, json=connector)
        if response.status_code not in [200, 201]:
            sys.exit("Something went wrong when adding connectors. Aborting.")
        while n_connectors <= _n_connectors:
            print("Waiting for connector to be added..")
            time.sleep(3)
        print("Connector was be added!")
        n_connectors = _n_connectors(client_url)


def _n_connectors(client_url):
    req_url = '/'.join([
        client_url.strip('/'),
        '_admin/connector/'
    ])
    result = requests.get(req_url)
    if result.status_code != 200:
        sys.exit("Something went wrong when counting connectors. Aborting.")
    return result.json()['total']

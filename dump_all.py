#!/usr/bin/python

import sys
import json
import time
import requests

CONFIGURATION_FILE = 'config.json'


def main():
    print("\nDownloading settings..")
    config = read_config()
    client_url = config['old_index_client_url']
    settings = {}
    settings['autocomplete'] = get_autocomplete(client_url)
    settings['connectors'] = get_connectors(client_url)
    settings['didyoumean'] = get_all_batches(client_url, '_didyoumean/list', 100, {})
    settings['synonyms'] = get_all_batches(client_url, '_admin/synonym/', 100, {})
    settings['unifiedweights'] = get_unifiedweights(client_url)

    print("All settings downloaded. Saving now..")
    now = str(time.time())
    with open('downloaded_{0}.json'.format(now), 'w') as f:
        json.dump(settings, f)

    config['time'] = now
    with open(CONFIGURATION_FILE, 'w') as f:
        json.dump(config, f)
    print("\nFinished successfully!")
    print("(Change service url in config and run dump_all.py.)\n")


def read_config():
    with open(CONFIGURATION_FILE) as f:
        config = json.load(f)
    return config


def make_req(client_url, path, args=None):
    req_url = client_url.strip('/') + '/' + path
    result = requests.get(req_url, params=args)
    if result.status_code == 429:
        print ("Got a 429. Sleeping 2s and retry")
        time.sleep(2)
        return make_req(client_url, path, args)
    elif result.status_code != 200:
        sys.exit("Error: Something went wrong when trying to GET '{0}'. Find returned status code {1}.".format(
            path,
            str(result.status_code)
        ))
    return result.json()


def get_all_batches(client_url, path, batch_size, args):
    args['size'] = batch_size
    result = make_req(client_url, path, args=args)
    hits = result['hits']
    args['from'] = batch_size
    while args['from'] < result['total']:
        time.sleep(0.2)
        r = make_req(client_url, path, args)
        hits += r['hits']
        args['from'] += batch_size
    return hits


def get_autocomplete(client_url):
    response = make_req(client_url, '_autocomplete/list', args={'size': 999})
    return response['hits']


def get_connectors(client_url):
    result = make_req(client_url, '_admin/connector')
    connectors = []
    for hit in result['hits']:
        configuration = hit['configuration']
        del configuration['version']
        connectors.append({
            'type': hit['type'],
            'configuration': configuration,
            'name': hit['name'],
            'channel': hit['channel']
        })
    return connectors


def get_unifiedweights(client_url):
    result = make_req(client_url, '_admin/unifiedweights/')
    if result['total'] == 0:
        return {}
    return result['hits'][0]


if __name__ == '__main__':
    main()

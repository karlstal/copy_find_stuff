#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from os.path import isfile
from copy_synonyms import add_synoyms
from copy_autocomplete import add_autocomplete
from copy_unifiedweights import add_unifiedweights
from copy_didyoumean import add_didyoumean


def main():
    config = read_config()
    now = config['time']
    client_url = config['client_url']

    add_synoyms(read_data(now + "_syonyms"), client_url)
    add_autocomplete(read_data(now + "_autocomplete"), client_url)
    add_unifiedweights(read_data(now + "_unifiedweights"), client_url)
    add_didyoumean(read_data(now + "_didyoumean"), client_url)


def read_config():
    with open('config.json') as f:
        config = json.load(f)
    return config


def read_data(file_name):
    if not isfile(file_name):
        print("{0} does not exist!".format(file_name))
        return {}
    with open(file_name) as f:
        return json.load(f)


if __name__ == '__main__':
    main()

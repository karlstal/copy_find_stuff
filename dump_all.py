#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
from copy_synonyms import get_synonyms
from copy_autocomplete import get_autocomplete
from copy_unifiedweights import get_unifiedweights
from copy_didyoumean import get_didyoumean


def main():
    config = read_config()
    client_url = config['client_url']
    now = str(time.time())
    print("Started: {0} (timestamp)".format(now))

    save_data(get_synonyms(client_url), now + "_syonyms")
    save_data(get_autocomplete(client_url), now + "_autocomplete")
    save_data(get_unifiedweights(client_url), now + "_unifiedweights")
    save_data(get_didyoumean(client_url), now + "_didyoumean")

    config['time'] = now
    with open('config.json', 'w') as f:
        json.dump(config, f)


def read_config():
    with open('config.json') as f:
        config = json.load(f)
    return config


def save_data(data_, file_name):
    if data_ is None or len(data_) == 0:
        print("{0}: Nothing to save!".format(file_name))
        return
    with open(file_name, 'w') as f:
        json.dump(data_, f)


if __name__ == '__main__':
    main()

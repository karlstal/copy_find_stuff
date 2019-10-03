
# Copy Find Stuff
A script for copying editorial autocomplete, connector configurations, editorial didyoumean, synonyms and unified weights from one index to another.

## Disclaimer
Be sure to verify that everything looks ok after each step since this script is not that well tested.


## External dependencies
Requests (`pip install requests`)


## Usage
Should work with python >= 2.7
1. Add a client_url on the form *https://<PROXY_URL>/<PRIVATE_KEY>/<INDEX_NAME>/* in **config.json**
  Run **dump_all.py** to download all data
2. Change the client_url to the new index
  Run **push_all.py**

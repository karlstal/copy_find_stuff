# Copy Find stuff

## Disclaimer
The connector part of this script have not been tested and added to push_all.py or dump_all.py. Please do, before using it!


## External dependencies
Requests (pip install requests)


## Usage
Should work with python >= 2.7
1. Add a client_url on the form https://<PROXY_URL>/<PRIVATE_KEY>/<INDEX_NAME>/ in config.json
   Run dump_all.py to download all data
2. Change the client_url to the new index
   Run push_all.py

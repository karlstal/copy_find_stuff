
# Copy Find Stuff
A script for copying editorial autocomplete, connector configurations, editorial didyoumean, synonyms and unified weights from one index to another.

## Disclaimer
Be sure to verify that everything looks ok after each step since this script is not that well tested.


## External dependencies
Requests (`pip install requests`)


## Usage
Should work with python >= 2.7.
The script uses a config file (**config.json**) that looks like this:
```javascript
{
	"old_index_client_url": "https:<PROXY_URL>/<PRIVATE_KEY_1>/<INDEX_NAME_1>/", // This is from where the settings will be copied.
	"new_index_client_url": "https:<PROXY_URL>/<PRIVATE_KEY_2>/<INDEX_NAME_2>/", // This is where the settings will be copied to.
	"time": "1561360096.23" // Don't touch this
}
```

1. Edit **config.json** as described above.
2. Run **dump_all.py** to download all data.
3. Do a (manual) sanity check on the generated file *downloaded_<TIMESTAMP>.json* and validate that the settings has been downloaded ok.
4. Run **push_all.py**

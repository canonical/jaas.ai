# flake8: noqa

import json
import os

# To update these JSON files run: ./run exec npm run update-test-json

test_dir = os.path.dirname(__file__)

search_data = None
with open(os.path.join(test_dir, "json/search.json"), "r") as json_file:
    data = json.loads(json_file.read())
    search_data = data["Results"]

charm_data = None
with open(os.path.join(test_dir, "json/charm.json"), "r") as json_file:
    charm_data = json.loads(json_file.read())

bundle_data = None
with open(os.path.join(test_dir, "json/bundle.json"), "r") as json_file:
    bundle_data = json.loads(json_file.read())

user_entities_data = None
with open(os.path.join(test_dir, "json/user-entities.json"), "r") as json_file:
    data = json.loads(json_file.read())
    user_entities_data = data["Results"]

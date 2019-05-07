from urllib.request import urlretrieve

# To update these JSON files run: ./run exec npm run update-test-json

search_url = 'https://api.jujucharms.com/v5/search?include=charm-metadata&include=bundle-metadata&include=owner&include=bundle-unit-count&include=promulgated&include=supported-series&text=apache2'
urlretrieve(search_url, 'tests/store/json/search.json')

charm_url = 'https://api.jujucharms.com/v5/apache2-26/meta/any?include=bundle-machine-count&include=bundle-metadata&include=bundle-unit-count&include=charm-actions&include=charm-config&include=charm-metadata&include=common-info&include=extra-info&include=owner&include=published&include=resources&include=supported-series&include=terms&include=revision-info&include=manifest&include=stats'
urlretrieve(charm_url, 'tests/store/json/charm.json')

bundle_url = 'https://api.jujucharms.com/v5/canonical-kubernetes-466/meta/any?include=bundle-machine-count&include=bundle-metadata&include=bundle-unit-count&include=charm-actions&include=charm-config&include=charm-metadata&include=common-info&include=extra-info&include=owner&include=published&include=resources&include=supported-series&include=terms&include=revision-info&include=manifest&include=stats'
urlretrieve(bundle_url, 'tests/store/json/bundle.json')

user_entities = 'https://api.jujucharms.com/v5/list?include=charm-metadata&include=bundle-metadata&include=owner&include=bundle-unit-count&include=bundle-machine-count&include=supported-series&include=published&owner=hatch'
urlretrieve(user_entities, 'tests/store/json/user-entities.json')

import unittest

from tests.store.testdata import charm_data, search_data
from unittest.mock import patch
from webapp.store import models


class TestStoreModels(unittest.TestCase):
    @patch('theblues.charmstore.CharmStore.search')
    def test_search_entities(self, mock_search):
        mock_search.return_value = search_data
        results = models.search_entities('apache2')
        self.assertEqual(len(results['community']), 8)
        self.assertEqual(len(results['recommended']), 2)

    @patch('theblues.charmstore.CharmStore.search')
    def test_search_entities_none(self, mock_search):
        mock_search.return_value = []
        results = models.search_entities('apache2')
        self.assertEqual(len(results['community']), 0)
        self.assertEqual(len(results['recommended']), 0)

    def test_parse_charm_data_tags(self):
        charm = models._parse_charm_data(charm_data)
        self.assertEqual(charm['tags'], ['app-servers'])

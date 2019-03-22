import unittest

from tests.store.testdata import search_data
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

from flask_testing import TestCase
from unittest.mock import patch
from webapp.app import create_app


class StoreViews(TestCase):
    render_templates = False

    def create_app(self):
        app = create_app(testing=True)
        return app

    @patch('webapp.store.models.search_entities')
    def test_search(self, mock_search_entities):
        mock_search_entities.return_value = {
            'recommended': [{}, {}],
            'community': [{}, {}]
        }
        response = self.client.get('/search?q=k8s')
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable('context')
        self.assertEqual(context['results_count'], 4)

    @patch('webapp.store.models.search_entities')
    def test_search_none(self, mock_search_entities):
        mock_search_entities.return_value = {
            'recommended': [],
            'community': []
        }
        response = self.client.get('/search?q=k8s')
        self.assertEqual(response.status_code, 200)

    @patch('webapp.store.models.search_entities')
    def test_search_redirect(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get('/q/k8s')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/search?q=k8s')

    @patch('webapp.store.models.search_entities')
    def test_search_redirect_multi_word(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get('/q/k8s/demo')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location, 'http://localhost/search?q=k8s+demo')

    @patch('webapp.store.models.search_entities')
    def test_search_redirect_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get('/q/k8s?sort=name&series=xenial')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            'http://localhost/search?q=k8s&sort=name&series=xenial')

    @patch('webapp.store.models.search_entities')
    def test_search_redirect_just_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get('/q?tags=proxy')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location, 'http://localhost/search?tags=proxy')

    @patch('webapp.store.models.get_user_entities')
    def test_user_details(self, mock_get_user_entities):
        mock_get_user_entities.return_value = {
            'bundles': [{}, {}],
            'charms': [{}, {}]
        }
        response = self.client.get('/u/user-name')
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable('context')
        self.assertEqual(context['username'], 'user-name')

    @patch('webapp.store.models.get_user_entities')
    def test_user_404(self, mock_get_user_entities):
        mock_get_user_entities.return_value = {
            'bundles': [],
            'charms': []
        }
        response = self.client.get('/u/user-name')
        self.assertEqual(response.status_code, 404)

    @patch('webapp.store.models.get_charm_or_bundle')
    def test_details_charm(self, mock_get_charm_or_bundle):
        entity = {
            'is_charm': True
        }
        mock_get_charm_or_bundle.return_value = entity
        response = self.client.get('/apache2')
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable('context')
        self.assertEqual(context['charm'], entity)

    @patch('webapp.store.models.get_charm_or_bundle')
    def test_details_bundle(self, mock_get_charm_or_bundle):
        entity = {
            'is_charm': False
        }
        mock_get_charm_or_bundle.return_value = entity
        response = self.client.get('/k8s-bundle')
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable('context')
        self.assertEqual(context['bundle'], entity)

    @patch('webapp.store.models.get_charm_or_bundle')
    def test_details_404(self, mock_get_charm_or_bundle):
        mock_get_charm_or_bundle.return_value = None
        response = self.client.get('/nothing')
        self.assertEqual(response.status_code, 404)

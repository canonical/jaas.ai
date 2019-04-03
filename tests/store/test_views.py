from flask_testing import TestCase
from unittest.mock import patch

from webapp.app import create_app
from tests.store.testdata import bundle_data, charm_data


class StoreViews(TestCase):
    render_templates = True

    def create_app(self):
        app = create_app(testing=True)
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app

    @patch("webapp.store.models.search_entities")
    def test_search(self, mock_search_entities):
        mock_search_entities.return_value = {
            "recommended": [{}, {}],
            "community": [{}, {}],
        }
        response = self.client.get("/search?q=k8s")
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable("context")
        self.assertEqual(context["results_count"], 4)

    @patch("webapp.store.models.search_entities")
    def test_search_none(self, mock_search_entities):
        mock_search_entities.return_value = {
            "recommended": [],
            "community": [],
        }
        response = self.client.get("/search?q=k8s")
        self.assertEqual(response.status_code, 200)

    @patch("webapp.store.models.search_entities")
    def test_search_redirect(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/search?q=k8s")

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_multi_word(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s/demo")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location, "http://localhost/search?q=k8s+demo"
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q/k8s?sort=name&series=xenial")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location,
            "http://localhost/search?q=k8s&sort=name&series=xenial",
        )

    @patch("webapp.store.models.search_entities")
    def test_search_redirect_just_query_params(self, mock_search_entities):
        mock_search_entities.return_value = []
        response = self.client.get("/q?tags=proxy")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.location, "http://localhost/search?tags=proxy"
        )

    @patch("webapp.store.models.get_user_entities")
    def test_user_details(self, mock_get_user_entities):
        mock_get_user_entities.return_value = {
            "bundles": [{}, {}],
            "charms": [{}, {}],
        }
        response = self.client.get("/u/user-name")
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable("context")
        self.assertEqual(context["username"], "user-name")

    @patch("webapp.store.models.get_user_entities")
    def test_user_404(self, mock_get_user_entities):
        mock_get_user_entities.return_value = {"bundles": [], "charms": []}
        response = self.client.get("/u/user-name")
        self.assertEqual(response.status_code, 404)

    def check_entity(self, mock_entity, entity_type, url):
        """Check that a provided URL renders an entity page.

        :param unittest.mock.MagicMock mock_entity: A mocked entity method.
        :param str entity_type: Whether this entity is a charm or bundle.
        :param str url: The URL to test.
        """
        return_value = charm_data if entity_type == "charm" else bundle_data
        mock_entity.return_value = return_value
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable("context")
        self.assertIsNotNone(context["entity"])

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/apache2")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_version(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/apache2/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_series(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/apache2/wily")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_series_version(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/apache2/wily/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/k8s-bundle")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_version(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/k8s-bundle/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_series(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/k8s-bundle/wily")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_series_version(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/k8s-bundle/wily/14")

    @patch("webapp.store.models.get_charm_or_bundle")
    def test_details_404(self, mock_get_charm_or_bundle):
        mock_get_charm_or_bundle.return_value = None
        response = self.client.get("/nothing")
        self.assertEqual(response.status_code, 404)

    @patch("webapp.store.models.get_charm_or_bundle")
    def test_user_entity_404(self, mock_get_charm_or_bundle):
        mock_get_charm_or_bundle.return_value = None
        response = self.client.get("/u/user-name/no-thing")
        self.assertEqual(response.status_code, 404)

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/u/user-name/apache2")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_version(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/u/user-name/apache2/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_series(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/u/user-name/apache2/wily")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_series_version(self, mock_entity):
        self.check_entity(mock_entity, "charm", "/u/user-name/apache2/wily/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/u/user-name/k8s-bundle")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_version(self, mock_entity):
        self.check_entity(mock_entity, "bundle", "/u/user-name/k8s-bundle/14")

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_series(self, mock_entity):
        self.check_entity(
            mock_entity, "bundle", "/u/user-name/k8s-bundle/wily"
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_series_version(self, mock_entity):
        self.check_entity(
            mock_entity, "bundle", "/u/user-name/k8s-bundle/wily/14"
        )

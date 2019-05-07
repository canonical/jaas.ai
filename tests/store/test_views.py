from flask import url_for
from flask_testing import TestCase
from unittest.mock import call, MagicMock, patch

from tests.store.testdata import bundle_data, charm_data, user_entities_data
from theblues.errors import ServerError
from webapp.app import create_app


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
        response = self.client.get(url_for("jaasstore.search", q="k8s"))
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable("context")
        self.assertEqual(context["results_count"], 4)

    @patch("webapp.store.models.search_entities")
    def test_search_none(self, mock_search_entities):
        mock_search_entities.return_value = {
            "recommended": [],
            "community": [],
        }
        response = self.client.get(url_for("jaasstore.search", q="k8s"))
        self.assertEqual(response.status_code, 200)

    @patch("webapp.store.models.search_entities")
    def test_search_entity(self, mock_search_entities):
        mock_search_entities.return_value = {
            "recommended": [],
            "community": [],
        }
        response = self.client.get(
            url_for("jaasstore.search", q="cs:~wombat/k8s")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_search_entities.call_count, 2)
        self.assertEqual(
            mock_search_entities.call_args_list[1],
            call(
                "k8s",
                owner="wombat",
                entity_type=None,
                tags=None,
                sort=None,
                series=None,
                promulgated_only=False,
            ),
        )

    @patch("theblues.charmstore.CharmStore.list")
    def test_user_details(self, mock_list):
        mock_list.return_value = user_entities_data
        response = self.client.get(
            url_for("jaasstore.user_details", username="user-name")
        )
        self.assertEqual(response.status_code, 200)
        context = self.get_context_variable("context")
        self.assertEqual(context["username"], "user-name")
        self.assertEqual(context["bundles_count"], 1)
        self.assertEqual(context["charms_count"], 4)

    @patch("webapp.store.models.get_user_entities")
    def test_user_details_404(self, mock_get_user_entities):
        mock_get_user_entities.return_value = {"bundles": [], "charms": []}
        response = self.client.get(
            url_for("jaasstore.user_details", username="user-name")
        )
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
        self.check_entity(
            mock_entity,
            "charm",
            url_for("jaasstore.details", charm_or_bundle_name="apache2"),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="apache2",
                series_or_version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_series(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="apache2",
                series_or_version="wily",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_charm_series_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="apache2",
                series_or_version="wily",
                version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for("jaasstore.details", charm_or_bundle_name="k8s-bundle"),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="k8s-bundle",
                series_or_version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_series(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="k8s-bundle",
                series_or_version="wily",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_details_bundle_series_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.details",
                charm_or_bundle_name="k8s-bundle",
                series_or_version="wily",
                version=14,
            ),
        )

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
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="apache2",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="apache2",
                series_or_version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_series(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="apache2",
                series_or_version="wily",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_charm_series_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "charm",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="apache2",
                series_or_version="wily",
                version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="k8s-bundle",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="k8s-bundle",
                series_or_version=14,
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_series(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="k8s-bundle",
                series_or_version="wily",
            ),
        )

    @patch("theblues.charmstore.CharmStore.entity")
    def test_user_entity_bundle_series_version(self, mock_entity):
        self.check_entity(
            mock_entity,
            "bundle",
            url_for(
                "jaasstore.user_entity",
                username="user-name",
                charm_or_bundle_name="k8s-bundle",
                series_or_version="wily",
                version=14,
            ),
        )

    @patch("theblues.terms.Terms.get_terms")
    def test_terms(self, mock_terms):
        mock_terms.return_value = MagicMock(content="Special terms")
        response = self.client.get(url_for("jaasstore.terms", name="myterm"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Special terms")

    @patch("theblues.terms.Terms.get_terms")
    def test_terms_with_revision(self, mock_terms):
        mock_terms.return_value = MagicMock(content="Special terms")
        response = self.client.get(
            url_for("jaasstore.terms", name="myterm", revision=99)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Special terms")

    @patch("theblues.terms.Terms.get_terms")
    def test_terms_none(self, mock_terms):
        mock_terms.side_effect = ServerError
        response = self.client.get(url_for("jaasstore.terms", name="myterm"))
        self.assertEqual(response.status_code, 404)

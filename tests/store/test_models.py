import unittest
from tests.store.testdata import bundle_data, charm_data, search_data
from unittest.mock import patch

from webapp.store import models


class TestStoreModels(unittest.TestCase):
    @patch("theblues.charmstore.CharmStore.search")
    def test_search_entities(self, mock_search):
        mock_search.return_value = search_data
        results = models.search_entities("apache2")
        self.assertEqual(len(results["community"]), 8)
        self.assertEqual(len(results["recommended"]), 2)

    @patch("theblues.charmstore.CharmStore.search")
    def test_search_entities_none(self, mock_search):
        mock_search.return_value = []
        results = models.search_entities("apache2")
        self.assertEqual(len(results["community"]), 0)
        self.assertEqual(len(results["recommended"]), 0)

    def test_parse_charm_data(self):
        charm = models._parse_charm_data(charm_data)
        self.assertEqual(
            charm["archive_url"],
            "https://api.jujucharms.com/v5/apache2-26/archive",
        )
        self.assertEqual(
            charm["bugs_url"], "https://bugs.launchpad.net/apache2-charm"
        )
        self.assertIsNone(charm["bzr_url"])
        self.assertEqual(charm["card_id"], "apache2-26")
        self.assertEqual(
            charm["channels"], [{"Channel": "stable", "Current": True}]
        )
        self.assertTrue(
            "The Apache Software Foundation's goal" in charm["description"]
        )
        self.assertEqual(charm["display_name"], "apache2")
        self.assertEqual(
            charm["homepage"], "https://launchpad.net/apache2-charm"
        )
        self.assertEqual(
            charm["icon"], "https://api.jujucharms.com/v5/apache2-26/icon.svg"
        )
        self.assertEqual(charm["id"], "cs:apache2-26")
        self.assertTrue(charm["is_charm"])
        self.assertEqual(charm["latest_revision"], {
            'full_id': 'cs:precise/apache2-27', 'id': 27, 'url': 'apache2/precise/27'
        })
        self.assertEqual(
            charm["options"].get("apt-key-id"),
            {
                "Type": "string",
                "Description": (
                    "A PGP key id.  This is used with PPA and the source "
                    "option to import a PGP public key for verifying "
                    "repository signatures. This value must match the PPA "
                    "for apt-source."
                ),
                "Default": "",
            },
        )
        self.assertEqual(charm["owner"], "apache2-charmers")
        self.assertIsNone(charm["promulgated"])
        self.assertEqual(
            charm["provides"].get("apache-website"),
            {
                "Name": "apache-website",
                "Role": "provider",
                "Interface": "apache-website",
                "Optional": False,
                "Limit": 0,
                "Scope": "container",
            },
        )
        self.assertEqual(
            charm["requires"].get("balancer"),
            {
                "Name": "balancer",
                "Role": "requirer",
                "Interface": "http",
                "Optional": False,
                "Limit": 1,
                "Scope": "global",
            },
        )
        self.assertEqual(charm["resources"], {})
        self.assertTrue(len(charm["revision_list"]) > 0)
        self.assertEqual(charm["revision_list"][0], 'cs:precise/apache2-27')
        self.assertEqual(charm["revision_number"], 26)
        self.assertEqual(len(charm["revisions"]), 10)
        self.assertEqual(charm["series"], ["xenial", "trusty", "bionic"])
        self.assertEqual(charm["tags"], ["app-servers"])
        self.assertEqual(charm["url"], "apache2/26")

    def test_parse_charm_data_terms(self):
        charm_data["Meta"]["terms"] = ["special-term/99", "another-term"]
        charm = models._parse_charm_data(charm_data)
        self.assertEqual(
            charm["term_ids"],
            [
                {
                    "id": "special-term/99",
                    "name": "special-term",
                    "revision": 99,
                },
                {
                    "id": "another-term",
                    "name": "another-term",
                    "revision": None,
                },
            ],
        )

    def test_parse_charm_data_supported(self):
        charm_data["Meta"]["extra-info"]["supported"] = "true"
        charm_data["Meta"]["extra-info"]["price"] = "99"
        charm_data["Meta"]["extra-info"][
            "description"
        ] = "Great ol' charm\nthis one"
        charm = models._parse_charm_data(charm_data)
        self.assertTrue(charm["supported"])
        self.assertEqual(charm["supported_price"], "99")
        self.assertEqual(
            charm["supported_description"],
            "<p>Great ol' charm<br />\nthis one</p>",
        )

    def test_parse_bundle_data(self):
        bundle = models._parse_bundle_data(bundle_data)
        self.assertEqual(
            bundle["archive_url"],
            (
                "https://api.jujucharms.com/v5/bundle/"
                "canonical-kubernetes-466/archive"
            ),
        )
        self.assertEqual(
            bundle["bundle_visulisation"],
            (
                "https://api.jujucharms.com/v5/bundle/canonical-kubernetes-466"
                "/diagram.svg"
            ),
        )
        self.assertEqual(bundle["card_id"], "bundle/canonical-kubernetes-466")
        self.assertEqual(
            bundle["channels"],
            [
                {"Channel": "stable", "Current": False},
                {"Channel": "candidate", "Current": False},
                {"Channel": "beta", "Current": False},
                {"Channel": "edge", "Current": False},
            ],
        )
        self.assertEqual(
            bundle["description"],
            "<p>A highly-available, production-grade Kubernetes cluster.</p>",
        )
        self.assertEqual(
            bundle["display_name"], "The Charmed Distribution of Kubernetes"
        )
        self.assertEqual(bundle["id"], "cs:bundle/canonical-kubernetes-466")
        self.assertFalse(bundle["is_charm"])
        self.assertEqual(bundle["latest_revision"], {'id': 530, 'full_id': 'cs:bundle/canonical-kubernetes-530', 'url': 'canonical-kubernetes/bundle/530'})
        self.assertEqual(bundle["owner"], "containers")
        self.assertIsNone(bundle["promulgated"])
        self.assertEqual(bundle["revision_number"], 466)
        self.assertEqual(bundle["series"], ["bionic"])
        self.assertIsNone(bundle["tags"])
        self.assertEqual(bundle["units"], 10)
        self.assertEqual(bundle["url"], "canonical-kubernetes/bundle/466")

    def test_parse_bundle_data_supported(self):
        bundle_data["Meta"]["extra-info"]["supported"] = "true"
        bundle_data["Meta"]["extra-info"]["price"] = "99"
        bundle_data["Meta"]["extra-info"][
            "description"
        ] = "Great ol' bundle\nthis one"
        bundle = models._parse_bundle_data(bundle_data)
        self.assertTrue(bundle["supported"])
        self.assertEqual(bundle["supported_price"], "99")
        self.assertEqual(
            bundle["supported_description"],
            "<p>Great ol' bundle<br />\nthis one</p>",
        )

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
        self.assertIsNone(charm["latest_revision"])
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
        self.assertIsNone(charm["revision_list"], "bob")
        self.assertEqual(charm["revision_number"], 26)
        self.assertEqual(len(charm["revisions"]), 10)
        self.assertEqual(charm["series"], ["xenial", "trusty", "bionic"])
        self.assertEqual(charm["tags"], ["app-servers"])
        self.assertEqual(charm["url"], "apache2/26")

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
                {"Channel": "stable", "Current": True},
                {"Channel": "candidate", "Current": False},
                {"Channel": "beta", "Current": False},
                {"Channel": "edge", "Current": False},
            ],
        )
        self.assertEqual(
            bundle["description"],
            "<p>A highly-available, production-grade Kubernetes cluster.</p>",
        )
        self.assertEqual(bundle["display_name"], "canonical kubernetes")
        self.assertEqual(bundle["id"], "cs:bundle/canonical-kubernetes-466")
        self.assertFalse(bundle["is_charm"])
        self.assertIsNone(bundle["latest_revision"])
        self.assertEqual(bundle["owner"], "containers")
        self.assertIsNone(bundle["promulgated"])
        self.assertEqual(bundle["revision_number"], 466)
        self.assertEqual(bundle["series"], ["bionic"])
        self.assertIsNone(bundle["tags"])
        self.assertEqual(bundle["units"], 10)
        self.assertEqual(bundle["url"], "canonical-kubernetes/bundle/466")

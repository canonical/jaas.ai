import copy
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

    @patch("theblues.charmstore.CharmStore.fetch_interfaces")
    def test_fetch_provides(self, mock_fetch_interfaces):
        mock_fetch_interfaces.return_value = [None, None, search_data]
        results = models.fetch_provides("mysql")
        self.assertEqual(len(results["community"]), 8)
        self.assertEqual(len(results["recommended"]), 2)

    @patch("theblues.charmstore.CharmStore.fetch_interfaces")
    def test_fetch_requires(self, mock_fetch_interfaces):
        mock_fetch_interfaces.return_value = [None, None, search_data]
        results = models.fetch_requires("mysql")
        self.assertEqual(len(results["community"]), 8)
        self.assertEqual(len(results["recommended"]), 2)

    def test_charm(self):
        charm = models.Charm(charm_data)
        self.assertTrue(charm.archive_url.endswith("apache2-26/archive"))
        self.assertEqual(
            charm.bugs_url, "https://bugs.launchpad.net/apache2-charm"
        )
        self.assertEqual(charm.card_id, "apache2-26")
        self.assertEqual(
            charm.channels, [{"Channel": "stable", "Current": True}]
        )
        self.assertTrue(
            "The Apache Software Foundation's goal" in charm.description
        )
        self.assertEqual(charm.display_name, "apache2")
        self.assertEqual(charm.homepage, "https://launchpad.net/apache2-charm")
        self.assertTrue(charm.icon.endswith("apache2-26/icon.svg"))
        self.assertEqual(charm.id, "cs:apache2-26")
        self.assertEqual(charm.canonical_url, "https://jaas.ai/apache2")
        self.assertTrue(charm.is_charm)
        self.assertEqual(
            charm.options.get("apt-key-id"),
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
        self.assertEqual(charm.owner, "apache2-charmers")
        self.assertIsNone(charm.promulgated)
        self.assertEqual(
            charm.provides.get("apache-website"),
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
            charm.requires.get("balancer"),
            {
                "Name": "balancer",
                "Role": "requirer",
                "Interface": "http",
                "Optional": False,
                "Limit": 1,
                "Scope": "global",
            },
        )
        self.assertEqual(charm.resources, {})
        self.assertTrue(len(charm.revision_list) > 0)
        self.assertEqual(charm.revision_list[0], "cs:precise/apache2-27")
        self.assertEqual(charm.revision_number, 26)
        self.assertEqual(len(charm.revisions), 10)
        self.assertEqual(charm.series, ["xenial", "trusty", "bionic"])
        self.assertEqual(charm.tags, ["app-servers"])
        self.assertEqual(charm.url, "apache2/26")

    def test_charm_terms(self):
        data = copy.deepcopy(charm_data)
        data["Meta"]["terms"] = ["special-term/99", "another-term"]
        charm = models.Charm(data)
        self.assertEqual(
            charm.term_ids,
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

    def test_charm_supported(self):
        data = copy.deepcopy(charm_data)
        data["Meta"]["extra-info"]["supported"] = "true"
        data["Meta"]["extra-info"]["price"] = "99"
        data["Meta"]["extra-info"]["description"] = "Great ol' charm\nthis one"
        charm = models.Charm(data)
        self.assertTrue(charm.supported)
        self.assertEqual(charm.supported_price, "99")
        self.assertEqual(
            charm.supported_description, "<p>Great ol' charm\nthis one</p>"
        )

    def test_bundle(self):
        bundle = models.Bundle(bundle_data)
        self.assertTrue(
            bundle.archive_url.endswith(
                "bundle/canonical-kubernetes-466/archive"
            )
        )
        self.assertTrue(
            bundle.bundle_visualisation.endswith(
                "bundle/canonical-kubernetes-466/diagram.svg"
            )
        )
        self.assertEqual(
            bundle.bugs_url, "https://bugs.launchpad.net/charmed-kubernetes"
        )
        self.assertEqual(bundle.card_id, "bundle/canonical-kubernetes-466")
        self.assertEqual(
            bundle.channels,
            [
                {"Channel": "stable", "Current": False},
                {"Channel": "candidate", "Current": False},
                {"Channel": "beta", "Current": False},
                {"Channel": "edge", "Current": False},
            ],
        )
        self.assertEqual(
            bundle.description,
            "<p>A highly-available, production-grade Kubernetes cluster.</p>",
        )
        self.assertEqual(
            bundle.display_name, "The Charmed Distribution of Kubernetes"
        )
        self.assertEqual(
            bundle.homepage, "https://www.ubuntu.com/kubernetes/docs"
        )
        self.assertEqual(bundle.id, "cs:bundle/canonical-kubernetes-466")
        self.assertFalse(bundle.is_charm)
        self.assertEqual(bundle.owner, "containers")
        self.assertIsNone(bundle.promulgated)
        self.assertEqual(bundle.revision_number, 466)
        self.assertEqual(bundle.series, ["bionic"])
        self.assertIsNone(bundle.tags)
        self.assertEqual(bundle.units, 10)
        self.assertEqual(bundle.url, "canonical-kubernetes/bundle/466")

    def test_bundle_supported(self):
        data = copy.deepcopy(bundle_data)
        data["Meta"]["extra-info"]["supported"] = "true"
        data["Meta"]["extra-info"]["price"] = "99"
        data["Meta"]["extra-info"][
            "description"
        ] = "Great ol' bundle\nthis one"
        bundle = models.Bundle(data)
        self.assertTrue(bundle.supported)
        self.assertEqual(bundle.supported_price, "99")
        self.assertEqual(
            bundle.supported_description, "<p>Great ol' bundle\nthis one</p>"
        )

    def test_bundle_icons(self):
        bundle = models.Bundle(bundle_data)
        self.assertTrue(
            bundle.icons[0].endswith(
                "~containers/kubernetes-master-636/icon.svg"
            )
        )
        self.assertTrue(
            bundle.icons[1].endswith(
                "~containers/kubernetes-worker-502/icon.svg"
            )
        )

    def test_bundle_icons_no_match(self):
        data = copy.deepcopy(bundle_data)
        data["Id"] = "cs:nothing-here-123"
        bundle = models.Bundle(data)
        self.assertTrue(
            bundle.icons[0].endswith("~containers/easyrsa-231/icon.svg")
        )
        self.assertTrue(
            bundle.icons[1].endswith("~containers/etcd-411/icon.svg")
        )

    def test_bundle_icons_exact_match(self):
        data = copy.deepcopy(bundle_data)
        data["Id"] = "~containers/kubeapi-load-balancer-613"
        bundle = models.Bundle(data)
        self.assertTrue(
            bundle.icons[0].endswith(
                "~containers/kubeapi-load-balancer-613/icon.svg"
            )
        )
        self.assertTrue(
            bundle.icons[1].endswith("~containers/easyrsa-231/icon.svg")
        )

    def test_bundle_icons_only_one(self):
        data = copy.deepcopy(bundle_data)
        data["Meta"]["bundle-metadata"]["applications"] = {
            "kubernetes-master": {
                "Charm": "cs:~containers/kubernetes-master-636"
            }
        }
        bundle = models.Bundle(data)
        self.assertEqual(len(bundle.icons), 1)
        self.assertTrue(
            bundle.icons[0].endswith(
                "~containers/kubernetes-master-636/icon.svg"
            )
        )

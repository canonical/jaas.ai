import collections
import os
import re
import markdown

from mdx_partial_gfm import PartialGithubFlavoredMarkdownExtension
from jujubundlelib import references
from theblues.charmstore import CharmStore
from theblues.errors import EntityNotFound, ServerError
from theblues.terms import Terms


cs = CharmStore(timeout=5)
terms = Terms("https://api.jujucharms.com/terms/")

SEARCH_LIMIT = 400

markdown = markdown.Markdown(
    extensions=[PartialGithubFlavoredMarkdownExtension()]
)


def search_entities(
    query,
    entity_type=None,
    tags=None,
    sort=None,
    series=None,
    owner=None,
    promulgated_only=None,
):
    includes = [
        "charm-metadata",
        "bundle-metadata",
        "owner",
        "bundle-unit-count",
        "promulgated",
        "supported-series",
    ]
    try:
        entities = cs.search(
            query,
            doc_type=entity_type,
            includes=includes,
            limit=SEARCH_LIMIT,
            owner=owner,
            promulgated_only=False,
            series=series,
            sort=sort,
            tags=tags,
        )
        results = {"community": [], "recommended": []}
        for entity in _parse_list(entities):
            group = "recommended" if entity.promulgated else "community"
            results[group].append(entity)
        return results
    except EntityNotFound:
        return None


def get_reference(entity):
    """From a string, see if we can make an entity reference out of it, using
    all possible methods.
    :param string: a string to turn into a reference.
    :returns: A reference or None.
    """
    reference = None
    try:
        reference = references.Reference.from_jujucharms_url(entity)
    except ValueError:
        pass
    try:
        reference = references.Reference.from_string(entity)
    except ValueError:
        pass
    try:
        reference = references.Reference.from_jujucharms_url(entity)
    except ValueError:
        pass
    try:
        reference = references.Reference.from_fully_qualified_url(entity)
    except ValueError:
        pass
    return reference


def _group_status(entities):
    results = {"community": [], "recommended": []}
    for entity in _parse_list(entities):
        group = "recommended" if entity.promulgated else "community"
        results[group].append(entity)
    return results


def fetch_provides(id):
    results = cs.fetch_interfaces(id, "provides")
    return _group_status(list(results)[2])


def fetch_requires(id):
    results = cs.fetch_interfaces(id, "requires")
    return _group_status(list(results)[2])


def get_user_entities(username):
    includes = [
        "charm-metadata",
        "bundle-metadata",
        "extra-info",
        "owner",
        "bundle-unit-count",
        "bundle-machine-count",
        "supported-series",
        "published",
    ]
    try:
        entities = cs.list(includes=includes, owner=username)
        parsed = _parse_list(entities)
        return _group_entities(parsed)
    except EntityNotFound:
        return None


def get_charm_or_bundle(reference):
    try:
        entity_data = cs.entity(reference, True, include_stats=False)
        return _parse_charm_or_bundle(entity_data, include_files=True)
    except EntityNotFound:
        return None


def get_terms(name, revision=None):
    try:
        terms_data = terms.get_terms(name, revision)
        return terms_data.content
    except ServerError:
        return None


def _parse_list(entities):
    return [_parse_charm_or_bundle(entity) for entity in entities]


def _group_entities(entities):
    groups = {"bundles": [], "charms": []}
    [
        groups["charms" if entity.is_charm else "bundles"].append(entity)
        for entity in entities
    ]
    return groups


def _parse_charm_or_bundle(entity_data, include_files=False):
    meta = entity_data.get("Meta", None)
    is_charm = meta.get("charm-metadata", False)
    if is_charm:
        return Charm(entity_data, include_files)
    else:
        return Bundle(entity_data, include_files)


class Entity:
    """Base class for charms and bundles. Contains the shared attributes and
    methods.
    Classes that extend Entity will need to provide the following methods:
    - _get_metadata
    - _get_metadata
    - _get_display_name
    - _get_tags
    - _get_series
    """

    def __init__(self, entity_data, include_files=False):
        self.id = entity_data["Id"]
        self._ref = references.Reference.from_string(self.id)
        self._meta = entity_data.get("Meta", None)
        self._metadata = self._get_metadata()
        description = self._metadata.get("Description")
        (
            _,
            supported,
            supported_price,
            supported_description,
        ) = self._extract_from_extrainfo()
        bugs_url, homepage = self._extract_from_commoninfo()
        self.files = None
        self.readme = None
        if include_files:
            self.files = self._get_entity_files(self._meta.get("manifest"))
            try:
                # If the readme is not available for the charm we pass
                # unparsed.
                self.readme = self._render_markdown(
                    cs.entity_readme_content(self.id)
                )
            except Exception:
                # Leave the readme unparsed.
                pass
        self.archive_url = cs.archive_url(self._ref)
        self.bugs_url = bugs_url
        self.card_id = self._ref.path()
        self.channels = self._meta.get("published", {}).get("Info")
        # Some entities don't have descriptions, so first check that the
        # description exists before trying to render the Markdown.
        self.description = (
            self._render_markdown(description) if description else None
        )
        self.display_name = self._get_display_name()
        self.homepage = homepage
        self.owner = self._meta.get("owner", {}).get("User")
        self.promulgated = self._meta.get("promulgated", {}).get("Promulgated")
        self.revision_number = self._ref.revision
        self.series = self._get_series()
        self.supported = supported
        self.supported_price = supported_price
        self.supported_description = (
            supported_description
            and self._render_markdown(supported_description)
        )
        self.tags = self._get_tags()
        self.url = self._ref.jujucharms_id()
        self.canonical_url = self._get_canonical_url()

    def _get_canonical_url(self):
        jujucharms_url = self._ref.copy(
            revision=None, series=None
        ).jujucharms_url()
        jaas_url = jujucharms_url.replace(
            "https://jujucharms.com", "https://jaas.ai"
        )
        return jaas_url

    def _render_markdown(self, content):
        """Render markdown for the provided content.
        :content string: Some markdown.
        :returns: HTML as a string.
        """
        html = markdown.convert(content)
        try:
            html = self._convert_http_to_https(html)
        except Exception:
            # Leave the readme unparsed.
            pass
        return html

    def _convert_http_to_https(self, content):
        """Convert any non secure inclusion of assets to secure.
        :param content: the content to parse as a string.
        :returns: the parsed content with http replaces with https
        """
        insensitive_link = re.compile(re.escape('src="http:'), re.IGNORECASE)
        content = insensitive_link.sub('src="https:', content)
        insensitive_link = re.compile(re.escape("src='http:"), re.IGNORECASE)
        content = insensitive_link.sub("src='https:", content)
        return content

    def _get_entity_files(self, manifest=None):
        """Get files for an entity.
        :manifest array: The manifest of the files.
        :returns: The collection of files.
        """
        try:
            files = cs.files(self._ref, manifest=manifest) or {}
            files = collections.OrderedDict(sorted(files.items()))
        except EntityNotFound:
            files = {}
        return files

    def _extract_from_extrainfo(self):
        """Get data from extrainfo.
        :returns: The extracted extrainfo data.
        """
        extra_info = self._meta.get("extra-info", {})
        revisions = extra_info.get("bzr-revisions") or extra_info.get(
            "vcs-revisions"
        )
        supported = bool(extra_info.get("supported", False))
        supported_price = extra_info.get("price")
        supported_description = extra_info.get("description")
        return (revisions, supported, supported_price, supported_description)

    def _parse_display_name(self, name):
        """Clean the name of the charm for readability.
        :param name: the charm/bundle name.
        :returns: a cleaned name for display.
        """
        name = name.replace("-", " ")
        # Hack to rename 'canonical kubernetes'. To be removed when display
        # name has been implemented.
        if name == "canonical kubernetes":
            name = "The Charmed Distribution of Kubernetes"
        return name

    def _extract_from_commoninfo(self):
        """Get data from commonifo.
        :returns: The extracted commoninfo data.
        """
        common_info = self._meta.get("common-info", {})
        bugs_url = common_info.get("bugs-url")
        homepage = common_info.get("homepage")
        return bugs_url, homepage


class Charm(Entity):
    """A charm definition."""

    is_charm = True

    def __init__(self, entity_data, include_files=False):
        super().__init__(entity_data, include_files)
        (revisions, _, _, _) = self._extract_from_extrainfo()
        self.icon = cs.charm_icon_url(self.id)
        self.options = self._meta.get("charm-config", {}).get("Options")
        self.provides = self._metadata.get("Provides")
        self.requires = self._metadata.get("Requires")
        self.resources = self._extract_resources()
        self.revision_list = self._meta.get("revision-info", {}).get(
            "Revisions"
        )
        self.revisions = revisions
        self.series = self._meta.get("supported-series", {}).get(
            "SupportedSeries"
        )
        self.term_ids = self._parse_term_ids()

    def _get_metadata(self):
        """Get the metadata info.
        :returns: The extracted metadata object.
        """
        return self._meta["charm-metadata"]

    def _get_display_name(self):
        """Get the display name for the charm.
        :returns: The parsed display name.
        """
        return self._parse_display_name(self._metadata["Name"])

    def _get_tags(self):
        """Get the list of tags.
        :returns: The array of tags.
        """
        # Some charms do not have tags, so fall back to categories if they
        # exist (mostly on older charms).
        return self._metadata.get("Tags") or self._metadata.get("Categories")

    def _get_series(self):
        """Get the list of series.
        :returns: The array of series.
        """
        return self._meta.get("supported-series", {}).get("SupportedSeries")

    def _parse_term_ids(self):
        """Extract the term names and revisions.
        :returns: a collection of term ids, names and revisions.
        """
        term_ids = self._meta.get("terms")
        if term_ids is None:
            return None
        terms = []
        for term in term_ids:
            parts = term.split("/")
            terms.append(
                {
                    "id": term,
                    "name": parts[0],
                    "revision": int(parts[1]) if len(parts) == 2 else None,
                }
            )
        return terms

    def _extract_resources(self):
        """Extract data from resources metadata.
        :returns: a dictionary of resource name and an array containing
            the file extension, the file link of the resource.
        """
        result = {}
        for resource in self._meta.get("resources", {}):
            resource_url = ""
            if resource["Revision"] >= 0:
                resource_url = cs.resource_url(
                    self._ref, resource["Name"], resource["Revision"]
                )
            result[resource["Name"]] = [
                os.path.splitext(resource["Path"])[1],
                resource_url,
            ]

        return result


class Bundle(Entity):
    """A bundle definition."""

    is_charm = False

    def __init__(self, entity_data, include_files=False):
        super().__init__(entity_data, include_files)
        self.bundle_visualisation = self._get_bundle_visualization()
        self.applications = self._parse_bundle_applications(
            self._metadata["applications"]
        )
        self.units = self._meta.get("bundle-unit-count", {}).get("Count", "")
        self.icons = self._get_icons()

    def _get_metadata(self):
        """Get the metadata info.
        :returns: The extracted metadata object.
        """
        return self._meta["bundle-metadata"]

    def _get_display_name(self):
        """Get the display name for the bundle.
        :returns: The parsed display name.
        """
        return self._parse_display_name(self._ref.name)

    def _get_tags(self):
        """Get the list of tags.
        :returns: The array of tags.
        """
        return self._metadata.get("Tags")

    def _get_series(self):
        """Get the list of series.
        :returns: The array of series.
        """
        # The series is an array to match the charm data.
        return [self._metadata.get("Series")]

    def _get_bundle_visualization(self):
        """Get the url for the bundle visualization.
        :returns: the bundle visualisation URL.
        """
        return cs.bundle_visualization_url(self._ref)

    def _parse_bundle_applications(self, applications):
        """Get the list of applications for a bundle.
        :returns: The array of applications.
        """
        for name, app in applications.items():
            ref = references.Reference.from_string(app["Charm"])
            app["Charm"] = ref.path()
            app["icon"] = cs.charm_icon_url(app["Charm"])
            app["url"] = ref.jujucharms_id()
            app["display_name"] = self._parse_display_name(name)
        return applications

    def _get_icons(self):
        """Get two sensible icons for this bundle.
        :returns: The icon URLS.
        """
        name_parts = self._ref.name.split("-")
        name_parts.insert(0, self._ref.name)
        primary_charm, primary_icon = self._get_icon(name_parts)
        icons = [primary_icon]
        if len(self.applications.keys()) > 1:
            secondary_charm, secondary_icon = self._get_icon(
                name_parts, primary_charm
            )
            icons.append(secondary_icon)
        return icons

    def _get_icon(self, names, previous_match=None):
        """Get a sensible icon for this bundle.
        :names array: A list of possible names to match.
        :previous_match string: A previous name match to ignore.
        :returns: The charm name and icon URL.
        """
        match = None
        # Look for an exact match.
        match = self._find_name_match(names, previous_match)
        # If there is no match then check within app names
        if not match:
            match = self._find_name_match(
                names, previous_match, partial_match=True
            )
        # If there is still no match then return the first/second icon.
        if not match and (
            previous_match is None or len(self.applications) > 1
        ):
            position = 0
            if list(self.applications.keys())[0] == previous_match:
                position = 1
            match = list(self.applications.keys())[position]
        return match, self.applications[match]["icon"]

    def _find_name_match(
        self, names, previous_match=None, partial_match=False
    ):
        """Search a list of names and application names for matches.
        :names array: A list of possible names to match.
        :previous_match string: A previous name match to ignore.
        :partial_match bool: Whether to check within app names.
        :returns: An application name or None.
        """
        for name in names:
            for app_name, app in self.applications.items():
                if app_name == previous_match:
                    # If this charm's icon has already be used then skip it.
                    continue
                # Check if there is an exact match.
                if app_name == name:
                    return name
                # Check if there is match within the parts of the app name.
                if partial_match and name in app_name.split("-"):
                    return app_name

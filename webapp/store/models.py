import os
import re

import gfm
from jujubundlelib import references
from theblues.charmstore import CharmStore
from theblues.errors import EntityNotFound

cs = CharmStore("https://api.jujucharms.com/v5")


def get_charm_or_bundle(reference):
    try:
        entity_data = cs.entity(reference, True)
        return _parse_charm_or_bundle(entity_data)
    except EntityNotFound:
        return None


def _parse_charm_or_bundle(entity_data):
    charm_or_bundle_id = entity_data['Id']
    ref = references.Reference.from_string(charm_or_bundle_id)
    meta = entity_data.get('Meta', None)
    bzr_url, revisions = _extract_from_extrainfo(meta, ref)
    bugs_url, homepage = _extract_from_commoninfo(meta)
    revision_list = meta['revision-info'].get('Revisions')
    latest_revision = {
        'id': int(revision_list[0].split('-')[-1]),
        'full_id': revision_list[0],
        'url': '{}/{}'.format(
            meta['charm-metadata']['Name'],
            int(revision_list[0].split('-')[-1])
        )}

    charm_or_bundle = {
        'archive_url': cs.archive_url(ref),
        'bugs_url': bugs_url,
        'bzr_url': bzr_url,
        'entity_data': entity_data,
        'files': _get_entity_files(ref, meta['manifest']),
        'homepage': homepage,
        'icon': cs.charm_icon_url(charm_or_bundle_id),
        'id': charm_or_bundle_id,
        'card_id': ref.path(),
        'latest_revision': latest_revision,
        'options': meta.get('charm-config', {}).get('Options'),
        'owner': entity_data.get('owner', {}).get('User'),
        'provides': meta['charm-metadata'].get('Provides'),
        'requires': meta['charm-metadata'].get('Requires'),
        'resources': _extract_resources(ref, meta.get('resources', {})),
        'readme': _render_markdown(
            cs.entity_readme_content(charm_or_bundle_id)
        ),
        'revision_list': revision_list,
        'revision_number': ref.revision,
        'revisions': revisions,
        'series': meta.get('supported-series', {}).get('SupportedSeries'),
        'is_charm': 'charm-metadata' in meta
    }

    return charm_or_bundle


def _get_entity_files(ref, manifest=None):
    try:
        files = cs.files(ref, manifest=manifest) or {}
    except EntityNotFound:
        files = {}
    return files


def _extract_resources(ref, resources):
    """Extract data from resources metadata.
        :param ref: The reference of the entity.
        :param resources: the resources metadata associated with the entity.
        :returns: a dictionary of resource name and an array containing
                the file extension, the file link of the resource.
    """
    result = {}
    for resource in resources:
        resource_url = ""
        if resource['Revision'] >= 0:
            resource_url = cs.resource_url(
                ref,
                resource['Name'],
                resource['Revision']
            )
        result[resource['Name']] = [
            os.path.splitext(resource['Path'])[1],
            resource_url
        ]

    return result


def _get_bug_url(name, bugs_url):
    """Create a link to the bug tracker on Launchpad.
        :param name: the charm name.
        :returns: a URL for the bug tracker.
    """
    if bugs_url:
        return bugs_url
    return 'https://bugs.launchpad.net/charms/+source/{}'.format(name)


def _render_markdown(content):
    html = gfm.markdown(content)

    try:
        html = _convert_http_to_https(html)
    except Exception:
        # Leave the readme unparsed.
        pass

    return html


def _convert_http_to_https(content):
    """Convert any non secure inclusion of assets to secure.
        :param content: the content to parse as a string.
        :returns: the parsed content with http replaces with https
    """
    insensitive_link = re.compile(re.escape('src="http:'), re.IGNORECASE)
    content = insensitive_link.sub('src="https:', content)
    insensitive_link = re.compile(re.escape("src='http:"), re.IGNORECASE)
    content = insensitive_link.sub("src='https:", content)
    return content


def _extract_from_extrainfo(charm_data, ref):
    extra_info = charm_data.get('extra-info', {})
    revisions = (
        extra_info.get('bzr-revisions') or
        extra_info.get('vcs-revisions')
    )
    bzr_url = extra_info.get('bzr-url')
    return bzr_url, revisions


def _extract_from_commoninfo(bundle_data):
    common_info = bundle_data.get('common-info', {})
    bugs_url = common_info.get('bugs-url')
    homepage = common_info.get('homepage')
    return bugs_url, homepage


from flask import abort
from theblues.charmstore import CharmStore
from jujubundlelib import references

import requests
import markdown
import gfm
import re


cs = CharmStore("https://api.jujucharms.com/v5")

def get_charm_or_bundle(name):
    try:
        entity_data = cs.entity(name, True)
    except Exception:
        return abort(404, "Entity not found {}".format(name))

    charm_or_bundle_id = entity_data['Id']
    ref = references.Reference.from_string(charm_or_bundle_id)
    meta = entity_data.get('Meta', None)
    bzr_url, revisions = _extract_from_extrainfo(meta, ref)
    bugs_url, homepage = _extract_from_commoninfo(meta)
    revision_list = meta['revision-info'].get('Revisions')

    charm_or_bundle = {
        'archive_url': cs.archive_url(ref),
        'bugs_url': bugs_url,
        'bzr_url': bzr_url,
        'entity_data': entity_data,
        'files': _getEntityFiles(ref, meta['manifest']),
        'homepage': homepage,
        'icon': _parse_charm_icon(charm_or_bundle_id),
        'id': charm_or_bundle_id,
        'latest_revision': _expand_revision(revision_list[0], meta['charm-metadata']['Name']),
        'options': meta.get('charm-config', {}).get('Options'),
        'owner': entity_data.get('owner', {}).get('User'),
        'provides': meta['charm-metadata'].get('Provides'),
        'requires': meta['charm-metadata'].get('Requires'),
        'resources': _extract_resources(ref, meta.get('resources')),
        'readme': _render_markdown(cs.entity_readme_content(charm_or_bundle_id)),
        'revision_list': revision_list,
        'revision_number': ref.revision,
        'revisions': revisions,
        'series': meta.get('supported-series', {}).get('SupportedSeries'),
        'is_charm': 'charm-metadata' in meta
    }

    return charm_or_bundle


def _getEntityFiles(ref, manifest=None):
    try:
        files = cs.files(ref, manifest=manifest)
    except EntityNotFound:
        files = {}
    if not files:
        files = {}
    try:
        readme = cs.entity_readme_content(ref)
    except EntityNotFound:
        readme = None
    return {
        'files': files,
        'readme': readme,
    }


def _parse_charm_icon(charm_id):
    try:
        return cs.charm_icon_url(charm_id)
    except Exception:
        return abort(500, "Entity not found {}".format(charm_id))


def _expand_revision(revision_id, charm_name):
    '''From a revision id, create a Dict.
    @param revision_id A revision id string.
    @param charm_name The name of the charm
    '''

    id = revision_id.split('-')[-1]
    url = charm_name + '/' + id
    return {
        'id': int(id),
        'full_id': revision_id,
        'url': url}


def _extract_resources(ref, data):
    """Extract data from resources metadata.
    @param ref The reference of the entity.
    @param data the resources metadata associated with the entity.
    @return a dictionary of resource name and an array containing
            the file extension, the file link of the resource.
    """
    if not data:
        # if resources are not present return an empty dictionary
        return {}

    try:
        resources = {}
        for i in data:
            resource_url = ""
            if i['Revision'] >= 0:
                resource_url = self.cs.resource_url(ref,
                                                    i['Name'],
                                                    i['Revision'])
            resources[i['Name']] = [os.path.splitext(i['Path'])[1],
                                    resource_url]
    except (KeyError, TypeError, ValueError):
        log.info('Unable to read resources for ',
                    data)
        return {}

    return resources


def _get_bug_url(name, bugs_url):
    '''Create a link to the bug tracker on Launchpad.
    @param name the charm name.
    @return a URL for the bug tracker.
    '''
    if bugs_url:
        return bugs_url
    return 'https://bugs.launchpad.net/charms/+source/{}'.format(name)


def _render_markdown(content):
    try:
        html = gfm.markdown(content)
        html = convert_http_to_https(html)
    except Exception:
        # Leave the readme unparsed.
        pass
    return html


def _convert_http_to_https(content):
    '''Convert any non secure inclusion of assets to secure.
        @param content the content to parse as a string.
        @return the parsed content with http replaces with https
    '''
    insensitive_link = re.compile(re.escape('src="http:'), re.IGNORECASE)
    content = insensitive_link.sub('src="https:', content)
    insensitive_link = re.compile(re.escape("src='http:"), re.IGNORECASE)
    content = insensitive_link.sub("src='https:", content)
    return content


def _bzr_to_launchpad_url(link):
    if link is not None:
        return link.replace('lp:', 'http://code.launchpad.net/')
    else:
        return None


def _extract_from_extrainfo(charm_data, ref):
    extra_info = charm_data.get('extra-info', {})
    revisions = (extra_info.get('bzr-revisions') or
                    extra_info.get('vcs-revisions'))
    bzr_url = extra_info.get('bzr-url')
    return bzr_url, revisions


def _extract_from_commoninfo(bundle_data):
    # ...and common info...
    common_info = bundle_data.get('common-info', {})
    bugs_url = common_info.get('bugs-url')
    homepage = common_info.get('homepage')
    return bugs_url, homepage
import sys
import logging
import tempfile
from packaging.version import parse as parse_version
from importlib import import_module
from pathlib import Path

from .network import Net
from .utils import download
from . import __version__ as current_version

log = logging.getLogger(__name__)

# A trick for checking if this in independent executable or not
try:
    import_module("pip")
except ImportError:
    executable = True
else:
    executable = False

# Helper functions
def _get_api_tags():
    versions = []
    r = Net.requests.get('https://api.github.com/repos/mansuf/mangadex-downloader/git/refs/tags')
    for version_info in r.json():
        versions.append(version_info['ref'].replace('refs/tags/', ''))
    return versions

def _get_asset(version):
    if not version.startswith('v'):
        version = 'v' + version

    r = Net.requests.get('https://api.github.com/repos/mansuf/mangadex-downloader/releases')
    for release_info in r.json():
        if version == release_info['tag_name']:
            assets = release_info['assets']
            pass

def check_version():
    # Get latest version
    versions = _get_api_tags()
    latest_version = max(versions, key=parse_version)

    if latest_version > current_version:
        log.info("There is new version mangadex-downloader ! (%s), you should update it with \"%s\" option" % (
            latest_version,
            '--update'
        ))

def update_app():
    if executable:
        with tempfile.TemporaryDirectory('md_temp') as temp_folder:
            download()



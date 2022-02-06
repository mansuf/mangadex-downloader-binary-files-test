import os
import sys
import logging
import tempfile
import zipfile
from packaging.version import parse as parse_version
from importlib import import_module
from pathlib import Path

from .network import Net
from .utils import download
from . import __version__

current_version = parse_version(__version__)

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
    r = Net.requests.get('https://api.github.com/repos/mansuf/mangadex-downloader-binary-files-test/git/refs/tags')
    for version_info in r.json():
        versions.append(version_info['ref'].replace('refs/tags/', ''))
    return versions

def _get_asset(_version):
    version = str(_version)
    if not version.startswith('v'):
        version = 'v' + version

    r = Net.requests.get('https://api.github.com/repos/mansuf/mangadex-downloader-binary-files-test/releases')
    for release_info in r.json():
        if version == release_info['tag_name']:
            asset = release_info['assets'][0]
            return asset['browser_download_url']

def check_version():
    # Get latest version
    versions = _get_api_tags()
    latest_version = parse_version(max(versions, key=parse_version))

    if latest_version > current_version:
        log.info("There is new version mangadex-downloader ! (%s), you should update it with \"%s\" option" % (
            latest_version,
            '--update'
        ))
        return latest_version
    return None

def update_app():
    try:
        latest_version = check_version()
    except Exception as e:
        log.error("Failed to check update, reason: %s" % e)
        sys.exit(1)

    if latest_version:

        # Get url update
        try:
            url_update = _get_asset(latest_version)
        except Exception as e:
            log.error("Failed to get update url, reason: %s" % e) 
            sys.exit(1)

        current_path = Path(sys.executable).parent

        if executable:
            try:
                temp_folder = Path(tempfile.mkdtemp(suffix='md_downloader_update'))
            except Exception as e:
                log.error("Failed to create temporary folder, reason: %s" % e)
                sys.exit(1)

            update_file_path = str(temp_folder / ('%s.zip' % latest_version))

            # Download update
            try:
                download(url_update, update_file_path)
            except Exception as e:
                log.error("Failed to download update, reason: %s" % e)
                sys.exit(1)

            # Extract udpate
            try:
                with zipfile.ZipFile(update_file_path, 'r') as update:
                    update.extractall()
            except Exception as e:
                log.error("Failed to extract update, reason: %s" % e)
                sys.exit(1)

            extracted_update_path = str(temp_folder / 'mangadex-dl')

            cmd_args = "@echo off && echo \"Updating mangadex-downloader from v%s to v%s\" && " % (
                current_version,
                latest_version
            )
            cmd_args += 'copy /Y \"%s\" \"%s\" && ' % (extracted_update_path, current_path)
            cmd_args += 'rmdir /S /Q \"%s\" && ' % temp_folder
            cmd_args += 'echo \"mangadex-downloader successfully updated to v%s\" && ' % latest_version
            cmd_args += 'echo \"You may close this window\" && pause && exit'
            os.system(cmd_args)
    else:
        log.info('This version mangadex-downloader is up-to-date')



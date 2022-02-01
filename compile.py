import sys
from PyInstaller.__main__ import run

output = 'mangadex-dl-%s' % sys.platform

run([
    __name__,
    'run.py',
    '-n',
    output
])
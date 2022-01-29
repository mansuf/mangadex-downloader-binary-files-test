import sys
from PyInstaller.__main__ import run

output = 'mangadex-dl_%s' % sys.platform

run([
    __name__,
    'run.py',
    '-n',
    output
])
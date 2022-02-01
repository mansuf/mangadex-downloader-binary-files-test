import os
import re

ref = os.environ.get('GITHUB_REF')
print('\"VERSION_TAG=%s\"' % ref.replace('refs/tags/', ''))
# flake8: noqa

# CHANGE VERSION HERE
__Version__ = '0.1.0'

from datetime import datetime
import re
import sys


build_loc = re.compile(r'"build_loc":"(.+)"').search(" ".join(sys.orig_argv))
if build_loc is None:
    datetime_str = datetime.strftime(datetime.now(), "%Y%m%d%H%M")
    needed_version = f'{__Version__}.dev{datetime_str}'
else:
    feed = build_loc.group(1)
    if feed == 'WDOD-Modules':
        needed_version = __Version__
    else:
        needed_version = __Version__ + '.alpha'

__version__ = needed_version

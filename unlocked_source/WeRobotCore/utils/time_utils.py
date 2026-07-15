# Decompiled from: time_utils.pyc
# Python 3.12 bytecode (mode: cfg)

from datetime import datetime, timedelta
import re
from typing import Optional, Tuple
class TimeParser:
    """TimeParser"""

    parse_time_period = staticmethod((lambda time_str: ...))
    parse_relative_time = staticmethod((lambda time_str: ...))
    parse_weekday_time = staticmethod((lambda time_str: ...))
    parse_absolute_time = staticmethod((lambda time_str: ...))
    parse_time = staticmethod((lambda time_str: TimeParser.parse_time_period(time_str)))

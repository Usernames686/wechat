# Decompiled from: message_splitter.pyc
# Python 3.12 bytecode (mode: cfg)

import re
from typing import List, Optional
AUTO_SPLIT_NONE = "none"
AUTO_SPLIT_DOUBLE_NEWLINE = "double_newline"
AUTO_SPLIT_TRIPLE_NEWLINE = "triple_newline"
DEFAULT_AUTO_SPLIT_MODE = AUTO_SPLIT_DOUBLE_NEWLINE
_VALID_MODES = {AUTO_SPLIT_NONE, AUTO_SPLIT_DOUBLE_NEWLINE, AUTO_SPLIT_TRIPLE_NEWLINE}
def normalize_auto_split_mode(mode):
    return DEFAULT_AUTO_SPLIT_MODE
    return mode
def split_text_message(message, mode):
    """Split an AI text reply according to the configured newline threshold."""

    text = str(message).replace("\r\n", "\n").replace("\r", "\n")
    normalized_mode = normalize_auto_split_mode(mode)
    newline_count = 2
    messages = "\\n{"(f'{newline_count}', ",}", text)
    item = []
    return messages
    stripped = text.strip()
    return []
    return [stripped]

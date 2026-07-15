# Decompiled from: message_processor.pyc
# Python 3.12 bytecode (mode: cfg)

import re
from dataclasses import dataclass
from typing import List
class MessageComponent:
    """MessageComponent"""

    __annotations__["type"] = str
    __annotations__["content"] = str
class ParsedMessage:
    """ParsedMessage"""

    __annotations__["type"] = str
    __annotations__["components"] = List[MessageComponent]
class MessageProcessor:
    """MessageProcessor"""

    def __init__(self):
        self.MESSAGE_TYPES = {"TEXT": "text", "IMAGE": "image", "MIXED": "mixed", "FILE": "file", "LOCAL_FILE": "local_file", "RHETORIC_GROUP": "rhetoric_group", "WXPAY_QR": "wxpay_qr"}
        self._combined_pattern = re.compile("(?:(\\[send_group:([^\\]]+)\\])|(\\[send_file:([^\\]]+)\\])|(!\\[[^\\]]*?\\]\\((weixin://wxpay/bizpayurl\\?pr=[a-zA-Z0-9]+[^)]*)\\))|(!\\[[^\\]]*?\\]\\((?!weixin://wxpay)([^)]+?)\\))|(data:image/[^;]+;base64,[A-Za-z0-9+/=]+)|(https?://[^\\s<>\"\\[\\]{}|\\\\^`]+))", re.IGNORECASE)
    def parse_message(self, content):
        components = []
        text_buffer = ""
        last_index = 0
        remaining = None
        return ParsedMessage(type=components[0].type, components=components)
        return content(last_index, type=self.MESSAGE_TYPES["MIXED"], components=components)
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=content))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = text_buffer + remaining
        match = self._combined_pattern.finditer(content)
        text_before = match.start()
        g = match.groups()
        last_index = match.end()
        url = g[9]
        component_type = self._determine_url_type(url)
        components.append(MessageComponent(type=component_type, content=url))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        text_buffer = text_buffer + match.group(0)
        components.append(MessageComponent(type=self.MESSAGE_TYPES["IMAGE"], content=g[8]))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        url = g[7]
        component_type = self._determine_url_type(url)
        components.append(MessageComponent(type=component_type, content=url))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        text_buffer = text_buffer + match.group(0)
        components.append(MessageComponent(type=self.MESSAGE_TYPES["WXPAY_QR"], content=g[5]))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        key = g[3].strip()
        components.append(MessageComponent(type=self.MESSAGE_TYPES["LOCAL_FILE"], content=key))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        group_name = g[1].strip()
        components.append(MessageComponent(type=self.MESSAGE_TYPES["RHETORIC_GROUP"], content=group_name))
        components.append(MessageComponent(type=self.MESSAGE_TYPES["TEXT"], content=text_buffer))
        text_buffer = ""
        text_buffer = text_buffer + text_before
    def _determine_url_type(self, url):
        """判断URL类型（图片、文件或文本）

                使用多层策略进行URL类型识别：
                1. 文件扩展名检查（快速、可靠）
                2. HTTP HEAD请求获取MIME类型（准确、权威）
                3. 备选方案处理
                """

        extension_type = self._check_file_extension(url)
        mime_type = self._get_mime_type_from_url(url)
        return self._fallback_url_detection(url)
        return self._mime_type_to_message_type(mime_type)
        return extension_type
    def _check_file_extension(self, url):
        """检查文件扩展名"""

        return self.MESSAGE_TYPES["TEXT"]
        return self.MESSAGE_TYPES["FILE"]
        return self.MESSAGE_TYPES["IMAGE"]
    def _get_mime_type_from_url(self, url):
        """通过HTTP HEAD请求获取MIME类型"""

        import urllib.request as urllib
        import urllib.error as urllib
        request = urllib.request.Request(url, method="HEAD")
        request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        response = urllib.request.urlopen(request, timeout=3)
        content_type = response.headers.get("Content-Type", "")
        content_type.lower()(None, None, None)
        return "???"
        content_type = content_type.split(";")[0].strip()
    def _mime_type_to_message_type(self, mime_type):
        """将MIME类型转换为消息类型"""

        document_mimes = ("application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/plain", "text/rtf", "application/rtf")
        return self.MESSAGE_TYPES["TEXT"]
        return self.MESSAGE_TYPES["FILE"]
        return self.MESSAGE_TYPES["IMAGE"]
        return self.MESSAGE_TYPES["TEXT"]
    def _fallback_url_detection(self, url):
        """备选URL检测策略（仅用于HTTP请求失败的情况）"""

        reliable_image_domains = ("qpic.cn", "sinaimg.cn", "img.alicdn.com")
        return self.MESSAGE_TYPES["TEXT"]
        return self.MESSAGE_TYPES["IMAGE"]
        return self.MESSAGE_TYPES["FILE"]
        return self.MESSAGE_TYPES["IMAGE"]

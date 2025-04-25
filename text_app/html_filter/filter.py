#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup


class XSSFilter(object):
    __instance = None

    def __init__(self):
        # XSS白名单
        self.valid_tags = {
            "font": ['color', 'size', 'face', 'style', 'class'],
            'b': ['class'],
            'div': ['class'],
            "span": ['class', 'style'],
            "table": [
                'border', 'cellspacing', 'cellpadding','class'
            ],
            'th': [
                'colspan', 'rowspan','class'
            ],
            'td': [
                'colspan', 'rowspan','class'
            ],
            "a": ['href', 'target', 'name', 'class'],
            "img": ['src', 'alt', 'title', 'class'],
            'p': [
                'align','class'
            ],
            "pre": ['class'],
            "hr": ['class'],
            'strong': ['class', 'style'],
        }
    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = super.__new__(cls)
            return cls.__instance
    # @classmethod
    # def instance(cls):
    #     if not cls.__instance:
    #         obj = cls()
    #         cls.__instance = obj
    #     return cls.__instance

    def process(self, content):
        soup = BeautifulSoup(content, 'lxml')
        # 遍历所有HTML标签
        for tag in soup.find_all(recursive=True):
            # 判断标签名是否在白名单中
            if tag.name not in self.valid_tags:
                tag.hidden = True
                if tag.name not in ['html', 'body']:
                    tag.hidden = True
                    tag.clear()
                continue
            # 当前标签的所有属性白名单
            attr_rules = self.valid_tags[tag.name]
            keys = list(tag.attrs.keys())
            for key in keys:
                if key not in attr_rules:
                    del tag[key]

        return soup.renderContents()



if __name__ == '__main__':
    html = """<p class="title">
                        <b>The Dormouse's story</b>
                    </p>
                    <p class="story">
                        <div name='root'>
                            Once upon a time there were three little sisters; and their names were
                            <a href="http://example.com/elsie" class="sister c1" style='color:red;background-color:green;' id="link1"><!-- Elsie --></a>
                            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                            <a href="http://example.com/tillie" class="sister" id="link3">Tilffffffffffffflie</a>;
                            and they lived at the bottom of a well.
                            <script>alert(123)</script>
                        </div>
                    </p>
                    <p class="story">...</p>"""

    v = XSSFilter.instance().process(html)
    print(v)

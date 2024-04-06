# coding: utf8
import os

from atlassian import  Confluence

CONFLUENCE_URL = os.environ.get("BAMBOO_URL", "https://confluence.zhihuiya.com/")

ATLASSIAN_USER = os.environ.get("ATLASSIAN_USER", "renjiajia")
ATLASSIAN_PASSWORD = os.environ.get("ATLASSIAN_PASSWORD", "Paic,1026")


class TestBasic:

    def test_init_confluence(self):
        Confluence(url=CONFLUENCE_URL, username=ATLASSIAN_USER, password=ATLASSIAN_PASSWORD)

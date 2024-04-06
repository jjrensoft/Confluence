# coding=utf-8
import json
import logging
import os
import tempfile
import pytest
from bs4 import BeautifulSoup

from atlassian import Confluence


class TestConfluenceAttach():
    secret_file = "../credentials.secret"

    """
        Keep the credentials private, the file is excluded. There is an example for credentials.secret
        See also: http://www.blacktechdiva.com/hide-api-keys/

        {
          "host" : "https://localhost:8080",
          "username" : "john_doe",
          "password" : "12345678"
        }
    """

    def test_confluence_attach_file_1(self):
        try:
            with open(self.secret_file) as json_file:
                credentials = json.load(json_file)
        except Exception as err:
            logging.ERROR("[{0}]: {1}".format(self.secret_file, err))
            #self.fail("[{0}]: {1}".format(self.secret_file, err))

        confluence = Confluence(
            url=credentials["host"],
            username=credentials["username"],
            password=credentials["password"],
        )

        # individual configuration
        space = "~renjiajia"
        title = "atlassian-python-rest-api-wrapper"


        fd, filename = tempfile.mkstemp("w")
        os.write(fd, b"Hello World - Version 1")

        # upload a new file
        #result = confluence.attach_file(filename, "", page_id=129009607,title=title, space=space, comment="upload from jiajia")
        page_content = confluence.get_page_by_id("193389165",expand="body.storage")
        print(page_content["body"]["storage"]["value"])
        html =page_content["body"]["storage"]["value"]
        soup = BeautifulSoup(html, 'html.parser')
        outline = []
        # 提取标题
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags:
            title = h2.text
            outline.append(title)

        # 提取标题下面的段落
        for h2 in h2_tags:
            p_tags = h2.find_next_siblings('p')
            for p in p_tags:
                content = p.text
                outline.append('  ' + content)

        # 提取表格
        table_tags = soup.find_all('table')
        for table in table_tags:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                row_content = []
                for cell in cells:
                    row_content.append(cell.text)
                outline.append('    ' + '|'.join(row_content))

        print(outline)



'''
        # attach_file() returns: {'results': [{'id': 'att144005326', 'type': 'attachment', ...
        assert "results" in result
        assert  not ("statusCode" in result)

        # upload a new version of an existing file
        os.lseek(fd, 0, 0)
        os.write(fd, b"Hello Universe - Version 2")
        result = confluence.attach_file(filename, "", title=title, space=space, comment="upload from unittest")

        # attach_file() returns: {'id': 'att144005326', 'type': 'attachment', ...
        assert ("id" in result)
        assert  not ("statusCode" in result)

        os.close(fd)
        os.remove(filename)

    def test_confluence_attach_file_2(self):
        try:
            with open(self.secret_file) as json_file:
                credentials = json.load(json_file)
        except Exception as err:
            self.fail("[{0}]: {1}".format(self.secret_file, err))

        confluence = Confluence(
            url=credentials["host"],
            username=credentials["username"],
            password=credentials["password"],
        )

        # individual configuration
        space = "~renjiajia"
        title = "atlassian-python-rest-api-wrapper"

        # TODO: check if page are exists

        fd, filename = tempfile.mkstemp("w")
        os.write(fd, b"Hello World - Version 1")

        name = os.path.basename(tempfile.mkstemp()) + ".txt"

        # upload a new file
        result = confluence.attach_file(
            filename,
            name,
            content_type="text/plain",
            title=title,
            space=space,
            comment="upload from unittest",
        )

        # attach_file() returns: {'results': [{'id': 'att144005326', 'type': 'attachment', ...
        assert ("results" in result)
        assert not ("statusCode" in result)

        # upload a new version of an existing file
        os.lseek(fd, 0, 0)
        os.write(fd, b"Hello Universe - Version 2")
        result = confluence.attach_file(
            filename,
            name,
            content_type="text/plain",
            title=title,
            space=space,
            comment="upload from unittest",
        )

        # attach_file() returns: {'id': 'att144005326', 'type': 'attachment', ...
        assert ("id" in result)
        assert not ("statusCode" in result)

        os.close(fd)
        os.remove(filename)

    def test_confluence_attach_content(self):
        try:
            with open(self.secret_file) as json_file:
                credentials = json.load(json_file)
        except Exception as err:
            self.fail("[{0}]: {1}".format(self.secret_file, err))

        confluence = Confluence(
            url=credentials["host"],
            username=credentials["username"],
            password=credentials["password"],
        )

        # individual configuration
        space = "~renjiajia"
        title = "atlassian-python-rest-api-wrapper"

        attachment_name = os.path.basename(tempfile.mkstemp())

        # upload a new file
        content = b"Hello World - Version 1"
        result = confluence.attach_content(
            content,
            attachment_name,
            "text/plain",
            title=title,
            space=space,
            comment="upload from unittest",
        )

        # attach_file() returns: {'results': [{'id': 'att144005326', 'type': 'attachment', ...
        assert ("results" in result)
        assert not ("statusCode" in result)

        # upload a new version of an existing file
        content = b"Hello Universe - Version 2"
        result = confluence.attach_content(
            content,
            attachment_name,
            "text/plain",
            title=title,
            space=space,
            comment="upload from unittest",
        )

        # attach_file() returns: {'id': 'att144005326', 'type': 'attachment', ...
        assert ("id" in result)
        assert not("statusCode" in result)
        '''


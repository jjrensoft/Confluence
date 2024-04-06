# coding=utf-8
import json
import logging

from bs4 import BeautifulSoup

from atlassian import Confluence
from gptdemo.gptdemo import Gptdemo


class TestConfluence():
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

    def test_confluence_content(self):
        try:
            with open(self.secret_file) as json_file:
                credentials = json.load(json_file)
        except Exception as err:
            logging.ERROR("[{0}]: {1}".format(self.secret_file, err))
            # self.fail("[{0}]: {1}".format(self.secret_file, err))

        confluence = Confluence(
            url=credentials["host"],
            username=credentials["username"],
            password=credentials["password"],
        )

        page_content = confluence.get_page_by_id("193389165", expand="body.storage")
        print(page_content["body"]["storage"]["value"])
        html = page_content["body"]["storage"]["value"]
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
        msg = self.msg_content(outline)
        result = Gptdemo(msg)
        print(result)

    def msg_content(self, content):
        prompt = f'''你是一名测试专家, 请直接根据需求文档内容,为我整理测试点和测试用例,步骤如下:\
        仔细阅读需求文档,理解其中的需求点\
        根据需求点划分,整理出测试点清单\
        针对每个测试点,列出相关需求点引用\
        为每个测试点设计详细的测试用例\
        测试点清单和测试用例格式如下:\
        测试点1:\
        相关需求:xxx,xxx\
        测试用例:\
        步骤1:\
        步骤2:\
        预期结果:\
        测试点2:\
        相关需求:xxx\
        测试用例:\
        步骤1:\
        步骤2:\
        预期结果:\
        等等\
        请根据需求文档内容{content},为我返回测试点清单和对应的测试用例,谢谢!
        '''
        return prompt

import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import private_constant

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}
proxies = {'http': 'http://127.0.0.1:8888', 'https': 'http:127.0.0.1:8888'}


class Song:
    def __init__(self, id_):
        self.id = id_
        res = requests.get(private_constant.target.replace('$song_id', self.id),
                           headers=headers, proxies=proxies, verify=r"FiddlerRoot.pem")
        self.html = res.text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def title(self):
        return self.soup.select_one('.information .title strong').text

    def artist(self):
        return self.soup.select_one('.information .artist').text

    def detail(self):
        return self.soup.find(class_='detail_txt').text

    def auction_id(self):
        return re.search(r'/auction/(?P<id>[0-9]+)', self.html).group('id')

    def copy_info(self):
        target = self.soup.find(class_='lst_copy_info')
        keys = [dt.text for dt in target.find_all('dt')]
        values = [dd.text for dd in target.find_all('dd')]
        output = dict(zip(keys, values))
        output.update({'crawling_dttm': datetime.now().strftime('%Y-%m-%d')})
        return output

    def recent_12months_royalties(self):
        target = self.soup.find(class_='tbl_flex')
        keys = [dt.text[:2] for dt in target.find_all('dt')]
        values = [dd.text for dd in target.find_all('dt')]
        return dict(zip(keys, values))

    def recent_12months_royalty_total(self):
        return self.soup.find('dt', text='최근 12개월 저작권료 (1주 기준)').find_next_sibling('dd').text

    def recent_5years_royalties(self):
        return re.search(r'arr_amt_royalty_ym\[.+\] ?= ?(?P<royalty>{.+})', self.html).group('royalty')

    @staticmethod
    # TODO
    def recent_month_royalty(year, month, royalties):
        now = datetime.now()
        assert now.year - 5 < year <= now.year, f'The value must be within 5 years. actual: {year}'
        assert 0 < month < now.month, f'The value must be before last month. actual: {month}'
        return json.loads(royalties)[str(year)][str(month)]

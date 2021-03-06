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

    def detail_royalty_recent_12months(self):
        target = self.soup.find(class_='tbl_flex')
        keys = [dt.text[:2] for dt in target.find_all('dt')]
        values = [only_amount(dd.text) for dd in target.find_all('dd')]
        return dict(zip(keys, values))

    def total_royalty_recent_12months(self):
        total_amount_text = self.soup.find('dt', text='최근 12개월 저작권료 (1주 기준)').find_next_sibling('dd').text
        return only_amount(total_amount_text)

    def monthly_royalty_recent_5years(self):
        return re.search(r'arr_amt_royalty_ym\[.+\] ?= ?(?P<royalty>{.+})', self.html).group('royalty')

    def auction_info(self):
        auctions = self.soup.find_all(class_='lst_numb_card')
        result = []
        for auction in auctions:
            keys = [dt.text for dt in auction.find_all('dt')]
            values = [dd.text for dd in auction.find_all('dd')]
            result.append({'title': auction.h2.text.strip(), **dict(zip(keys, values))})
        return result

    def to_song(self):
        return (self.id, self.auction_id(), self.title(), self.artist(),
                self.detail(), json.dumps(self.copy_info(), ensure_ascii=False),
                json.dumps(self.auction_info(), ensure_ascii=False), datetime.now())

    def to_recent_detail_royalty(self):
        detail_royalty = self.detail_royalty_recent_12months()
        monthly_royalty = json.loads(self.monthly_royalty_recent_5years())
        year = max(monthly_royalty.keys())
        month = max(monthly_royalty[year].keys())
        return (self.id, f'{year}-{month}-01',
                monthly_royalty[year][month], self.total_royalty_recent_12months(),
                detail_royalty['방송'], detail_royalty['전송'], detail_royalty['복제'], detail_royalty['공연'],
                detail_royalty['해외'], detail_royalty['기타'],  datetime.now())

    def to_monthly_royalties(self):
        monthly_royalty = json.loads(self.monthly_royalty_recent_5years())
        return [(self.id, f'{year}-{month}-01', value)
                for year, months in monthly_royalty.items() for month, value in months.items()]


def only_amount(text):
    return re.search(r'(?P<price>\d+)원', text).group('price')

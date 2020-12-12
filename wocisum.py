import json
import re
import requests
import private_constant
from datetime import datetime
from bs4 import BeautifulSoup



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}
proxies = {'http': 'http://127.0.0.1:8888', 'https': 'http:127.0.0.1:8888'}

id = '936'
res = requests.get(private_constant.target.replace('$song_id', id),
                   headers=headers, proxies=proxies, verify=r"FiddlerRoot.pem")
html = res.text
soup = BeautifulSoup(html, 'html.parser')

info = soup.find(class_='information')
title = info.find(class_='title').strong.get_text()
artist = info.find(class_='artist').get_text()
detail = soup.find(class_='detail_txt').get_text()
auction_id = re.search(r'/auction/(?P<id>[0-9]+)', html).group('id')

keys = [dt.text for dt in soup.select('.lst_copy_info dt')]
values = [dd.text for dd in soup.select('.lst_copy_info dd')]
copy_info = dict(zip(keys, values))
copy_info.update({'crawling_dttm': datetime.now().strftime('%Y-%m-%d')})

recent_5years_royalties = re.search(r'arr_amt_royalty_ym\[.+\] ?= ?(?P<royalty>{.+})', html).group('royalty')

year = '2020'
month = '11'
month_royalty = json.loads(recent_5years_royalties)[year][month]

recent_12months_royalty_keys = [key.text[:2] for key in soup.select('.tbl_flex dt')]
recent_12months_royalty_values = [key.text for key in soup.select('.tbl_flex dd')]
recent_12months_royalties = dict(zip(recent_12months_royalty_keys, recent_12months_royalty_values))
recent_12months_royalty_total = soup.find('dt', text='최근 12개월 저작권료 (1주 기준)').find_next_sibling('dd').text

print(id)
print(title)
print(artist)
print(detail)
print(auction_id)
print(copy_info)
print(recent_12months_royalties)
print(recent_12months_royalty_total)
from urllib import request
from bs4 import BeautifulSoup
import private_constant
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'musicoin_CID=56fd2442e9ee463aa8de362ab6266135; _fbp=fb.1.1602393468210.1437410477; _ga=GA1.2.1591153744.1602393469; SID=kqqgcggib1ndmrfdmmmka3i19j; _gid=GA1.2.1013599040.1607216146; _gat_gtag_UA_101753043_1=1',
}
res = requests.get(private_constant.target, headers=headers)
print(res.text)



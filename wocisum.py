import requests
import private_constant

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

proxies = {'http': 'http://127.0.0.1:8888', 'https': 'http:127.0.0.1:8888'}
res = requests.get(private_constant.target, headers=headers, proxies=proxies, verify=r"FiddlerRoot.pem")
print(res.text)

from urllib import request
from bs4 import BeautifulSoup
import constant

target = request.urlopen(constant.target)
bs = BeautifulSoup(target, 'html.parser')
print(bs.a)


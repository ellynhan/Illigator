from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from collections import Counter
from konlpy.tag import Hannanum
import pytagcloud
import webbrowser
import random

gamble_keywords = ['충전', '환전', '카지노', '이벤트', '출금', '신규가입', '충환전', '입금계좌', '게임머니', '베팅', '보장', '안전놀이터', '토토']

class url_struct:
    def __init__(self, internal, url, depth):
        self.internal = internal  # internal: 1, external: 0
        self.url = url
        self.depth = depth


url_list = []
visited_url_list = []

internal_depth = 1
external_depth = 1

r = lambda: random.randint(0, 255)
color = lambda: (r(), r(), r())


def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    print(count)
    return [{'color': color(), 'tag': n, 'size': c * multiplier} \
            for n, c in count.most_common(ntags)]


def get_hit_list(keywords, text):
    hit_list = {}
    score = 0
    for keyword in keywords:
        keyword_count = text.count(keyword)
        if keyword_count > 0:
            hit_list.update({keyword: keyword_count})
            score += keyword_count
    return [hit_list, score]


def draw_cloud(tags, filename, fontname='Cantarell', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)


def link_crawler(struct):
    while len(url_list):
        count = 0
        if (struct.internal and (struct.depth < internal_depth)) or \
                (not struct.internal and (struct.depth < external_depth)):
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
            driver.implicitly_wait(3)
            driver.get(url_list[0].url)
            print("["+str(url_list[0].depth)+"] Crawling " + url_list[0].url + "...")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            result = get_hit_list(gamble_keywords, soup.text)
            print(url_list[0].url, result)
            visited_url_list.append(url_list[0].url)

            # get internal/external link and append to url list
            net = urlparse(url_list[0].url).netloc

            hrefs = soup.findAll("a")
            for href in hrefs:
                if not ('href' in href.attrs):
                    continue
                if href in visited_url_list or href in url_list:
                    continue
                if href.attrs["href"].startswith('/'):  # internal link start with
                    ap = url_struct(1, str(net + href.attrs["href"]), struct.depth + 1)
                    url_list.append(ap)
                elif urlparse(href.attrs["href"]).netloc == net:  # internal link
                    ap = url_struct(1, str(href.attrs["href"]), struct.depth + 1)
                    url_list.append(ap)
                else:  # external link
                    ap = url_struct(0, str(href.attrs["href"]), struct.depth + 1)
                    url_list.append(ap)
                count += 1

            print("Delete +" + url_list[0].url)
            del url_list[0]

        # exit()  # for test only one link#


if __name__ == "__main__":
    start_struct = url_struct(0, "http://betmoa03.com/", 0)
    url_list.append(start_struct)
    link_crawler(start_struct)

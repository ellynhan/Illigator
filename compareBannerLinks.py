from bs4 import BeautifulSoup
from urllib.parse import urlparse

def compare_banner_link(url1, url2, driver):
    driver.get(url1)
    html1 = driver.page_source
    driver.get(url2)
    html2 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')
    hrefs1 = soup1.findAll("a")
    hrefs2 = soup2.findAll("a")
    net1 = urlparse(url1).netloc
    net2 = urlparse(url2).netloc
    external_link_1 = []
    external_link_2 = []
    for href in hrefs1:
        if not ('href' in href.attrs):
            continue
        if href.attrs["href"].startswith('/') or urlparse(
                href.attrs["href"]).netloc == net1:  # internal link start with
            continue
        else:  # external link
            external_link_1.append(href)

    for href in hrefs2:
        if not ('href' in href.attrs):
            continue
        if href.attrs["href"].startswith('/') or urlparse(
                href.attrs["href"]).netloc == net2:  # internal link start with
            continue
        else:  # external link
            external_link_2.append(href)

    bigger = []
    smaller = []
    compare_length = len(external_link_1) >= len(external_link_2)
    bigger = external_link_1 if compare_length == True else external_link_2
    smaller = external_link_2 if compare_length == True else external_link_1

    count = 0
    for link in smaller:
        if bigger.__contains__(link):
            count += 1
            
    result = 0 if count == 0 else count/len(bigger)*100
    return result 


if __name__ == "__main__":
    compare_banner_link("url1", "url2")

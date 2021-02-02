from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from selenium import webdriver

def extract_external_link(url, webdriver):
    external_link = []

    webdriver.get(url)
    html = webdriver.page_source
    soup = bs(html, 'html.parser')
    a_tags = soup.findAll('a')
    net = urlparse(url).netloc

    for tag in a_tags:
        if not ('href' in tag.attrs):
            continue
        elif tag.attrs['href'].startswith('/') or tag.attrs['href'].startswith('#'):
            continue
        elif urlparse(tag.attrs['href']).netloc == net:
            continue
        else:
            external_link.append(tag.attrs['href'])

        string_links = ','.join(external_link)
        return string_links
        # return external_link


def compare_banner_link(string_links1, string_links2):
    links1 = string_links1.split(",")
    links2 = string_links2.split(",")

    if links1 > links2:
        links1, links2 = links2, links1

    count = 0
    for link in links1:
        if links2.__contains__(link):
            count += 1

    result = 0 if count == 0 else count / len(links1) * 100
    return result


if __name__ == "__main__":
    driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    driver.implicitly_wait(3)

    external_link2 = extract_external_link("url1", driver)
    external_link1 = extract_external_link("url2", driver)


    print(compare_banner_link(external_link1, external_link2))

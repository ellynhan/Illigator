from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
from selenium import webdriver


def extract_external_link(url):
    driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
    driver.implicitly_wait(3)

    external_link = []
    driver.get(url)
    html = driver.page_source

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
    external_link_string = ','.join(external_link)

    return external_link_string


def compare_banner_link(src_links, dest_links):
    source_links = src_links.split(',')
    destination_links = dest_links.split(',')

    # src is small
    if source_links > destination_links:
        source_links, destination_links = destination_links, source_links

    count = 0
    for link in source_links:
        if destination_links.__contains__(link):
            count += 1

    result = 0 if count == 0 else count / len(source_links) * 100
    return result


if __name__ == "__main__":
    external_link2 = extract_external_link("url1")
    external_link1 = extract_external_link("url2")

    print(compare_banner_link(external_link1, external_link2))

from bs4 import BeautifulSoup  as bs
import requests

webpage = requests.get('~~')
soup = bs(webpage.content, "html.parser")

all_tags = [tag.name for tag in soup.find_all()]
open_tags = all_tags[:int(len(all_tags)/2)]
for tag in open_tags:
    print(tag)

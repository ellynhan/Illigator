from bs4 import BeautifulSoup  as bs
import requests


# 주어진 키워드리스트와 url의 html text를 비교, 어떤 키워드와 몇개나 매칭되었는지 반환
def get_hit_list(keywords, url):
    hit_list = {}
    webpage = requests.get(url)
    soup = bs(webpage.content, "html.parser")
    text = soup.text

    score = 0
    for keyword in keywords:
        keyword_count = text.count(keyword)
        if (keyword_count > 0):
            hit_list.update({keyword: keyword_count})
            score += keyword_count
    return [hit_list, score]


# sort by score with [list, [list, list]], the last list contains scores
def sort_by_sum(e):
    return e[1][1]


if __name__ == "__main__":
    gamble_keywords = ['충전', '환전', '카지노', '이벤트', '출금', '신규가입', '충환전', '입금계좌', '게임머니', '베팅', '보장', '안전놀이터', '토토']
    url_list = ['~~urls~~']

    hit_lists = []
    hit_score = []

    for url in url_list:
        list_total_score = get_hit_list(gamble_keywords, url)
        hit_lists.append(list_total_score[0])
        hit_score.append(list_total_score[1])

    result = list(zip(url_list, zip(hit_lists, hit_score)))
    result.sort(reverse=True, key=sort_by_sum)

    for r in result:
        print("총계: " + str(r[1][1]) + '\t', r[0], r[1][0])

else:
    print("crawler.py is exported!")
    # 아직 외부에서 부를 수 있을 만한 코드가 아님.

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from corp_info.models import News
import json
from ict_api.settings import NCP_KEY, NCP_KEY_ID, NAVER_ID, NAVER_SECRET


class UsingApiException(Exception):
    pass


class UsageExceededException(Exception):
    pass


def get_news(query):
    url = "https://openapi.naver.com/v1/search/news.xml"
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }

    params = {
        "query": query,
        "display": 5,
        "start": 1,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise UsingApiException('API 응답 불량')
    response = response.content.decode("utf-8")

    root = ET.fromstring(response)
    result = []

    for item in root.findall("./channel/item"):
        title = item.find("title").text.replace("<b>", "").replace("</b>", "").replace("&apos;", "")
        originallink = item.find("originallink").text
        link = item.find("link").text
        description = item.find("description").text.replace("<b>", "").replace("</b>", "").replace("&apos;", "")
        pubDate = item.find("pubDate").text

        pubDate = datetime.strptime(pubDate, "%a, %d %b %Y %H:%M:%S %z")
        pubDate = pubDate.strftime("%Y-%m-%d %H:%M:%S")

        if link.startswith("https://n.news.naver.com/"):
            item_dict = {
                "title": title,
                "originallink": originallink,
                "link": link,
                "description": description,
                "pubDate": pubDate
            }

            result.append(item_dict)

    return result


def get_news_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise UsingApiException('API 호출 불량')
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")
    target_div = soup.find('div', class_='newsct_article _article_body')

    text = target_div.get_text(strip=True)

    text = " ".join(text.split())
    text = text[:1999]

    return text


def get_summary(content):
    url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
    headers = {
        "X-NCP-APIGW-API-KEY-ID":  NCP_KEY_ID,
        "X-NCP-APIGW-API-KEY":  NCP_KEY,
        "Content-Type": "application/json"
    }

    document = {
        'content': content
    }

    option = {
        'language': 'ko',
        'model': 'news',
        'tone': 2,
        'summaryCount': 3
    }

    data = {
        'document': document,
        'option': option
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        summary = result['summary']
    else:
        raise UsageExceededException("사용량 초과")
    return summary


def save_news(query, result):
    for item in result:
        title = item['title']
        link = item['link']
        originallink = item['originallink']
        description = item['description']
        pubDate = item['pubDate']
        article = get_news_content(link)
        summary = get_summary(article)

        news = News(
            query=query,
            title=title,
            link=link,
            originalLink=originallink,
            description=description,
            pubData=pubDate,
            article=article,
            summary=summary,
        )
        news.save()



# -*- coding: utf-8 -*-

'''
Info
- author : "wyh"
- date   : "2018.3.21"
- description : 解析网页
'''


import requests

from utils import *
from db import Db
from lxml import etree
import queue



def MouthHot():
    '''
    解析月热点提问和回答
    :return: None
    '''
    url = 'https://www.zhihu.com/node/ExploreAnswerListV2?params=%7B%22offset%22%3A{}%2C%22type%22%3A%22month%22%7D'
    urls = [url.format(page) for page in range(0,10,5)]
    responses = [get_page(url) for url in urls]
    htmls = [response.text for response in responses]
    baseurl = 'https://www.zhihu.com'
    for html in htmls:
        xpathObj = etree.HTML(html)
        # author_pages = xpathObj.xpath('//a[@class="UserLink-link"]/@href')
        # for author_link in author_links:
        #     user_list.put(author_link)
        question_pages = xpathObj.xpath('//a[@class="question_link"]/@href')
        question_links = [baseurl+l for l in question_pages]
        for question_link in question_links:
            QuestionPage(question_link)
    return


def FindUsers(author_page,offset):
    '''
    :param author_page:用户页面id
           offset:页码
    :return: True or False
    '''
    baseUrl = 'https://www.zhihu.com/api/v4/members/{author_page}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'.format(author_page=author_page,offset=offset)
    newHeaders = headers.copy()
    newHeaders['authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    response = get_page(baseUrl,headers=newHeaders)
    for i in response.json()['data']:
          user_list.put(i['url_token'])
          db = Db()
          db.Users(i)
    if response.json()['paging']['is_end'] == True:
        return False
    else:
        return True

    # author_link = "https:"+author_page+"activities"
    # html = get_page(author_link)
    # xpathObj = etree.HTML(html.text)
    # NumberBoard = xpathObj.xpath('//strong[@class="NumberBoard-itemValue"]/@title')
    # #favorites = NumberBoard[0]
    # followers = NumberBoard[1]
    # if followers >= 10000:
    #     PopularUsers(author_link)
    # followingsUrl = "https:"+author_page+"following"
    # html1 = get_page(followingsUrl)
    # xpathObj1 = etree.HTML(html1.text)
    # followings = xpathObj1.xpath('//a[@class="UserLink-link"]/@href')
    # for following in followings:
    #     user_list.put(following)


def QuestionPage(question_link):
    '''
    :param question_link:问题页面 
    :return: 问题标签
    '''
    html = get_page(question_link)
    xpathObj = etree.HTML(html.text)
    title = xpathObj.xpath('//h1[@class="QuestionHeader-title"]/text()')
    tags = xpathObj.xpath('//div[@class="QuestionHeader-topics"]//div[@class="Tag QuestionTopic"]//text()')
    item = {
        "title":title,
        "question_link":question_link,
        "tags":tags
    }
    db = Db()
    db.Questions(item)
    return

if __name__=="__main__":
    #MouthHot()
    global user_list
    user_list = queue.Queue()
    user_list.put('McDoge')
    while not user_list.empty():
        author_page = user_list.get()
        offset = 0
        user_data = FindUsers(author_page,offset)
        while user_data:
            offset += 20
            user_data = FindUsers(author_page, offset)
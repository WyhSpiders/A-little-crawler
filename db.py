# -*- coding: utf-8 -*-
'''
Info
- author : "wyh"
- date   : "2018.3.21"
- description : 和数据库相关的操作，创建数据库表，插入数据
'''

#import pymongo
import pymysql

class Db(object):
    def __init__(self):
        # self.port = 27017
        # self.host = 'localhost'
        # self.db_name = 'Zhihu'
        # self.client = pymongo.MongoClient(self.host, self.port)
        # self.db = self.client[self.db_name]
        # self.collection_questions = self.db["Questions"]
        # self.collection_questions.ensure_index("question_link",unique=True)
        # self.collection_users = self.db["Users"]
        # self.collection_users.ensure_index("user_id", unique=True)
        self.conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='root',db='test',charset='utf8')

    def Questions(self,item):
        '''
        问题信息
        :return: 
        '''
       # print(item)
       #  try:
       #      print(item)
       #      self.collection_questions.insert_one(item)
       #  except:
       #      print("error")
       #  return
        pass



    def Users(self, data):
        '''
        用户信息
        :return: 
        '''
        sql = '''
INSERT INTO users 
(
answer_count,  
articles_count,  
follower_count,  
gender,  
headline,    
is_advertiser,  
is_followed,  
is_following,  
is_org,  
user_name,  
url,  
url_token,  
user_type 
)
VALUES('{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}',  '{}' );
        '''.format(
            data['answer_count'],
            data['articles_count'],
            data['follower_count'],
            data['gender'],
            data['headline'],
            str(data['is_advertiser']),
            str(data['is_followed']),
            str(data['is_following']),
            str(data['is_org']),
            data['name'],
            data['url'],
            data['url_token'],
            data['user_type']
        )
        try:
            cursor = self.conn.cursor()
            print('写入数据库...')
            #print(sql)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.close()

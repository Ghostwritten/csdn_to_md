#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import uuid
import time
import requests
import datetime
import argparse
import re
from bs4 import BeautifulSoup


def request_blog_column(id):

    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    
    urls = 'https://blog.csdn.net/' + id
    reply = requests.get(url=urls,headers=headers)
    parse = BeautifulSoup(reply.content, "html.parser")
    spans = parse.find_all('a', attrs={'class':'special-column-name'})

    blog_columns = []
    
    for span in spans:
          href = re.findall(r'href=\"(.*?)\".*?',str(span),re.S)
          href = ''.join(href)
         # print(href)

          headers = {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
          }
          blog_column_reply = requests.get(url=href,headers=headers)
         # print(blog_column_reply)
          blogs_num = re.findall(r'<a class="clearfix special-column-name"  href=\"'+ href +'\".*?<span class="special-column-num">(.+?)篇</span>',blog_column_reply.text,re.S)
         # print(str(blogs_num[0]))
          blogs_column_num = str(blogs_num[0])


          blog_column = span.text.strip()

          blog_column_dir = './' + str(id) + '/' + str(blog_column)          
          if not os.path.exists(blog_column_dir):
            os.mkdir(blog_column_dir)

          blog_id = href.split("_")[-1]
          blog_id = blog_id.split(".")[0]
          blog_columns.append([href,blog_column,blog_id,blogs_column_num])
        #  print(blog_columns)
          
 

    return blog_columns

def request_blog_list(id):
    blog_columns = request_blog_column(id)
    blogs = []
    for blog_column in blog_columns:
        blog_column_url = blog_column[0]
        blog_column_name = blog_column[1]
        blog_column_id = blog_column[2]
        blog_column_num = int(blog_column[3])
        #print(blog_column_url) 

        if blog_column_num > 40: 
           page_num = round(blog_column_num/40)
           for i in range(page_num,0,-1):
               blog_column_url = blog_column[0]
               url_str = blog_column_url.split('.html')[0]
               blog_column_url = url_str + '_' + str(i) + '.html'
               append_blog_info(blog_column_url,blog_column_name,blogs)
           blog_column_url = blog_column[0]
           blogs = append_blog_info(blog_column_url,blog_column_name,blogs)
        #   print(blogs)
               
        else:
           blogs = append_blog_info(blog_column_url,blog_column_name,blogs)
        #   print(blogs)
   
    #print(blogs)
    return blogs


def append_blog_info(blog_column_url,blog_column_name,blogs):
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    reply = requests.get(url=blog_column_url,headers=headers)
    blog_span = BeautifulSoup(reply.content, "html.parser")
    blogs_list = blog_span.find_all('ul', attrs={'class':'column_article_list'})
    for arch_blog_info in blogs_list:
        blogs_list = arch_blog_info.find_all('li')
        for blog_info in blogs_list:
	    
            blog_url = blog_info.find('a', attrs={'target':'_blank'})['href']
            blog_title = blog_info.find('h2', attrs={'class':"title"}).get_text().strip().replace(" ", "_").replace('/','_')
            blog_dict = {'column': blog_column_name,'url': blog_url, 'title': blog_title}
            blogs.append(blog_dict)
    return blogs 

def request_md(id):

    blogs = request_blog_list(id)
    
    for blog_dict in blogs:
        blog_url = blog_dict['url']
        blog_title = blog_dict['title']
        blog_column = blog_dict['column']
        blog_id = blog_url.split("/")[-1] 
        url = f"https://blog-console-api.csdn.net/v1/editor/getArticle?id={blog_id}"
        headers = {
        
         #"Cookie": "uuid_tt_dd=20_18815108270-1651420958061-407001;dc_session_id=10_1651420958062.474827;acw_tc=276077c116514209580398703eb6ccd1972794b4689cf3b5039f85506a6146;UserName=hahalelehehe; UserInfo=30ee073e05d84844b34a829ef0d80541; UserToken=30ee073e05d84844b34a829ef0d80541; UserNick=ghostwritten; AU=5F9; BT=1651420447587; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22xixihahalelehehe%22%2C%22scope%22%3A1%7D%7D; log_Id_click=1111; c_pref=https%3A//i.csdn.net/; c_ref=https%3A//blog.csdn.net/xixihahalelehehe%3Fspm%3D1010.2135.3001.5343; c_page_id=default; dc_tos=rb7pev; log_Id_pv=1346; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1651422057; log_Id_view=2182;",
         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
           
        }
        data = {"id": blog_id}
        reply = requests.get(url, headers=headers,data=data)
        reply_data = reply.json()
    #    print(reply_data)

        try:
           key = "key" + str(uuid.uuid4())
           content = reply_data["data"]["markdowncontent"].replace("@[toc]", "")
           blog_title_dir = './' + str(id) + '/' + str(blog_column) + '/' + str(blog_title) + '.md'
           with open(blog_title_dir, "w", encoding="utf-8") as f:
               f.write(content)
             
           print("download blog markdown blog:" + '【' + blog_column + '】' + str(blog_title))
        except Exception as e:
           print("***********************************")
           print(e)
           print(url)




def read_from_json(filename):
    jsonfile = open(filename, "r",encoding='utf-8')
    jsondata = jsonfile.read()
    return json.loads(jsondata)

def write_to_json(filename, data):
    jsonfile = open(filename, "w")
    jsonfile.write(data)



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--id', dest='id',type=str,  required=True, help='csdn name')

    args = parser.parse_args()
    
    csdn_id = args.id

    name_dir = './' + str(csdn_id)
    if not os.path.exists(name_dir):
       os.mkdir(name_dir)

    request_md(csdn_id)

if __name__ == '__main__':
    main()
